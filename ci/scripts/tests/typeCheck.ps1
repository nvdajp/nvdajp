# Stop Pyright warning us that we're not running the latest version
$env:PYRIGHT_PYTHON_IGNORE_WARNINGS="1"
$pyrightOutput = (uv run pyright) -Join "`n"
if ($LASTEXITCODE -ne 0) {
	Write-Output @"
FAIL: Static type analysis. Pyright exited with exit code $LASTEXITCODE.
<details>
<summary>Type analysis errors</summary>

``````
$pyrightOutput
``````

</details>

"@ >> $env:GITHUB_STEP_SUMMARY
}
exit $LASTEXITCODE
