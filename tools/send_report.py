"""
send_report.py v3 — Generateur PDF + envoi email (CLI leger).

Refactore : delegue toute la generation au module pdf_engine/.
Conserve la compatibilite arriere COMPLETE avec les anciens appels.

Usage :
  python send_report.py "Sujet" "contenu markdown" [email]
  python send_report.py "Sujet" --file chemin.md [email]

Options nouvelles (v3) :
  --template <nom>      executive | financial | technical | research | minimal
  --no-cover            desactive la page de garde complete
  --check-quality       lance un quality check apres generation
  --pdf-ua              tag PDF/UA-1 (accessibilite ISO)
  --no-email            ne pas envoyer l'email (genere et garde le PDF local)
  --output-dir <dir>    repertoire de sortie (defaut: reports/AAAA-MM/)

Variables d'env :
  GMAIL_SENDER, GMAIL_APP_PASSWORD (fallback si email_config.json absent)

Backward compat : tous les anciens appels fonctionnent sans modification.
"""
import sys
import os
import json
import re
import smtplib
import logging
import argparse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# pdf_engine est dans le meme repertoire (tools/)
sys.path.insert(0, str(Path(__file__).parent))
try:
    from pdf_engine.renderer import render_pdf, list_templates
    from pdf_engine.quality_check import format_quality_report
    PDF_ENGINE_OK = True
except ImportError as e:
    logger.error(f"[FATAL] pdf_engine indisponible : {e}")
    logger.error("        Verifiez que ~/.claude/tools/pdf_engine/ existe et que weasyprint est installe.")
    PDF_ENGINE_OK = False

CONFIG_PATH = Path(__file__).parent / "email_config.json"
REPORTS_BASE = Path(__file__).parent / "reports"
DEFAULT_TO = "acollenne@gmail.com"


# =====================================================================
# DETECTION TYPE DOC + TEMPLATE
# =====================================================================
def detect_type(title: str) -> str:
    """Detecte le type de document depuis le titre."""
    t = title.upper()
    if ' - CODE' in t or t.endswith('CODE'):
        return 'code'
    if 'GUIDE' in t or 'MISE EN ROUTE' in t:
        return 'guide'
    if 'MODIF' in t or 'AJOUT' in t:
        return 'modifications'
    if any(k in t for k in ('FINANC', 'TRADING', 'BOURSE', 'ACTION', 'CRYPTO', 'DCF', 'VALORISATION')):
        return 'financial'
    if 'EXECUTIVE' in t or 'SYNTHESE' in t or 'BOARD' in t:
        return 'executive'
    if 'RECHERCHE' in t or 'RESEARCH' in t or 'ETUDE' in t:
        return 'research'
    return 'analysis'


def auto_select_template(doc_type: str) -> str:
    """Choisit le template par defaut selon le type."""
    return {
        'code': 'technical',
        'guide': 'technical',
        'modifications': 'technical',
        'financial': 'financial',
        'executive': 'executive',
        'research': 'research',
        'analysis': 'executive',
    }.get(doc_type, 'executive')


# =====================================================================
# ENVOI EMAIL (conserve)
# =====================================================================
def send_email(subject: str, pdf_paths, recipient: str = DEFAULT_TO) -> bool:
    """Envoie un email avec les PDFs en piece jointe."""
    sender = None
    pwd = None
    try:
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        sender = cfg.get("sender_email")
        pwd = cfg.get("gmail_app_password")
    except FileNotFoundError:
        logger.warning(f"Config introuvable : {CONFIG_PATH}")
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Erreur lecture config email : {e}")

    if not sender:
        sender = os.environ.get('GMAIL_SENDER')
    if not pwd:
        pwd = os.environ.get('GMAIL_APP_PASSWORD')

    if not sender or not pwd:
        logger.warning(
            "Configuration email manquante. PDF genere localement sans envoi."
        )
        for p in (pdf_paths if isinstance(pdf_paths, list) else [pdf_paths]):
            logger.info(f"  PDF disponible : {p}")
        return False

    if isinstance(pdf_paths, str):
        pdf_paths = [pdf_paths]

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    n = len(pdf_paths)
    files_list = ''.join(
        f'<li style="padding:4px 0">{Path(p).name}</li>' for p in pdf_paths
    )
    html = f"""<html><body style="font-family:'Segoe UI',Arial,sans-serif;max-width:700px;margin:auto;color:#2d3748">
    <div style="background:linear-gradient(135deg,#1a365d 0%,#2b6cb0 100%);padding:22px 28px;border-radius:8px 8px 0 0">
      <h2 style="color:white;margin:0;font-size:18px;font-weight:700">{subject}</h2>
      <p style="color:#bee3f8;margin:6px 0 0;font-size:11px">
        {datetime.now().strftime('%d/%m/%Y %H:%M')} &mdash; Claude Code - Deep Research
      </p>
    </div>
    <div style="background:#f7fafc;padding:20px 28px;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 8px 8px">
      <p style="margin-top:0;color:#2d3748">{n} document(s) en piece(s) jointe(s) :</p>
      <ul style="color:#2b6cb0;font-weight:500">{files_list}</ul>
      <hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0">
      <p style="font-size:10px;color:#a0aec0;margin-bottom:0">
        Genere automatiquement par le systeme Deep Research multi-agents (pdf_engine v2).
      </p>
    </div></body></html>"""
    msg.attach(MIMEText(html, "html"))

    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{Path(pdf_path).name}"'
            )
            msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
        srv.login(sender, pwd)
        srv.send_message(msg)
    logger.info(f"[Email] Envoye a {recipient} ({n} PDF(s))")
    return True


# =====================================================================
# CLI / MAIN
# =====================================================================
def parse_legacy_args(argv: list[str]) -> dict:
    """Parse les arguments avec retro-compatibilite totale.

    Anciens formats supportes :
      send_report.py "Sujet" "contenu" [email]
      send_report.py "Sujet" --file rapport.md [email]

    Nouveaux flags : --template, --no-cover, --check-quality, --pdf-ua,
                     --no-email, --output-dir
    """
    if len(argv) < 3:
        raise SystemExit(
            "Usage: python send_report.py 'Sujet' 'contenu_ou_--file' [email] [options]\n"
            "       python send_report.py 'Sujet' --file chemin.md [email] [options]\n"
            "\n"
            "Options:\n"
            "  --template <nom>     executive | financial | technical | research | minimal\n"
            "  --no-cover           desactive la page de garde complete\n"
            "  --check-quality      lance le quality check apres generation\n"
            "  --pdf-ua             tag PDF/UA-1 (accessibilite ISO)\n"
            "  --no-email           ne pas envoyer l'email\n"
            "  --output-dir <dir>   repertoire de sortie\n"
        )

    subject = argv[1]
    rest = argv[2:]

    # Defaults
    parsed = {
        'subject': subject,
        'content': None,
        'recipient': DEFAULT_TO,
        'template': None,
        'with_cover': True,
        'check_quality': False,
        'pdf_ua': False,
        'send_email': True,
        'output_dir': None,
    }

    i = 0
    positional = []
    while i < len(rest):
        arg = rest[i]
        if arg == '--file':
            if i + 1 >= len(rest):
                raise SystemExit("--file necessite un chemin")
            file_path = rest[i + 1]
            with open(file_path, 'r', encoding='utf-8') as f:
                parsed['content'] = f.read()
            i += 2
        elif arg == '--template':
            parsed['template'] = rest[i + 1]
            i += 2
        elif arg == '--no-cover':
            parsed['with_cover'] = False
            i += 1
        elif arg == '--check-quality':
            parsed['check_quality'] = True
            i += 1
        elif arg == '--pdf-ua':
            parsed['pdf_ua'] = True
            i += 1
        elif arg == '--no-email':
            parsed['send_email'] = False
            i += 1
        elif arg == '--output-dir':
            parsed['output_dir'] = rest[i + 1]
            i += 2
        else:
            positional.append(arg)
            i += 1

    # Premier positionnel = contenu (si pas --file), deuxieme = email
    if parsed['content'] is None and positional:
        parsed['content'] = positional[0]
        positional = positional[1:]
    if positional:
        parsed['recipient'] = positional[0]

    if parsed['content'] is None:
        raise SystemExit("Contenu manquant : utilisez --file ou passez le markdown en argument")

    return parsed


def get_output_path(subject: str, output_dir: str | None) -> str:
    """Construit le chemin de sortie : reports/AAAA-MM/rapport_titre_TS.pdf"""
    now = datetime.now()
    if output_dir:
        out_base = Path(output_dir)
    else:
        out_base = REPORTS_BASE / now.strftime('%Y-%m')
    out_base.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r'[^\w-]', '_', subject[:40])
    ts = now.strftime("%Y%m%d_%H%M%S")
    return str(out_base / f"rapport_{safe}_{ts}.pdf")


def main():
    if not PDF_ENGINE_OK:
        sys.exit(1)

    args = parse_legacy_args(sys.argv)

    doc_type = detect_type(args['subject'])
    template = args['template'] or auto_select_template(doc_type)

    if template not in list_templates():
        logger.warning(f"Template '{template}' inconnu. Disponibles : {list_templates()}")
        template = 'executive'

    pdf_path = get_output_path(args['subject'], args['output_dir'])

    logger.info(f"[Generation PDF] Template: {template} | Type: {doc_type}")
    logger.info(f"  Titre  : {args['subject'][:60]}")
    logger.info(f"  Sortie : {pdf_path}")

    result = render_pdf(
        title=args['subject'],
        content=args['content'],
        output=pdf_path,
        template=template,
        doc_type=doc_type,
        with_cover=args['with_cover'],
        check_quality=args['check_quality'],
        pdf_ua=args['pdf_ua'],
    )

    logger.info(f"  PDF genere : {result['size_kb']} KB")

    if args['check_quality']:
        logger.info(format_quality_report(result))
        if not result.get('qc_ok'):
            logger.warning("[QC] Quality check echoue. Voir details ci-dessus.")

    if args['send_email']:
        logger.info(f"  Envoi email a {args['recipient']}...")
        sent = send_email(args['subject'], [pdf_path], args['recipient'])
        if not sent:
            logger.warning("[SKIP] Email non envoye. PDF disponible localement.")
        else:
            logger.info("[OK] Rapport envoye avec succes.")
    else:
        logger.info("[SKIP] --no-email specifie, PDF disponible localement.")


if __name__ == '__main__':
    main()
