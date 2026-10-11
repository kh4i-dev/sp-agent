$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$src = Join-Path $root ".claude\skills"
$dst = Join-Path $root ".agents\skills"

if (-not (Test-Path -LiteralPath $src)) {
    throw "Khong tim thay thu muc nguon: $src"
}

if (Test-Path -LiteralPath $dst) {
    Remove-Item -LiteralPath $dst -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $dst | Out-Null

Copy-Item -Path (Join-Path $src "*") -Destination $dst -Recurse -Force

$count = (Get-ChildItem -LiteralPath $dst -Directory).Count
Write-Output "Synced $count skills: $src -> $dst"
