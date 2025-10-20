$ErrorActionPreference = "Stop";

foreach ($syms in
	# We don't just include source\*.dll because that would include system dlls.
	"source\liblouis.dll",
	"source\*.pdb",
	"source\lib\*.dll",
	"source\lib\*.pdb",
	# We include source\lib64\*.exe to cover nvdaHelperRemoteLoader.
	"source\lib64\*.dll",
	"source\lib64\*.exe",
	"source\lib64\*.pdb",
	"source\synthDrivers\*.dll",
	"source\synthDrivers\*.pdb"
) {
	# https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/symstore-command-line-options
	& $env:symStore add /f $syms /s symbols /t NVDA /compress
}

Set-Location symbols
# Use built-in Compress-Archive to avoid external 7-Zip dependency
$outputZip = Join-Path (Resolve-Path ..\output) symbols.zip
if (Test-Path $outputZip) {
    Remove-Item $outputZip -Force
}

$files = Get-ChildItem -Recurse -Include *.dl_, *.ex_, *.pd_ -File
if (-not $files) {
    Write-Host "No compressed symbol files found (*.dl_, *.ex_, *.pd_)"
} else {
    $files | Compress-Archive -DestinationPath $outputZip -Force
    Write-Host "Created symbols archive: $outputZip"
}
