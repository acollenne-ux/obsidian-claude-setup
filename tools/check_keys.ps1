$f = 'C:\Users\Alexandre collenne\.claude\skills\deep-research\SKILL.md'
$c = Get-Content $f -Raw
$patterns = @(
    '[a-f0-9]{32,}',
    'sk-[a-zA-Z0-9]{20,}',
    'gsk_[a-zA-Z0-9]{20,}',
    'hf_[a-zA-Z0-9]{20,}'
)
$found = $false
foreach ($p in $patterns) {
    $matches = [regex]::Matches($c, $p)
    if ($matches.Count -gt 0) {
        Write-Output "ALERTE: Pattern $p trouve $($matches.Count) fois"
        $found = $true
    }
}
if (-not $found) {
    Write-Output "OK: Aucune cle API detectee"
}
Write-Output "Lignes: $((Get-Content $f).Count)"
Write-Output "Taille: $((Get-Item $f).Length) octets"
Write-Output "Premiere ligne: $((Get-Content $f)[0])"
Write-Output "Derniere ligne: $((Get-Content $f)[-1])"