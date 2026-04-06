import base64, gzip, os, sys

b64_file = r'C:\Users\Alexandre collenne\.claude\tools\skill_b64.txt'
target = r'C:\Users\Alexandre collenne\.claude\skills\deep-research\SKILL.md'

print(f'Lecture de {b64_file}...')
with open(b64_file, 'r', encoding='utf-8') as f:
    b64_data = f.read().replace('\n', '').replace('\r', '').strip()

print(f'Base64 lu: {len(b64_data)} caracteres')
compressed = base64.b64decode(b64_data)
print(f'Decompression gzip ({len(compressed)} octets)...')
decoded = gzip.decompress(compressed).decode('utf-8')

os.makedirs(os.path.dirname(target), exist_ok=True)
with open(target, 'w', encoding='utf-8') as f:
    f.write(decoded)

lines = decoded.count('\n') + 1
size = len(decoded)
print(f'OK: {target}')
print(f'   {lines} lignes, {size} octets')

# Verification rapide
if lines < 1900:
    print(f'ATTENTION: seulement {lines} lignes (attendu ~1974)')
else:
    print('Verification OK: nombre de lignes correct')
