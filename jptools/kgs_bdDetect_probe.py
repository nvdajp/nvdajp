"""Probe USB/COM data for KGS bdDetect (standalone; no NVDA runtime).

Usage (Next Touch 40 connected via USB):
  py jptools/kgs_bdDetect_probe.py

Optional: run from betajp root with NVDA dev env to also test kgs._cp210xUsbIdMatch:
  py jptools/kgs_bdDetect_probe.py --with-kgs
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys
import winreg

_KGS_USB_IDS = (
	"VID_1148&PID_0301",
	"VID_1148&PID_0001",
	"VID_10C4&PID_EA60",
)


def _enum_usb_com_ports(vidPid: str) -> list[dict]:
	ports: list[dict] = []
	try:
		rootKey = winreg.OpenKey(
			winreg.HKEY_LOCAL_MACHINE,
			r"SYSTEM\CurrentControlSet\Enum\USB\%s" % vidPid,
		)
	except OSError:
		return ports
	with rootKey:
		for index in itertools.count():
			try:
				keyName = winreg.EnumKey(rootKey, index)
			except OSError:
				break
			try:
				with winreg.OpenKey(rootKey, os.path.join(keyName, "Device Parameters")) as paramsKey:
					portName = winreg.QueryValueEx(paramsKey, "PortName")[0]
					ports.append({"port": str(portName), "vidPid": vidPid})
			except OSError:
				continue
	return ports


def _cp210x_match_text(text: str) -> bool:
	text = text.lower()
	kgsHints = (
		"kgs",
		"braille memo",
		"braillememo",
		"next touch",
		"bm-smart",
		"bmsmart",
		"bm smart",
		"bm_disp",
		"bm-nexttouch",
	)
	if any(h in text for h in kgsHints):
		return True
	return "cp210" in text or "silicon labs" in text


def main() -> int:
	parser = argparse.ArgumentParser(description="Probe KGS USB/COM for bdDetect")
	parser.add_argument(
		"--with-kgs",
		action="store_true",
		help="Import kgs module (requires NVDA Python deps on PYTHONPATH)",
	)
	args = parser.parse_args()

	print("KGS bdDetect probe\n=== Registry USB -> COM ===")
	found = False
	for vidPid in _KGS_USB_IDS:
		entries = _enum_usb_com_ports(vidPid)
		if entries:
			found = True
		for e in entries:
			print("  %s -> %s" % (vidPid, e["port"]))
	if not found:
		print("  (no KGS VID/PID in USB enum — display off or different USB chip?)")

	if args.with_kgs:
		print("\n=== kgs._cp210xUsbIdMatch ===")
		repo = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
		sys.path.insert(0, os.path.join(repo, "source"))
		try:
			from brailleDisplayDrivers import kgs
			import bdDetect

			for e in _enum_usb_com_ports("VID_10C4&PID_EA60"):
				match = bdDetect.DeviceMatch(
					bdDetect.ProtocolType.SERIAL,
					"VID_10C4&PID_EA60",
					e["port"],
					{"port": e["port"], "friendlyName": "", "hardwareID": "USB\\VID_10C4&PID_EA60"},
				)
				print("  %s: %s" % (e["port"], kgs._cp210xUsbIdMatch(match)))
		except Exception as ex:
			print("  failed: %s" % ex)

	print(
		"\nNext Touch 40 USB is expected as VID_10C4&PID_EA60 (CP210x)."
		"\nIn NVDA: debug bdDetect on, driver kgs, port automatic."
	)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
