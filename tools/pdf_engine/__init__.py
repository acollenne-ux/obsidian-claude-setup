"""
pdf_engine — Moteur de generation PDF professionnel.

Architecture modulaire :
  - markdown_parser : parsing enrichi (callouts, footnotes, KPI YAML, frontmatter)
  - components      : composants reutilisables (cover, kpi_card, callout, dashboard)
  - mermaid         : rendu Mermaid -> PNG -> embed base64
  - renderer        : pipeline WeasyPrint complet (templates, PDF/UA)
  - quality_check   : QC post-generation (pages, taille, lisibilite, tags)
  - templates/      : 5 themes CSS externes (executive, financial, technical, research, minimal)

Usage rapide :
  from pdf_engine.renderer import render_pdf
  render_pdf(title="Mon rapport", content=md, output="rapport.pdf",
             template="financial", cover=True, check_quality=True)
"""
from .renderer import render_pdf, list_templates
from .quality_check import check_pdf_quality
from .markdown_parser import parse_markdown_document

__version__ = "2.0.0"
__all__ = [
    "render_pdf",
    "list_templates",
    "check_pdf_quality",
    "parse_markdown_document",
]
