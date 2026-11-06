param(
    [string]$ScriptPath,
    [Parameter(Mandatory = $true)][string]$FixtureRoot
)
$ErrorActionPreference = 'Stop'
if (-not $ScriptPath) { $ScriptPath = Join-Path $PSScriptRoot 'sync-skills.ps1' }
$fixture = Join-Path $FixtureRoot ('sync-regression-' + [Guid]::NewGuid().ToString('N'))
$tools = Join-Path $fixture 'tools'
$source = Join-Path $fixture '.claude/skills'
$target = Join-Path $fixture '.agents/skills'
New-Item -ItemType Directory -Path $tools,(Join-Path $source 'demo/reference/empty'),(Join-Path $source 'demo/[literal]') -Force | Out-Null
Copy-Item -LiteralPath $ScriptPath -Destination (Join-Path $tools 'sync-skills.ps1')
[IO.File]::WriteAllText((Join-Path $source 'demo/SKILL.md'), 'alpha')
[IO.File]::WriteAllText((Join-Path $source 'demo/[literal]/a b.txt'), 'nested')
[IO.File]::WriteAllBytes((Join-Path $source 'demo/empty.bin'), [byte[]]@())
function Run-Sync {
    $output = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'sync-skills.ps1') 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Sync failed: $output" }
    $output | Write-Output
}
Run-Sync
if (-not (Test-Path -LiteralPath (Join-Path $target 'demo/reference/empty'))) { throw 'Empty directory missing' }
if ((Get-Content -LiteralPath (Join-Path $target 'demo/[literal]/a b.txt') -Raw) -ne 'nested') { throw 'Literal filename mismatch' }
Write-Output 'PASS initial copy, empty file, empty directory, literal paths'
Start-Sleep -Milliseconds 700
$watcher = New-Object IO.FileSystemWatcher $target
$watcher.IncludeSubdirectories = $true
$watcher.NotifyFilter = [IO.NotifyFilters]'FileName,DirectoryName,LastWrite,Size'
$eventName = 'sync-noop-' + [Guid]::NewGuid().ToString('N')
$watchSubscription = Register-ObjectEvent $watcher Changed -SourceIdentifier $eventName
try {
    $watcher.EnableRaisingEvents = $true
    Run-Sync
    Start-Sleep -Milliseconds 500
    $writes = @(Get-Event -SourceIdentifier $eventName -ErrorAction SilentlyContinue | Where-Object { -not (Test-Path -LiteralPath $_.SourceEventArgs.FullPath -PathType Container) }).Count
    Get-Event -SourceIdentifier $eventName -ErrorAction SilentlyContinue | ForEach-Object { Write-Output ("Event: " + $_.SourceEventArgs.FullPath + " " + $_.SourceEventArgs.ChangeType) }
    if ($writes -ne 0) { throw "No-op sync rewrote files: $writes filesystem change events" }
    Write-Output 'PASS no-op produces 0 file change events'
} finally {
    $watcher.Dispose()
    Unregister-Event -SourceIdentifier $eventName
    Get-Event -SourceIdentifier $eventName -ErrorAction SilentlyContinue | Remove-Event
}
$sourceFile = Join-Path $source 'demo/SKILL.md'
$targetFile = Join-Path $target 'demo/SKILL.md'
$originalTime = (Get-Item -LiteralPath $sourceFile).LastWriteTimeUtc
[IO.File]::WriteAllText($sourceFile, 'bravo')
(Get-Item -LiteralPath $sourceFile).LastWriteTimeUtc = $originalTime
Run-Sync
if ([IO.File]::ReadAllText($targetFile) -ne 'bravo') { throw 'Same-size same-mtime content update missed' }
Write-Output 'PASS same-size same-mtime update detected by content'
[IO.File]::WriteAllText((Join-Path $target 'local-only.txt'), 'keep')
[IO.File]::WriteAllText((Join-Path $source 'demo/new.txt'), 'new')
Run-Sync
if ([IO.File]::ReadAllText((Join-Path $target 'local-only.txt')) -ne 'keep') { throw 'Local-only file lost' }
if ([IO.File]::ReadAllText((Join-Path $target 'demo/new.txt')) -ne 'new') { throw 'New file missing' }
$pending = @(Get-ChildItem -LiteralPath $target -Recurse -Filter '*.sync-tmp')
if ($pending.Count -ne 0) { throw 'Temporary files leaked' }
Write-Output 'PASS new files copied, local-only files retained, no temporary files leaked'
Write-Output "All regression checks passed. Fixture: $fixture"