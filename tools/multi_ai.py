"""
multi_ai.py — Orchestrateur multi-IA parallele.
Interroge DeepSeek, Mistral, Gemini, GitHub Models, Groq, OpenAI, xAI en parallele.

Usage:
  python multi_ai.py query "ta question" [--models deepseek,mistral] [--mode chat|reason|research]
  python multi_ai.py query "ta question" --best          # retourne la meilleure reponse
  python multi_ai.py query "ta question" --aggregate     # synthetise toutes les reponses
  python multi_ai.py list                                # liste les modeles disponibles
  python multi_ai.py add-key <provider> <key>           # ajoute une cle API

Modes:
  chat     : reponse rapide (deepseek-chat + mistral-small)
  reason   : raisonnement profond (deepseek-reasoner + mistral-large)
  research : tous les modeles disponibles en parallele (max precision)
"""
import sys, os, json, asyncio, time, argparse
from pathlib import Path
from openai import AsyncOpenAI

# Fix encodage Windows (CMD cp1252 ne supporte pas tous les caracteres Unicode)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CONFIG_PATH = Path(__file__).parent / "ai_config.json"


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def get_enabled_providers(cfg, requested=None):
    providers = []
    for name, data in cfg.items():
        if not data.get("enabled", False):
            continue
        if requested and name not in requested:
            continue
        providers.append((name, data))
    return providers


async def query_provider(name, data, prompt, model_key="chat"):
    models = data.get("models", {})
    model = models.get(model_key) or list(models.values())[0]

    client = AsyncOpenAI(
        api_key=data["api_key"],
        base_url=data["base_url"],
    )

    start = time.time()
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            timeout=60,
        )
        elapsed = round(time.time() - start, 1)
        content = resp.choices[0].message.content or ""
        return {
            "provider": name,
            "model": model,
            "content": content,
            "elapsed": elapsed,
            "error": None,
        }
    except Exception as e:
        return {
            "provider": name,
            "model": model,
            "content": "",
            "elapsed": round(time.time() - start, 1),
            "error": str(e),
        }


async def query_all(providers, prompt, model_key="chat"):
    tasks = [query_provider(name, data, prompt, model_key) for name, data in providers]
    return await asyncio.gather(*tasks)


def pick_best(results):
    """Retourne la reponse la plus longue et sans erreur."""
    valid = [r for r in results if not r["error"] and r["content"]]
    if not valid:
        return None
    return max(valid, key=lambda r: len(r["content"]))


def format_aggregate(results):
    """Formate une synthese de toutes les reponses."""
    lines = []
    for r in results:
        if r["error"]:
            lines.append(f"\n## [{r['provider'].upper()}] ERREUR\n{r['error']}")
        else:
            lines.append(f"\n## [{r['provider'].upper()} — {r['model']}] ({r['elapsed']}s)\n{r['content']}")
    return "\n".join(lines)


def synthesize_with_deepseek(responses_text, original_prompt):
    """Utilise DeepSeek pour synthetiser les reponses de tous les modeles."""
    cfg = load_config()
    if not cfg["deepseek"]["enabled"]:
        return None

    import openai
    client = openai.OpenAI(
        api_key=cfg["deepseek"]["api_key"],
        base_url=cfg["deepseek"]["base_url"],
    )

    synthesis_prompt = f"""Tu es un expert en synthese. Voici une question posee a plusieurs IA :

QUESTION ORIGINALE : {original_prompt}

REPONSES DES DIFFERENTES IA :
{responses_text}

Synthetise ces reponses en une seule reponse optimale, claire et complete.
Prends le meilleur de chaque reponse. Signale si des reponses se contredisent.
Reponds en francais sauf si la question est en anglais."""

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": synthesis_prompt}],
            timeout=90,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erreur synthese DeepSeek : {e}"


def main():
    parser = argparse.ArgumentParser(description="Multi-IA Orchestrateur")
    subparsers = parser.add_subparsers(dest="command")

    # query
    q_parser = subparsers.add_parser("query", help="Interroger les IA")
    q_parser.add_argument("prompt", help="La question a poser")
    q_parser.add_argument("--models", help="Providers a utiliser (ex: deepseek,mistral)")
    q_parser.add_argument("--mode", choices=["chat", "reason", "research"], default="chat")
    q_parser.add_argument("--best", action="store_true", help="Retourner uniquement la meilleure reponse")
    q_parser.add_argument("--aggregate", action="store_true", help="Afficher toutes les reponses")
    q_parser.add_argument("--synthesize", action="store_true", help="Synthetiser via DeepSeek")

    # list
    subparsers.add_parser("list", help="Lister les providers disponibles")

    # add-key
    k_parser = subparsers.add_parser("add-key", help="Ajouter une cle API")
    k_parser.add_argument("provider", help="Nom du provider (ex: gemini)")
    k_parser.add_argument("key", help="La cle API")

    # enable / disable
    e_parser = subparsers.add_parser("enable", help="Activer un provider")
    e_parser.add_argument("provider")
    d_parser = subparsers.add_parser("disable", help="Desactiver un provider")
    d_parser.add_argument("provider")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cfg = load_config()

    # --- LIST ---
    if args.command == "list":
        print("\nProviders disponibles :")
        for name, data in cfg.items():
            status = "ACTIF" if data.get("enabled") else "inactif"
            models_str = ", ".join(data.get("models", {}).values())
            print(f"  {name:15} [{status:6}]  modeles: {models_str}")
            if not data.get("enabled") and data.get("note"):
                print(f"                         -> {data['note']}")
        return

    # --- ADD-KEY ---
    if args.command == "add-key":
        provider = args.provider.lower()
        if provider not in cfg:
            print(f"Provider inconnu : {provider}")
            return
        cfg[provider]["api_key"] = args.key
        cfg[provider]["enabled"] = True
        save_config(cfg)
        print(f"Cle ajoutee et {provider} active.")
        return

    # --- ENABLE / DISABLE ---
    if args.command == "enable":
        cfg[args.provider]["enabled"] = True
        save_config(cfg)
        print(f"{args.provider} active.")
        return
    if args.command == "disable":
        cfg[args.provider]["enabled"] = False
        save_config(cfg)
        print(f"{args.provider} desactive.")
        return

    # --- QUERY ---
    if args.command == "query":
        requested = [m.strip() for m in args.models.split(",")] if args.models else None
        providers = get_enabled_providers(cfg, requested)

        if not providers:
            print("Aucun provider actif. Utilisez 'python multi_ai.py list' pour voir les options.")
            print("Ajoutez une cle avec : python multi_ai.py add-key <provider> <key>")
            sys.exit(1)

        # Choisir le bon model_key selon le mode
        if args.mode == "reason":
            model_key = "reasoner"
        elif args.mode == "research":
            model_key = "large"
        else:
            model_key = "chat"

        print(f"Interrogation de {len(providers)} IA(s) en parallele : {[p[0] for p in providers]}")
        print(f"Mode : {args.mode} | Modele : {model_key}\n")

        results = asyncio.run(query_all(providers, args.prompt, model_key))

        if args.aggregate:
            print(format_aggregate(results))

        elif args.synthesize:
            valid = [r for r in results if not r["error"] and r["content"]]
            if not valid:
                print("Aucune reponse valide obtenue.")
                sys.exit(1)
            responses_text = "\n\n".join(
                f"[{r['provider'].upper()} — {r['model']}]:\n{r['content']}" for r in valid
            )
            print(f"Synthese de {len(valid)} reponse(s) via DeepSeek...\n")
            synthesis = synthesize_with_deepseek(responses_text, args.prompt)
            print(synthesis or "Echec de la synthese.")

        else:
            # Par defaut : meilleure reponse
            best = pick_best(results)
            if best:
                print(f"[{best['provider'].upper()} — {best['model']}] ({best['elapsed']}s)\n")
                print(best["content"])
            else:
                print("Toutes les IA ont echoue :")
                for r in results:
                    print(f"  {r['provider']}: {r['error']}")

        # Toujours afficher le resume des erreurs si --aggregate pas actif
        if not args.aggregate:
            errors = [r for r in results if r["error"]]
            if errors:
                print(f"\n[{len(errors)} erreur(s): {', '.join(r['provider'] for r in errors)}]")


if __name__ == "__main__":
    main()
