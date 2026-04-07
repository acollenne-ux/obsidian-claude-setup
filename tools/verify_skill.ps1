$f = 'C:\Users\Alexandre collenne\.claude\skills\deep-research\SKILL.md'
if(Test-Path $f){
    $c = Get-Content $f
    Write-Host "Lignes: $($c.Count)"
    Write-Host "Taille: $((Get-Item $f).Length) octets"
    Write-Host "Premiere: $($c[0])"
    Write-Host "Derniere: $($c[$c.Count-1])"
    $hasKey = ($c | Select-String -Pattern '[a-f0-9]{20,}|sk-[a-zA-Z0-9]|gsk_|hf_' -Quiet)
    if($hasKey){Write-Host "ALERTE: cles API detectees!"}
    else{Write-Host "OK: aucune cle API detectee"}
} else {
    Write-Host "FICHIER NON TROUVE"
}