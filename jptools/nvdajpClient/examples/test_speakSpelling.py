# coding: utf-8
# NVDA日本語版拡張 nvdaController_speakSpelling のデモ
# Usage: python test_speakSpelling.py  (NVDA 起動後、jptools/nvdajpClient/examples/ から実行)

import time
import ctypes

from _dll_path import get_nvda_controller_client_dll_path

clientLib = ctypes.windll.LoadLibrary(get_nvda_controller_client_dll_path())
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	errorMessage = str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0, "Error: %s" % errorMessage, "Error communicating with NVDA", 0)
for count in range(4):
	clientLib.nvdaController_speakSpelling("カタカナ ひらがな")
	time.sleep(5)
