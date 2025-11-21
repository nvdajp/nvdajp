$outDir = (Resolve-Path .\testOutput\unit\)
$unitTestsXml = "$outDir\unitTests.xml"

# Print a brief braille environment diagnostic to aid debugging
try {
    uv run python ci/scripts/tests/diagBrailleEnv.py
} catch {
    Write-Output "[diag] skipped: $_"
}

.\rununittests.bat --output-file "$unitTestsXml" -v
if ($LastExitCode -ne 0) {
	Write-Output "FAIL: Unit tests. See test results for more information." >> $env:GITHUB_STEP_SUMMARY
	Write-Output "testFailExitCode=$LastExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}
exit $LastExitCode
