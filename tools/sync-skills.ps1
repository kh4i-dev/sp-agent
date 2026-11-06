$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$src = Join-Path $root '.claude\skills'
$dst = Join-Path $root '.agents\skills'

if (-not (Test-Path -LiteralPath $src -PathType Container)) {
    throw "Khong tim thay thu muc nguon: $src"
}

# Khong di theo junction/symlink ra ngoai hai cay skill.
$sourceEntries = @(Get-ChildItem -LiteralPath $src -Recurse -Force)
$targetEntries = @()
if (Test-Path -LiteralPath $dst) {
    $targetEntries = @(Get-ChildItem -LiteralPath $dst -Recurse -Force)
}
foreach ($entry in @((Get-Item -LiteralPath $src)) + $sourceEntries + $targetEntries) {
    if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "Khong sync qua symlink/junction: $($entry.FullName)"
    }
}
if (Test-Path -LiteralPath $dst) {
    if (((Get-Item -LiteralPath $dst).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "Khong sync qua symlink/junction: $dst"
    }
} else {
    New-Item -ItemType Directory -Path $dst | Out-Null
}

$copied = 0
$unchanged = 0
foreach ($entry in $sourceEntries) {
    $relative = $entry.FullName.Substring($src.Length + 1)
    $target = Join-Path $dst $relative
    if ($entry.PSIsContainer) {
        if (-not (Test-Path -LiteralPath $target -PathType Container)) {
            [IO.Directory]::CreateDirectory($target) | Out-Null
        }
        continue
    }

    $sourceHash = (Get-FileHash -LiteralPath $entry.FullName -Algorithm SHA256).Hash
    if (Test-Path -LiteralPath $target -PathType Leaf) {
        $targetInfo = Get-Item -LiteralPath $target
        if ($entry.Length -eq $targetInfo.Length -and
            $sourceHash -eq (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash) {
            $unchanged++
            continue
        }
    }

    # Chi publish file hoan chinh; khong de watcher doc file dang copy do.
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
    $temporary = $target + '.' + [Guid]::NewGuid().ToString('N') + '.sync-tmp'
    try {
        Copy-Item -LiteralPath $entry.FullName -Destination $temporary
        if ((Get-FileHash -LiteralPath $temporary -Algorithm SHA256).Hash -ne $sourceHash) {
            throw "Nguon thay doi trong luc sync, hay chay lai: $($entry.FullName)"
        }
        if (Test-Path -LiteralPath $target -PathType Leaf) {
            [IO.File]::Replace($temporary, $target, [System.Management.Automation.Language.NullString]::Value)
        } else {
            [IO.File]::Move($temporary, $target)
        }
        $copied++
    } finally {
        if (Test-Path -LiteralPath $temporary) {
            Remove-Item -LiteralPath $temporary -Force
        }
    }
}

$count = @(Get-ChildItem -LiteralPath $src -Directory).Count
Write-Output "Synced $count skills: copied=$copied unchanged=$unchanged; $src -> $dst"