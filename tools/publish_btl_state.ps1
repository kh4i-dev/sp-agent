$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$packRoot = Join-Path $repoRoot 'docs\diagrams\btl-cnpm-state-redraw'
$projectRoot = [IO.Path]::GetFullPath('E:\HOC TAP\my-project\btl-cnpm')
$targetRoot = Join-Path $projectRoot 'private-docs'
$expected = Get-Content -LiteralPath (Join-Path $packRoot 'audit\baseline-hashes.json') -Raw | ConvertFrom-Json
foreach ($property in $expected.PSObject.Properties) {
    $filePath = Join-Path $projectRoot $property.Name
    if ((Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $property.Value) {
        throw "File changed since inspection, refusing to overwrite: $filePath"
    }
}
$backupRoot = Join-Path $targetRoot ('audit\state-redraw-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$mapping = @{
    'diagrams\state-01-don-hang.json' = 'diagrams\state-01-don-hang.json'
    'diagrams\state-01-don-hang-model.md' = 'diagrams\state-01-don-hang-model.md'
    'diagrams\state-01-don-hang-audit.md' = 'diagrams\state-01-don-hang-audit.md'
    'diagrams\state-01-don-hang.drawio' = 'diagrams\drawio\state-01-don-hang.drawio'
    'domain\step0-order-state.md' = 'domain\step0-order-state.md'
    'images\diagrams\state-01-don-hang.svg' = 'diagrams\svg\state-01-don-hang.svg'
    'images\diagrams\state-01-don-hang.png' = 'images\diagrams\state-01-don-hang.png'
    'tools\render_state_model.py' = 'tools\render_state_model.py'
    'tools\gen_state_svg.py' = 'diagrams\gen_state_svg.py'
}
function Publish-File([string]$sourcePath, [string]$relativeTarget) {
    $destinationPath = [IO.Path]::GetFullPath((Join-Path $targetRoot $relativeTarget))
    if (-not $destinationPath.StartsWith($targetRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Target outside private-docs' }
    if (Test-Path -LiteralPath $destinationPath) {
        $backupPath = Join-Path $backupRoot $relativeTarget
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($backupPath)) | Out-Null
        Copy-Item -LiteralPath $destinationPath -Destination $backupPath
    }
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($destinationPath)) | Out-Null
    Copy-Item -LiteralPath $sourcePath -Destination $destinationPath -Force
    if ((Get-FileHash -LiteralPath $sourcePath).Hash -ne (Get-FileHash -LiteralPath $destinationPath).Hash) { throw "Copy verification failed: $destinationPath" }
}
foreach ($entry in $mapping.GetEnumerator()) { Publish-File (Join-Path $packRoot $entry.Key) $entry.Value }
Publish-File (Join-Path $packRoot 'images\diagrams\state-01-don-hang.svg') 'images\diagrams\state-01-don-hang.svg'
Publish-File (Join-Path $packRoot 'images\diagrams\state-01-don-hang.png') 'images\diagrams\state-preview.png'
foreach ($entry in Get-ChildItem -LiteralPath (Join-Path $packRoot 'audit') -File -Recurse) {
    $rel = $entry.FullName.Substring((Join-Path $packRoot 'audit').Length + 1)
    Publish-File $entry.FullName ('audit\soi-so-do\state-redraw-20261101\' + $rel)
}
Write-Output "Published State SVG/PNG/drawio, model, generator and audit. Backup: $backupRoot"
