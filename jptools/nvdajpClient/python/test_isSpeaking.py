# coding: utf-8
import time
import ctypes
DLLPATH = '../newclient/nvdaHelper/build/x86/client/nvdaControllerClient32.dll'
clientLib=ctypes.windll.LoadLibrary(DLLPATH)
res=clientLib.nvdaController_testIfRunning()
if res!=0:
	errorMessage=str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0,u"Error: %s"%errorMessage,u"Error communicating with NVDA",0)
	exit(1)
clientLib.nvdaController_speakText(
u"This is test case.\n \
The case nvdaController_isSpeaking beep out when speaking with nvda! \
")
while ( True ):
	time.sleep(0.5)
	ctypes.windll.user32.MessageBeep(0)
	if not clientLib.nvdaController_isSpeaking():
		break
ctypes.windll.user32.MessageBeep(1)
clientLib.nvdaController_cancelSpeech()
clientLib.nvdaController_speakText(u"Finished!")
