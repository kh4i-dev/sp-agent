param(
    [string]$Block = "",
    [switch]$Json
)
$ErrorActionPreference = "Stop"

$root   = Split-Path -Parent $PSScriptRoot
$cDir   = Join-Path $root ".claude\skills"
$aDir   = Join-Path $root ".agents\skills"
$bt     = [char]96   # backtick

if (-not (Test-Path -LiteralPath $cDir)) { throw "Khong thay: $cDir" }

$findings = @{}   # skill -> list of "FAIL|WARN  message"
function Add-Finding($skill, $level, $msg) {
    if (-not $findings.ContainsKey($skill)) { $findings[$skill] = New-Object System.Collections.ArrayList }
    [void]$findings[$skill].Add("$level $msg")
}
$globalFindings = New-Object System.Collections.ArrayList

$skillNames = @((Get-ChildItem -LiteralPath $cDir -Directory).Name | Sort-Object)

# ---------- 1. Parse block -> members from coord-*/SKILL.md (nguon SSOT) ----------
$blocks = [ordered]@{}
foreach ($n in $skillNames) {
    if ($n -notlike "coord-*") { continue }
    $f = Join-Path (Join-Path $cDir $n) "SKILL.md"
    if (-not (Test-Path -LiteralPath $f)) { continue }
    $c = Get-Content -LiteralPath $f -Raw -Encoding UTF8
    $members = New-Object System.Collections.ArrayList
    foreach ($ln in (Get-Content -LiteralPath $f -Encoding UTF8)) {
        $row = [regex]::Match($ln, "^\s*\|\s*${bt}([a-z0-9][a-z0-9-]*)${bt}")
        if (-not $row.Success) { continue }
        $nm = $row.Groups[1].Value
        if (($skillNames -contains $nm) -and -not $members.Contains($nm)) { [void]$members.Add($nm) }
    }
    $blocks[$n] = $members
}
$assigned = @{}
foreach ($k in $blocks.Keys) { foreach ($m in $blocks[$k]) { $assigned[$m] = $true } }

# ---------- 2. Kiem tra tung skill ----------
foreach ($n in $skillNames) {
    $dir = Join-Path $cDir $n
    $skillFile = Join-Path $dir "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile)) { Add-Finding $n "FAIL" "thieu SKILL.md"; continue }

    $content = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8

    if (-not $content.TrimStart().StartsWith("---")) { Add-Finding $n "FAIL" "thieu YAML frontmatter"; continue }

    $nm = [regex]::Match($content, "(?m)^name:\s*(\S+)")
    if (-not $nm.Success) { Add-Finding $n "FAIL" "thieu 'name'" }
    elseif ($nm.Groups[1].Value -ne $n) { Add-Finding $n "FAIL" "name '$($nm.Groups[1].Value)' khong khop ten thu muc" }

    # description (ho tro YAML multiline '>' / '|')
    $dm = [regex]::Match($content, "(?m)^description:\s*(.*)$")
    $desc = ""
    if ($dm.Success) {
        $val = $dm.Groups[1].Value.Trim()
        if ($val -eq ">" -or $val -eq "|" -or $val -eq "") {
            $rest = $content.Substring($dm.Index + $dm.Length)
            $buf = @()
            foreach ($ln in ($rest -split "\r?\n")) {
                if ($ln -match "^\s+\S") { $buf += $ln.Trim() }
                elseif ($ln.Trim() -eq "") { continue }
                else { break }
            }
            $desc = ($buf -join " ")
        } else { $desc = $val }
    }
    if ([string]::IsNullOrWhiteSpace($desc)) { Add-Finding $n "FAIL" "thieu 'description'" }
    elseif ($desc.Length -gt 1024) { Add-Finding $n "WARN" "description > 1024 ($($desc.Length))" }
    elseif ($desc.Length -lt 40)  { Add-Finding $n "WARN" "description qua ngan ($($desc.Length)) -> thieu tu khoa kich hoat?" }

    # do dai SKILL.md
    $lc = (Get-Content -LiteralPath $skillFile -Encoding UTF8).Count
    if ($lc -gt 500) { Add-Finding $n "WARN" "SKILL.md $lc dong (>500 -> nen tach reference/)" }

    # mojibake (UTF-8 bi doc sai)
    if ($content -match "\u00C3[\u0080-\u00BF]|\u00E2\u20AC\u0099|\u00E2\u0080") {
        Add-Finding $n "FAIL" "nghi mojibake (UTF-8 doc sai / ky tu rac)"
    }

    # link markdown noi bo trong SKILL.md (bo qua placeholder/minh hoa)
    foreach ($lm in [regex]::Matches($content, "\[[^\]]*\]\(([^)]+)\)")) {
        $tgt = $lm.Groups[1].Value.Trim().Split("#")[0]
        if ($tgt -match "^(https?:|mailto:|tel:|file:|data:)" -or $tgt -eq "") { continue }
        if ($tgt -match '[<>|"?*]|path[\\/]to|^path$|relative-url|does-not-exist|subdir|NNNN|\{\{|\.\.\.') { continue }
        $rel = [uri]::UnescapeDataString($tgt).Replace("/", "\")
        $abs = Join-Path $dir $rel
        try { $exists = Test-Path -LiteralPath $abs } catch { $exists = $true }
        if (-not $exists) { Add-Finding $n "WARN" "link hong: '$tgt'" }
    }

    # coordinator phai co Definition of Done; chi report/diagrams/slides bat buoc co cong (gate)
    if ($n -like "coord-*") {
        if ($content -notmatch "(?i)Definition of Done") { Add-Finding $n "WARN" "coordinator thieu muc 'Definition of Done'" }
        if (($n -in @("coord-report","coord-diagrams","coord-slides")) -and ($content -notmatch "(?i)\bgate\b|C\u1ed5ng")) {
            Add-Finding $n "WARN" "coordinator thieu muc cong (gate)"
        }
    }

    # invariant theo khoi (WARN)
    if (@("plantuml-diagrams","tldraw-diagrams","simplified-diagrams","use-case-layout","diagram-orchestrator","diagram-auditor") -contains $n) {
        if ($content -notmatch "(?i)zero-color|zero color|tr\u1eafng") { Add-Finding $n "WARN" "thieu quy uoc zero-color / trang-den" }
    }
    if (@("docx-report","human-report-writing") -contains $n) {
        if ($content -notmatch "(?i)em dash|em-dash") { Add-Finding $n "WARN" "thieu luat cam em dash" }
    }
}

# ---------- 3. Mirror parity .claude <-> .agents ----------
if (Test-Path -LiteralPath $aDir) {
    $cFiles = Get-ChildItem -LiteralPath $cDir -Recurse -File | Where-Object { $_.FullName -notmatch "__pycache__" }
    foreach ($f in $cFiles) {
        $rel = $f.FullName.Substring($cDir.Length + 1)
        $b = Join-Path $aDir $rel
        if (-not (Test-Path -LiteralPath $b)) { [void]$globalFindings.Add("FAIL  mirror: thieu o .agents -> $rel") }
        elseif ((Get-FileHash -LiteralPath $f.FullName).Hash -ne (Get-FileHash -LiteralPath $b).Hash) {
            [void]$globalFindings.Add("FAIL  mirror: lech noi dung -> $rel")
        }
    }
    foreach ($f in (Get-ChildItem -LiteralPath $aDir -Recurse -File | Where-Object { $_.FullName -notmatch "__pycache__" })) {
        $rel = $f.FullName.Substring($aDir.Length + 1)
        if (-not (Test-Path -LiteralPath (Join-Path $cDir $rel))) { [void]$globalFindings.Add("WARN  mirror: thua o .agents -> $rel") }
    }
} else { [void]$globalFindings.Add("WARN  khong thay .agents\skills de doi chieu mirror") }

# ---------- 3b. Drift: bang block trong AGENTS.md vs bang trong coord-* ----------
$agentsPath = Join-Path $root "AGENTS.md"
if (Test-Path -LiteralPath $agentsPath) {
    $ag = Get-Content -LiteralPath $agentsPath -Raw -Encoding UTF8
    foreach ($k in $blocks.Keys) {
        $m = [regex]::Match($ag, "(?m)^\|\s*[^|]*\|\s*${bt}$([regex]::Escape($k))${bt}\s*\|\s*([^|]*)\|")
        if (-not $m.Success) { [void]$globalFindings.Add("WARN  drift: AGENTS.md thieu khoi '$k'"); continue }
        $listed = @($m.Groups[1].Value -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ -match "^[a-z0-9-]+$" } | Sort-Object -Unique)
        $actual = @($blocks[$k] | Sort-Object -Unique)
        if (($listed -join ",") -ne ($actual -join ",")) {
            [void]$globalFindings.Add("WARN  drift $k : AGENTS[$($listed -join ',')] != coord[$($actual -join ',')]")
        }
    }
}

# ---------- 4. Tinh toan & in ----------
$allFail = 0; $allWarn = 0
foreach ($k in $findings.Keys) { foreach ($x in $findings[$k]) { if ($x.StartsWith("FAIL")) { $allFail++ } else { $allWarn++ } } }
foreach ($x in $globalFindings) { if ($x.StartsWith("FAIL")) { $allFail++ } else { $allWarn++ } }

if ($Json) {
    $out = [ordered]@{ blocks = @{}; findings = $findings; global = $globalFindings; fail = $allFail; warn = $allWarn }
    foreach ($k in $blocks.Keys) { $out.blocks[$k] = @($blocks[$k]) }
    $out | ConvertTo-Json -Depth 5
    exit $(if ($allFail -gt 0) { 1 } else { 0 })
}

Write-Output "================ AUDIT SKILLS THEO KHOI ================"
foreach ($k in $blocks.Keys) {
    if ($Block -and $k -ne $Block) { continue }
    Write-Output ""
    Write-Output ("### {0}  ({1} thanh vien)" -f $k, $blocks[$k].Count)
    foreach ($m in $blocks[$k]) {
        $fl = if ($findings.ContainsKey($m)) { $findings[$m] } else { @() }
        $tag = if ($fl.Count -eq 0) { "[ok]" } else { "[$($fl.Count)]" }
        Write-Output ("  - {0} {1}" -f $m, $tag)
        foreach ($x in $fl) { Write-Output ("      $x") }
    }
}

# skill ngoai block (meta / chua gan)
$unassigned = $skillNames | Where-Object { -not $assigned[$_] }
Write-Output ""
Write-Output "### Khong thuoc khoi nao (meta / chua gan)"
foreach ($m in $unassigned) {
    $fl = if ($findings.ContainsKey($m)) { $findings[$m] } else { @() }
    $tag = if ($fl.Count -eq 0) { "[ok]" } else { "[$($fl.Count)]" }
    Write-Output ("  - {0} {1}" -f $m, $tag)
    foreach ($x in $fl) { Write-Output ("      $x") }
}

if ($globalFindings.Count -gt 0) {
    Write-Output ""
    Write-Output "### GLOBAL (mirror / cau truc)"
    foreach ($x in $globalFindings) { Write-Output ("  $x") }
}

Write-Output ""
Write-Output ("================ KET QUA: {0} FAIL, {1} WARN ================" -f $allFail, $allWarn)
if ($allFail -gt 0) { exit 1 } else { exit 0 }
