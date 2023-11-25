# coding: utf-8
# 日本語版で拡張した speakSpelling を追加した DLL は 
# scons nvdaHelper\client で作成する必要があります。 
# いちおう以下の Python コードで「カタカナ ひらがな」をピッチを変えて出力できていることは確認しました。 

import time
import ctypes
DLLPATH = '../newClient/nvdaHelper/build/x86/client/nvdaControllerClient32.dll'
clientLib=ctypes.windll.LoadLibrary(DLLPATH)
res=clientLib.nvdaController_testIfRunning()
if res!=0:
	errorMessage=str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0,u"Error: %s"%errorMessage,u"Error communicating with NVDA",0)
for count in range(4):
	clientLib.nvdaController_speakSpelling(u"カタカナ ひらがな")
	time.sleep(5)
