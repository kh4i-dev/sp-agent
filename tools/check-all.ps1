$ErrorActionPreference = "Stop"

# check-all.ps1 -- chay toan bo cong kiem dinh skill: verify frontmatter + audit theo khoi.
# Tra ve exit != 0 neu co FAIL.

$tools = $PSScriptRoot
$LASTEXITCODE = 0   # PowerShell de $null; $null -ne 0 = $true -> phai khoi tao

& (Join-Path $tools "verify-skills.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& (Join-Path $tools "audit-skills.ps1")
exit $LASTEXITCODE
