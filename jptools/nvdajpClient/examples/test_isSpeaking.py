# NVDA Controller Client isSpeaking デモ
# - nvdaController_isSpeakingJp: 日本語版拡張（0引数、戻り値 1=発話中, 0=停止中）
# - nvdaController_isSpeaking: 本家 2026.3+ 標準（1引数、outパラメータ boolean*、戻り値 error_status_t）
# Usage: python test_isSpeaking.py  (NVDA 起動後、examples/ から実行)

import ctypes
import time

from _dll_path import get_nvda_controller_client_dll_path

clientLib = ctypes.windll.LoadLibrary(get_nvda_controller_client_dll_path())
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	raise ctypes.WinError(res)

print("Testing nvdaController_isSpeakingJp (0-arg)...")
clientLib.nvdaController_speakText(
	"""This is test case 1.
Testing nvdaController_isSpeakingJp zero-argument API with NVDA!
""",
)
while True:
	time.sleep(0.5)
	ctypes.windll.kernel32.Beep(500, 100)
	if not clientLib.nvdaController_isSpeakingJp():
		break
ctypes.windll.kernel32.Beep(1000, 100)
print("Test 1 completed.")

time.sleep(1.0)

print("Testing nvdaController_isSpeaking (upstream 1-arg out parameter)...")
clientLib.nvdaController_speakText(
	"""This is test case 2.
Testing standard nvdaController_isSpeaking with boolean out-parameter!
""",
)
speaking = ctypes.c_bool()
while True:
	time.sleep(0.5)
	ctypes.windll.kernel32.Beep(600, 100)
	status = clientLib.nvdaController_isSpeaking(ctypes.byref(speaking))
	if status != 0:
		raise ctypes.WinError(status)
	if not speaking.value:
		break
ctypes.windll.kernel32.Beep(1200, 100)
print("Test 2 completed.")

clientLib.nvdaController_speakText("All isSpeaking tests finished successfully!")
