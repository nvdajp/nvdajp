# coding: utf-8
import time
import ctypes

DLLPATH = "../newclient/nvdaHelper/build/x86/client/nvdaControllerClient32.dll"
clientLib = ctypes.windll.LoadLibrary(DLLPATH)
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
