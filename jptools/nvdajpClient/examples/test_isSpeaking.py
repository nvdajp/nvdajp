# NVDA日本語版拡張 nvdaController_isSpeaking のデモ
# Usage: python test_isSpeaking.py  (NVDA 起動後、examples/ から実行)

import time
import ctypes

from _dll_path import get_nvda_controller_client_dll_path

clientLib = ctypes.windll.LoadLibrary(get_nvda_controller_client_dll_path())
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	raise ctypes.WinError(res)
clientLib.nvdaController_speakText(
	"""This is test case.
The case nvdaController_isSpeaking beep out when speaking with nvda!
""",
)
while True:
	time.sleep(0.5)
	ctypes.windll.kernel32.Beep(500, 100)
	if not clientLib.nvdaController_isSpeaking():
		break
ctypes.windll.kernel32.Beep(1000, 100)
clientLib.nvdaController_cancelSpeech()
clientLib.nvdaController_speakText("Finished!")
