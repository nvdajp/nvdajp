# coding: utf-8
# NVDA日本語版拡張 nvdaController_getRate / setRate のデモ
# Usage: python test_rateCtl.py  (NVDA 起動後、examples/ から実行)

import time
import ctypes

from _dll_path import get_nvda_controller_client_dll_path

clientLib = ctypes.windll.LoadLibrary(get_nvda_controller_client_dll_path())
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	errorMessage = str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0, "Error: %s" % errorMessage, "Error communicating with NVDA", 0)
	exit(1)
oldRate = clientLib.nvdaController_getRate()
clientLib.nvdaController_speakText("現在の速さは %s です。今から速さを変更します" % oldRate)
time.sleep(5)
clientLib.nvdaController_setRate(oldRate - 50)
newRate = clientLib.nvdaController_getRate()
clientLib.nvdaController_speakText("速さを %s に変更しました。" % newRate)
time.sleep(5)
clientLib.nvdaController_setRate(oldRate + 50)
newRate = clientLib.nvdaController_getRate()
clientLib.nvdaController_speakText("速さを %s に変更しました。" % newRate)
time.sleep(5)
clientLib.nvdaController_setRate(oldRate)
clientLib.nvdaController_speakText("デフォルト %s に設定しました。元通りです。ほらね。" % oldRate)
clientLib.nvdaController_speakText("作業を終了しました")
