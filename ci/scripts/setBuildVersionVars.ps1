$ErrorActionPreference = "Stop";

$pythonVersion = (py --version)
Write-Output $pythonVersion
if ($env:GITHUB_REF_TYPE -eq "tag" -and $env:GITHUB_REF_NAME.StartsWith("release-")) {
	# Strip "release-" prefix.
	$version = $env:GITHUB_REF_NAME.Substring(8)
	$release = 1
	Write-Output "release=1" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
	if ($env:GITHUB_REF_TYPE -eq "tag" -and ($env:GITHUB_REF_NAME.Contains("rc") -or $env:GITHUB_REF_NAME.Contains("beta"))) {
		$versionType = "beta"
	} else {
		$versionType = "stable"
	}
} else {
	$commitVersion = $env:GITHUB_SHA.Substring(0, 8)
	$BUILD_NUMBER = [int]$env:GITHUB_RUN_NUMBER + [int]$env:START_BUILD_NUMBER
	if ([int]$env:pullRequestNumber) {
		$version = "pr$env:pullRequestNumber-$BUILD_NUMBER,$commitVersion"
	} elseif ($env:GITHUB_REF_NAME -eq "master") {
		$version = "alpha-$BUILD_NUMBER,$commitVersion"
	} elseif ($env:GITHUB_REF_NAME -eq "alphajp" -and $env:GITHUB_EVENT_NAME -eq "workflow_dispatch") {
		# BEGIN JP PATCH (alphajp workflow_dispatch release: align with local build versioning)
		# Use nowdate computed once in the matrix job if available; otherwise compute it here.
		if ($env:NOWDATE) {
			$nowdate = $env:NOWDATE
		} else {
			$jstNow = (Get-Date).ToUniversalTime().AddHours(9)
			$nowdate = $jstNow.ToString("yyMMdd") + [char]($jstNow.Hour + 97)
		}
		$version = "jpalpha_$nowdate"
		$versionType = "nvdajpalpha"
		$release = 1
		Write-Output "release=1" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
		Write-Output "nowdate=$nowdate" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
		# END JP PATCH
	} else {
		$version = "$env:GITHUB_REF_NAME-$BUILD_NUMBER,$commitVersion"
		# BEGIN JP PATCH (betajp: use nowdate-based version like 2026.2jp-beta-260720a)
		if ($env:GITHUB_REF_NAME -eq "betajp" -and $env:NOWDATE) {
			$version = "2026.2jp-beta-$env:NOWDATE"
			$release = 1
			$versionType = "nvdajpbeta"
			Write-Output "release=1" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
		}
		# END JP PATCH
		if ($env:GITHUB_REF_NAME.StartsWith("try-release-")) {
			Write-Output "release=1" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
		}
	}
}
if (!$release) {
	if ($env:GITHUB_REF_NAME -eq "master") {
		$versionType = "snapshot:alpha"
	} elseif (!$env:GITHUB_REF_NAME.StartsWith("try-") -and ![int]$env:pullRequestNumber) {
		$versionType = "snapshot:$env:GITHUB_REF_NAME"
	}
}
Write-Output "version=$version" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
if ($versionType) {
	Write-Output "versionType=$versionType" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}
