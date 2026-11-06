$files = @(
    "02-phan-ra-chuc-nang",
    "03-use-case",
    "03b-use-case-van-hanh",
    "04-seq-dat-hang",
    "05-seq-dong-goi-qr",
    "06-seq-giao-hang",
    "07-seq-giai-ngan",
    "08-seq-nap-tien",
    "09-seq-khieu-nai",
    "10-state-don-hang",
    "11-class-don-hang",
    "11b-class-tien-ho-tro",
    "12-erd-giao-dich",
    "12b-erd-van-hanh",
    "13-kho-hub",
    "14-cau-tao-qr",
    "15-seq-cskh",
    "16-seq-bao-cao"
)

$base = "E:\HOC TAP\my-project\btl-cnpm\private-docs\diagrams\puml"

foreach ($f in $files) {
    $in = "$base\$f.puml"
    Write-Host "Rendering $f..."
    $result = node render-puml.mjs --in "$in" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed $f"
    }
}