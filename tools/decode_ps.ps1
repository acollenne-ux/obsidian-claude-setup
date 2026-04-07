$b64 = Get-Content 'C:\Users\Alexandre collenne\.claude\tools\skill_b64.txt' -Raw
$b64 = $b64 -replace '\r?\n',''
$bytes = [Convert]::FromBase64String($b64)
$ms = New-Object System.IO.MemoryStream(,$bytes)
$gs = New-Object System.IO.Compression.GZipStream($ms,[System.IO.Compression.CompressionMode]::Decompress)
$sr = New-Object System.IO.StreamReader($gs,[System.Text.Encoding]::UTF8)
$text = $sr.ReadToEnd()
$sr.Close()
$gs.Close()
$ms.Close()
$target = 'C:\Users\Alexandre collenne\.claude\skills\deep-research\SKILL.md'
$dir = Split-Path $target
if(!(Test-Path $dir)){New-Item -ItemType Directory -Path $dir -Force}
[System.IO.File]::WriteAllText($target, $text, [System.Text.Encoding]::UTF8)
$lines = ($text -split '\r?\n').Count
$size = $text.Length
Write-Host "OK: $target"
Write-Host "   $lines lignes, $size octets"
if($lines -lt 1900){Write-Host "ATTENTION: seulement $lines lignes (attendu ~1974)"}
else{Write-Host "Verification OK: nombre de lignes correct"}