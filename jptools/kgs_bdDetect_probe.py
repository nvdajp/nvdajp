"""Probe USB/COM data for KGS bdDetect (standalone; no NVDA runtime).

Usage:
  py jptools/kgs_bdDetect_probe.py
  py jptools/kgs_bdDetect_probe.py --encoding mbcs
  py jptools/kgs_bdDetect_probe.py --encoding auto

Encoding:
  Japanese Windows consoles often use the system ANSI code page (MBCS, typically cp932).
  PowerShell may emit UTF-8 or MBCS depending on version and settings. Use --encoding
  mbcs if device names look garbled with the default, or set KGS_PROBE_ENCODING=mbcs.
"""

from __future__ import annotations

import argparse
import itertools
import json
import locale
import os
import re
import subprocess
import sys
import winreg

_ENCODING_CHOICES = ("auto", "utf-8", "mbcs")
_OUTPUT_ENCODING: str = "utf-8"
_SUBPROCESS_DECODINGS: list[str] = ["utf-8-sig", "utf-8", "mbcs"]


def _encoding_candidates() -> list[str]:
	"""Build an ordered list of encodings to try for subprocess output."""
	candidates: list[str] = []
	if override := os.environ.get("KGS_PROBE_ENCODING"):
		candidates.append(override.strip())
	if _OUTPUT_ENCODING not in ("auto",):
		candidates.append(_OUTPUT_ENCODING)
	if sys.stdout.encoding:
		candidates.append(sys.stdout.encoding)
	try:
		candidates.append(locale.getencoding())
	except AttributeError:
		candidates.append(locale.getpreferredencoding(False))
	candidates.extend(_SUBPROCESS_DECODINGS)
	seen: set[str] = set()
	ordered: list[str] = []
	for enc in candidates:
		if not enc or enc in seen:
			continue
		seen.add(enc)
		ordered.append(enc)
	return ordered


def _resolve_output_encoding(name: str) -> str:
	"""Resolve CLI --encoding for stdout."""
	if name != "auto":
		return name
	if os.environ.get("PYTHONUTF8", "").lower() in ("1", "true", "yes"):
		return "utf-8"
	stdout_enc = (sys.stdout.encoding or "").lower().replace("-", "")
	if stdout_enc in ("utf8", "utf_8"):
		return "utf-8"
	if sys.platform == "win32":
		try:
			return locale.getencoding() or "mbcs"
		except AttributeError:
			return locale.getpreferredencoding(False) or "mbcs"
	return sys.stdout.encoding or "utf-8"


def _text_decode_score(text: str) -> int:
	"""Heuristic: higher is more likely correct Japanese/ASCII device text."""
	if not text:
		return -999
	score = 0
	if "\ufffd" in text:
		score -= 100
	if "Bluetooth" in text:
		score += 5
	if any("\u3040" <= c <= "\u30ff" or "\u4e00" <= c <= "\u9fff" for c in text):
		score += 25
	# Typical mojibake when UTF-8 is read as MBCS (or the reverse)
	score -= sum(1 for c in text if "\u0080" <= c <= "\u00ff")
	return score


def _json_caption_score(decoded: str) -> int:
	"""Score a decoded JSON blob by PnP Caption fields (if parseable)."""
	try:
		data = json.loads(decoded.strip())
	except json.JSONDecodeError:
		return _text_decode_score(decoded)
	if isinstance(data, dict):
		items = [data]
	elif isinstance(data, list):
		items = data
	else:
		return _text_decode_score(decoded)
	score = 0
	for item in items:
		if isinstance(item, dict):
			score = max(score, _text_decode_score(str(item.get("Caption") or "")))
	return score


def _decode_bytes(data: bytes, encodings: list[str] | None = None) -> tuple[str, str]:
	"""Decode subprocess bytes; return (text, encoding_used)."""
	candidates = encodings or _encoding_candidates()
	if len(candidates) == 1:
		enc = candidates[0]
		try:
			return data.decode(enc), enc
		except (LookupError, UnicodeDecodeError):
			return data.decode("utf-8", errors="replace"), "utf-8(replace)"

	best_text = ""
	best_enc = "utf-8(replace)"
	best_score = -(10**9)
	for enc in candidates:
		try:
			text = data.decode(enc)
		except (LookupError, UnicodeDecodeError):
			continue
		score = _json_caption_score(text)
		if score > best_score:
			best_score = score
			best_text = text
			best_enc = enc
	if best_text:
		return best_text, best_enc
	return data.decode("utf-8", errors="replace"), "utf-8(replace)"


def _out(text: str) -> None:
	"""Print using the resolved console encoding (avoids double codec on Windows)."""
	payload = (text + os.linesep).encode(_OUTPUT_ENCODING, errors="replace")
	try:
		sys.stdout.buffer.write(payload)
		sys.stdout.buffer.flush()
	except (AttributeError, OSError):
		print(text)


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


def _live_ports_pnp() -> tuple[list[dict], str]:
	"""Serial/COM devices via PowerShell (no NVDA imports). Returns rows and decode label."""
	# Do not force PowerShell output encoding: on Japanese Windows the pipeline may be
	# UTF-8 or MBCS (cp932); _decode_bytes picks the best match.
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
		raw = subprocess.check_output(
			["powershell", "-NoProfile", "-Command", ps],
			timeout=30,
		)
	except (subprocess.SubprocessError, OSError) as ex:
		_out("  (PnP query failed: %s)" % ex)
		return [], "n/a"
	text, decode_used = _decode_bytes(raw)
	out = text.strip()
	if not out or out == "null":
		return [], decode_used
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
	return rows, decode_used


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Probe USB/COM data for KGS bdDetect.")
	parser.add_argument(
		"--encoding",
		choices=_ENCODING_CHOICES,
		default="auto",
		help=(
			"Console output encoding and preferred subprocess decode "
			"(auto: system locale / MBCS on Japanese Windows; mbcs: ANSI code page)"
		),
	)
	return parser.parse_args()


def main() -> int:
	global _OUTPUT_ENCODING, _SUBPROCESS_DECODINGS

	args = _parse_args()
	_OUTPUT_ENCODING = _resolve_output_encoding(args.encoding)
	if args.encoding == "mbcs":
		_SUBPROCESS_DECODINGS = ["mbcs", "cp932", "utf-8-sig", "utf-8"]
	elif args.encoding == "utf-8":
		_SUBPROCESS_DECODINGS = ["utf-8-sig", "utf-8", "mbcs"]
	else:
		_SUBPROCESS_DECODINGS = ["utf-8-sig", "utf-8", "mbcs", "cp932"]

	_out("KGS bdDetect probe (stdout encoding: %s)" % _OUTPUT_ENCODING)
	_out("=== Registry USB -> COM (can remain after unplug) ===")
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
	live, pnp_decode = _live_ports_pnp()
	_out("  (PnP JSON decoded as: %s)" % pnp_decode)
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
