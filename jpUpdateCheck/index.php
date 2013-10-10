<?php 
define("LATEST_VERSION", "jpnext131010");
define("LATEST_LAUNCHER", "https://dl.dropboxusercontent.com/u/62564469/nvda_jpnext131010.exe");
$version = '';
if (isset($_GET['version'])) {
	$version = $_GET['version'];
}
header('Content-type: text/plain');
if ($version === '' || $version === LATEST_VERSION) {
	exit();
}
echo "version: " . LATEST_VERSION . PHP_EOL;
echo "launcherUrl: " . LATEST_LAUNCHER . PHP_EOL;
