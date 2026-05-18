"""Probe USB/COM data for KGS bdDetect (standalone; no NVDA runtime).

Usage:
  py jptools/kgs_bdDetect_probe.py
"""

from __future__ import annotations

import itertools
import json
import os
import re
import subprocess
import sys
import winreg


def _out(text: str) -> None:
	enc = sys.stdout.encoding or "utf-8"
	print(text.encode(enc, errors="replace").decode(enc, errors="replace"))

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


def _serial_comm_map() -> list[dict]:
	"""Active COM mapping from HARDWARE\\DEVICEMAP\\SERIALCOMM."""
	entries: list[dict] = []
	try:
		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DEVICEMAP\SERIALCOMM") as key:
			for index in itertools.count():
				try:
					device, port, _ = winreg.EnumValue(key, index)
				except OSError:
					break
				entries.append({"device": device, "port": str(port)})
	except OSError:
		pass
	return entries


def _usb_id_from_pnp_id(pnp_id: str) -> str | None:
	if not pnp_id:
		return None
	m = re.search(r"VID_[0-9A-F]{4}&PID_[0-9A-F]{4}", pnp_id.upper())
	return m.group(0) if m else None


def _live_ports_pnp() -> list[dict]:
	"""Serial/COM devices via PowerShell (no NVDA imports)."""
	ps = (
		"$ports = @(); "
		"Get-CimInstance Win32_PnPEntity | Where-Object { $_.Caption -match '\\(COM\\d+\\)' } | "
		"ForEach-Object { "
		"$ports += [PSCustomObject]@{ "
		"Caption=$_.Caption; DeviceID=$_.DeviceID; Status=$_.Status "
		"} }; "
		"$ports | ConvertTo-Json -Compress"
	)
	try:
		out = subprocess.check_output(
			["powershell", "-NoProfile", "-Command", ps],
			text=True,
			encoding="utf-8",
			errors="replace",
			timeout=30,
		).strip()
	except (subprocess.SubprocessError, OSError) as ex:
		_out("  (PnP query failed: %s)" % ex)
		return []
	if not out or out == "null":
		return []
	data = json.loads(out)
	if isinstance(data, dict):
		data = [data]
	rows: list[dict] = []
	for item in data:
		caption = item.get("Caption") or ""
		pnp = item.get("DeviceID") or ""
		port_m = re.search(r"\(COM\d+\)", caption)
		port = port_m.group(0)[1:-1] if port_m else ""
		rows.append(
			{
				"port": port,
				"name": caption,
				"pnpDeviceID": pnp,
				"usbID": _usb_id_from_pnp_id(pnp),
				"status": item.get("Status"),
				"isBluetooth": "BTHENUM" in pnp.upper() or "BTHMODEM" in pnp.upper(),
			},
		)
	return rows


def main() -> int:
	_out("KGS bdDetect probe\n=== Registry USB -> COM (can remain after unplug) ===")
	registry_coms: dict[str, list[str]] = {}
	for vidPid in _KGS_USB_IDS:
		for e in _enum_usb_com_ports(vidPid):
			registry_coms.setdefault(e["port"], []).append(vidPid)
			_out("  registry %s -> %s" % (vidPid, e["port"]))
	if not registry_coms:
		_out("  (no KGS VID/PID in USB registry)")

	_out("\n=== Active SERIALCOMM (OS-level COM map) ===")
	serial_comm = _serial_comm_map()
	if not serial_comm:
		_out("  (none)")
	for e in serial_comm:
		_out("  %s <= %s" % (e["port"], e["device"]))

	_out("\n=== Live PnP serial (Name / usbID / Status) ===")
	live = _live_ports_pnp()
	if not live:
		_out("  (none or query failed)")
	for row in live:
		_out(
			"  {port}: usbID={usbID!r} status={status!r} name={name!r}".format(
				port=row.get("port") or "?",
				usbID=row.get("usbID"),
				status=row.get("status"),
				name=row.get("name"),
			),
		)

	_out("\n=== Interpretation (for kgs bdDetect) ===")
	for com, vid_list in sorted(registry_coms.items()):
		live_row = next((r for r in live if r.get("port") == com), None)
		if not live_row:
			_out(
				"  %s: registry lists %s but PnP has no such COM -> "
				"NVDA should SKIP (ghost after unplug)" % (com, ", ".join(vid_list)),
			)
			continue
		live_usb = live_row.get("usbID")
		for vid in vid_list:
			if live_usb == vid:
				_out("  %s: live usbID matches %s -> USB scan may try this port" % (com, vid))
			else:
				_out(
					"  %s: registry %s but live usbID=%r -> NVDA should SKIP (BT/other device)"
					% (com, vid, live_usb),
				)

	_out("\n=== Bluetooth (from SERIALCOMM - try in NVDA manual port) ===")
	for e in serial_comm:
		if "BthModem" in e["device"] or "BTH" in e["device"].upper():
			_out("  %s  (device path: %s)" % (e["port"], e["device"]))

	bt_rows = [r for r in live if r.get("isBluetooth")]
	if bt_rows:
		_out("\n=== Bluetooth PnP detail ===")
		for row in bt_rows:
			_out(
				"  {port}: {name} [{status}]".format(
					port=row.get("port"),
					name=row.get("name"),
					status=row.get("status"),
				),
			)

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
