import base64, sys, shutil

src = r"C:\Users\Alexandre collenne\.claude\skills\deep-research\SKILL.md"
dst = src
b64_file = r"C:\Users\Alexandre collenne\.claude\tools\mega_b64.txt"
bak = src + ".bak_before_restore"

# Backup
shutil.copy2(src, bak)
print(f"Backup: {bak}")

# Decode
with open(b64_file, 'r') as f:
    b64_data = f.read().strip()

decoded = base64.b64decode(b64_data)
with open(dst, 'wb') as f:
    f.write(decoded)

print(f"Written {len(decoded)} bytes to {dst}")

# Count lines
with open(dst, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
