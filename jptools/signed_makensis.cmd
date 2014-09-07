SET VERSION=2014.3jp
del output\nvda_%VERSION%.exe
miscDeps\tools\NSIS\makensis.exe /V2 /DVERSION=%VERSION% /DPUBLISHER="nvdajp" /DCOPYRIGHT="Copyright (C) 2006-2014 NVDA Contributors" /DNVDADistDir=C:\work\nvda\nvdajp\dist /DLAUNCHEREXE=C:\work\nvda\nvdajp\output\nvda_%VERSION%.exe launcher\nvdaLauncher.nsi