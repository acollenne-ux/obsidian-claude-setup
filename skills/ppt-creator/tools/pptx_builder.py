#!/usr/bin/env python3
"""
Génère un .pptx éditable à partir d'un YAML de deck.

Usage:
    python pptx_builder.py deck.yaml out.pptx [--template pitch_deck]
"""
import sys
from pathlib import Path

PRIMARY = (0x0B, 0x3D, 0x91)
ACCENT = (0xE6, 0x39, 0x46)
INK = (0x1A, 0x1A, 0x1A)

def build(deck: dict, out: Path, template: str = "executive_deck"):
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    for slide_data in deck.get("slides", []):
        slide = prs.slides.add_slide(blank)
        # Action title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.3), Inches(0.9))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = slide_data.get("action_title", "Action title manquant")
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = RGBColor(*PRIMARY)
        # Bullets
        body = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.5))
        btf = body.text_frame
        btf.word_wrap = True
        for i, bullet in enumerate(slide_data.get("bullets", [])):
            p = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
            r = p.add_run()
            r.text = f"• {bullet}"
            r.font.size = Pt(16)
            r.font.color.rgb = RGBColor(*INK)
        # Notes orateur
        notes = slide_data.get("notes", "")
        if notes:
            slide.notes_slide.notes_text_frame.text = notes

    prs.save(str(out))
    print(f"[OK pptx] {out}")

def main():
    if len(sys.argv) < 3:
        print("Usage: pptx_builder.py deck.yaml out.pptx")
        sys.exit(1)
    try:
        import yaml
    except ImportError:
        print("[ERR] pip install pyyaml", file=sys.stderr); sys.exit(2)
    deck = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    build(deck, Path(sys.argv[2]))

if __name__ == "__main__":
    main()
