# coding: utf-8
# NVDA日本語版拡張 nvdaController_getPitch / setPitch のデモ
# Usage: python test_pitchCtl.py  (NVDA 起動後、examples/ から実行)

import time
import ctypes

from _dll_path import get_nvda_controller_client_dll_path

clientLib = ctypes.windll.LoadLibrary(get_nvda_controller_client_dll_path())
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	errorMessage = str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0, "Error: %s" % errorMessage, "Error communicating with NVDA", 0)
	exit(1)
oldPitch = clientLib.nvdaController_getPitch()
clientLib.nvdaController_speakText("現在のピッチは %s です。今からピッチを変更します" % oldPitch)
time.sleep(5)
clientLib.nvdaController_setPitch(oldPitch - 50)
newPitch = clientLib.nvdaController_getPitch()
clientLib.nvdaController_speakText("ピッチを %s に変更しました。" % newPitch)
time.sleep(5)
clientLib.nvdaController_setPitch(oldPitch + 50)
newPitch = clientLib.nvdaController_getPitch()
clientLib.nvdaController_speakText("ピッチを %s に変更しました。" % newPitch)
time.sleep(5)
clientLib.nvdaController_setPitch(oldPitch)
clientLib.nvdaController_speakText("デフォルト %s に設定しました。元通りです。ほらね。" % oldPitch)
clientLib.nvdaController_speakText("作業を終了しました")
