"""Restore mega-skill from base64 chunks."""
import sys, base64
from pathlib import Path

SKILL_PATH = Path(r"C:\Users\Alexandre collenne\.claude\skills\deep-research\SKILL.md")
CHUNKS_DIR = Path(r"C:\Users\Alexandre collenne\.claude\tools\b64_chunks")

def restore():
    # Read and concatenate all chunks in order
    chunks = sorted(CHUNKS_DIR.glob("chunk_*"))
    if not chunks:
        print("ERROR: No chunks found")
        return
    
    b64_data = ""
    for c in chunks:
        b64_data += c.read_text(encoding="utf-8").strip()
    
    # Decode
    content = base64.b64decode(b64_data).decode("utf-8")
    
    # Backup current
    if SKILL_PATH.exists():
        backup = SKILL_PATH.with_suffix(".md.bak")
        backup.write_text(SKILL_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Backup: {backup}")
    
    # Write restored
    SKILL_PATH.write_text(content, encoding="utf-8")
    lines = content.count("\n") + 1
    print(f"Restored: {SKILL_PATH} ({lines} lines)")

if __name__ == "__main__":
    restore()
