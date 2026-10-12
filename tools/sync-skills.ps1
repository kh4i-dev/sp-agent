$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$src = Join-Path $root ".claude\skills"
$dst = Join-Path $root ".agents\skills"

if (-not (Test-Path -LiteralPath $src)) {
    throw "Khong tim thay thu muc nguon: $src"
}

if (-not (Test-Path -LiteralPath $dst)) {
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
}

$dirs = Get-ChildItem -LiteralPath $src -Directory
foreach ($d in $dirs) {
    $targetDir = Join-Path $dst $d.Name
    if (-not (Test-Path -LiteralPath $targetDir)) {
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }
    Copy-Item -Path (Join-Path $d.FullName "*") -Destination $targetDir -Recurse -Force
}

$count = (Get-ChildItem -LiteralPath $dst -Directory).Count
Write-Output "Synced $count skills: $src -> $dst"
