$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$skillsDir = Join-Path $root ".claude\skills"

if (-not (Test-Path -LiteralPath $skillsDir)) {
    throw "Khong tim thay: $skillsDir"
}

$problems = 0
$dirs = Get-ChildItem -LiteralPath $skillsDir -Directory

foreach ($dir in $dirs) {
    $skillFile = Join-Path $dir.FullName "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile)) {
        Write-Output "FAIL  $($dir.Name): thieu SKILL.md"
        $problems++
        continue
    }

    $content = Get-Content -LiteralPath $skillFile -Raw
    if (-not $content.StartsWith("---")) {
        Write-Output "FAIL  $($dir.Name): thieu YAML frontmatter"
        $problems++
        continue
    }

    $nameMatch = [regex]::Match($content, "(?m)^name:\s*(.+)$")
    $descMatch = [regex]::Match($content, "(?m)^description:\s*(.+)$")

    if (-not $nameMatch.Success) {
        Write-Output "FAIL  $($dir.Name): thieu 'name'"
        $problems++
        continue
    }
    if (-not $descMatch.Success) {
        Write-Output "FAIL  $($dir.Name): thieu 'description'"
        $problems++
        continue
    }

    $name = $nameMatch.Groups[1].Value.Trim()
    $desc = $descMatch.Groups[1].Value.Trim()

    if ($name -ne $dir.Name) {
        Write-Output "FAIL  $($dir.Name): name '$name' khong khop ten thu muc"
        $problems++
        continue
    }
    if ($name -notmatch "^[a-z0-9]+(-[a-z0-9]+)*$") {
        Write-Output "FAIL  $($dir.Name): name sai dinh dang (lowercase + hyphen)"
        $problems++
        continue
    }
    if ($name.Length -gt 64) {
        Write-Output "FAIL  $($dir.Name): name > 64 ky tu"
        $problems++
        continue
    }
    if ($desc.Length -gt 1024) {
        Write-Output "WARN  $($dir.Name): description > 1024 ky tu ($($desc.Length))"
    }

    Write-Output "OK    $($dir.Name)  (desc $($desc.Length) ky tu)"
}

Write-Output ""
if ($problems -eq 0) {
    Write-Output "Tat ca skill hop le: $($dirs.Count) skill."
} else {
    Write-Output "Co $problems loi can sua."
    exit 1
}
