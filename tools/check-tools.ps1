$ErrorActionPreference = "SilentlyContinue"

function Test-Tool($name, $path) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) {
        return [pscustomobject]@{ Tool = $name; Status = "OK"; Where = $cmd.Source }
    }
    if ($path) {
        foreach ($p in $path) {
            if (Test-Path -LiteralPath $p) {
                return [pscustomobject]@{ Tool = $name; Status = "OK"; Where = $p }
            }
        }
    }
    return [pscustomobject]@{ Tool = $name; Status = "MISSING"; Where = "" }
}

$sofficePaths = @(
    "C:\Program Files\LibreOffice\program\soffice.exe",
    "C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice"
)

$results = @()
$results += Test-Tool "python" $null
$results += Test-Tool "node" $null
$results += Test-Tool "npm" $null
$results += Test-Tool "npx" $null
$results += Test-Tool "git" $null
$results += Test-Tool "soffice" $sofficePaths
$results += Test-Tool "pandoc" $null
$results += Test-Tool "pdftoppm" $null

$results | Format-Table -AutoSize

Write-Output ""
Write-Output "Goi y cai dat (neu MISSING):"
Write-Output "  LibreOffice : winget install TheDocumentFoundation.LibreOffice"
Write-Output "  pandoc      : winget install JohnMacFarlane.Pandoc"
Write-Output "  Python pkgs : pip install python-docx python-pptx openpyxl xlsxwriter pandas pymupdf pdfplumber pypdf reportlab"
Write-Output "  PlantUML    : Render truc tiep qua Kroki (scripts/render-puml.mjs) hoac Java + plantuml.jar"
