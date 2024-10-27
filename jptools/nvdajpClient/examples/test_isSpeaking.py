# coding: utf-8
import time
import ctypes

DLLPATH = r"..\client\nvdaControllerClient32.dll"
clientLib = ctypes.windll.LoadLibrary(DLLPATH)
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	raise ctypes.WinError(res)
clientLib.nvdaController_speakText(
	"""This is test case.
The case nvdaController_isSpeaking beep out when speaking with nvda!
"""
)
while True:
	time.sleep(0.5)
	ctypes.windll.kernel32.Beep(500, 100)
	if not clientLib.nvdaController_isSpeaking():
		break
ctypes.windll.kernel32.Beep(1000, 100)
clientLib.nvdaController_cancelSpeech()
clientLib.nvdaController_speakText("Finished!")
