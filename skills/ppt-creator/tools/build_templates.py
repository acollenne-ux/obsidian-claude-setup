#!/usr/bin/env python3
"""
Génère les 5 templates .pptx squelettes via python-pptx.

Usage:
    python build_templates.py [out_dir]
"""
import sys
from pathlib import Path

TEMPLATES = {
    "executive_deck": {
        "slide_count": 8,
        "theme": "Exécutif 5-10 slides",
        "slides": ["Title", "Executive summary", "Key finding 1", "Key finding 2",
                   "Key finding 3", "Recommandations", "Next steps", "Annexes"],
    },
    "institutional_deck": {
        "slide_count": 22,
        "theme": "Rapport institutionnel 20+ slides",
        "slides": ["Title", "Agenda", "Key message", "Context"] + [f"Section {i}" for i in range(1, 15)] + ["Recos", "Annexes", "Sources"],
    },
    "financial_analysis_deck": {
        "slide_count": 15,
        "theme": "Analyse financière action",
        "slides": ["Title", "Thèse", "Valorisation", "DCF", "Comps", "Multiples",
                   "Risques", "Catalyseurs", "Scénarios", "Bull case", "Base case",
                   "Bear case", "Recommandation", "Target price", "Sources"],
    },
    "data_deck": {
        "slide_count": 12,
        "theme": "Data-heavy",
        "slides": ["Title", "Key insight"] + [f"Chart {i}" for i in range(1, 9)] + ["Méthodologie", "Dataset"],
    },
    "pitch_deck": {
        "slide_count": 15,
        "theme": "Pitch investisseur Sequoia/YC",
        "slides": ["Cover", "Problème", "Solution", "Marché (TAM/SAM/SOM)", "Produit",
                   "Traction", "Business model", "GTM", "Compétition", "Équipe",
                   "Roadmap", "Financials", "Ask", "Use of funds", "Contact"],
    },
}

def build_template(name: str, spec: dict, out_dir: Path):
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
    except ImportError:
        print(f"[SKIP {name}] python-pptx non installé, génération du .md squelette uniquement")
        md = out_dir / f"{name}.md"
        md.write_text(f"# Template {name}\n\n**{spec['theme']}**\n\n" +
                      "\n".join(f"- Slide {i+1}: {s}" for i, s in enumerate(spec["slides"])),
                      encoding="utf-8")
        return
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    for i, title in enumerate(spec["slides"]):
        slide = prs.slides.add_slide(blank)
        tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.9))
        p = tb.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = f"[{i+1}/{spec['slide_count']}] {title}"
        r.font.size = Pt(24)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0B, 0x3D, 0x91)
    out = out_dir / f"{name}.pptx"
    prs.save(str(out))
    print(f"[OK] {out}")

def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "templates"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, spec in TEMPLATES.items():
        build_template(name, spec, out_dir)

if __name__ == "__main__":
    main()
