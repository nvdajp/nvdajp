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
# Create symbols.zip without external 7z dependency
$dest = Join-Path (Resolve-Path ..\output) 'symbols.zip'
if (Test-Path $dest) { Remove-Item -Force $dest }
$files = Get-ChildItem -Recurse -File -Include *.dl_,*.ex_,*.pd_ | Select-Object -ExpandProperty FullName
if ($files -and $files.Count -gt 0) {
    Compress-Archive -Path $files -DestinationPath $dest
} else {
    Write-Host "No symbol files (*.dl_, *.ex_, *.pd_) found to archive."
}
