# jptools/test_controller_speakSpelling.py
# Reproduction script for nvdajp/nvdajp issue #642:
#   nvdaController_speakSpelling を利用するとNVDAがクラッシュする
#
# Usage:
#   1. Build NVDA: scons source
#   2. Start NVDA: runnvda.bat
#   3. Run: python jptools/test_controller_speakSpelling.py
#      Or:  python jptools/test_controller_speakSpelling.py path\to\nvdaControllerClient.dll
#
# Before fix: NVDA crashes when nvdaController_speakSpelling is called.
# After fix: NVDA speaks the given text in spelling mode and does not crash.

import ctypes
import os
import sys


def _default_dll_path() -> str:
	"""Python のアーキテクチャに応じて extras/controllerClient のパスを返す。"""
	repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	arch = "x64" if sys.maxsize > 2**32 else "x86"
	return os.path.join(
		repo_root,
		"extras",
		"controllerClient",
		arch,
		"nvdaControllerClient.dll",
	)


def main() -> int:
	if len(sys.argv) >= 2:
		dll_path = os.path.abspath(sys.argv[1])
	else:
		dll_path = _default_dll_path()
		if not os.path.isfile(dll_path):
			dll_path = "nvdaControllerClient.dll"

	if not os.path.isfile(dll_path):
		default_path = _default_dll_path()
		print("Error: nvdaControllerClient.dll not found.", file=sys.stderr)
		print(f"  Tried: {dll_path}", file=sys.stderr)
		print(f"  Expected (for this Python): {default_path}", file=sys.stderr)
		print("  Run: scons source", file=sys.stderr)
		print(
			"  Usage: python test_controller_speakSpelling.py [path_to_nvdaControllerClient.dll]",
			file=sys.stderr,
		)
		return 1

	try:
		client_lib = ctypes.windll.LoadLibrary(dll_path)
	except OSError as e:
		print(f"Error loading DLL: {e}", file=sys.stderr)
		return 1

	res = client_lib.nvdaController_testIfRunning()
	if res != 0:
		err = ctypes.WinError(res)
		print(f"nvdaController_testIfRunning failed: {err}", file=sys.stderr)
		return 1

	print("Calling nvdaController_speakSpelling('a')...")
	res = client_lib.nvdaController_speakSpelling("a")
	if res != 0:
		err = ctypes.WinError(res)
		print(f"nvdaController_speakSpelling returned: {res} ({err})", file=sys.stderr)
		return 1

	print("OK. NVDA should have spoken 'a' in spelling mode. (Issue #642 fix verified.)")
	return 0


if __name__ == "__main__":
	sys.exit(main())
