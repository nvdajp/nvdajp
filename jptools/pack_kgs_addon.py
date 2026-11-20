import argparse
import ast
import os
import shutil
import subprocess
import tempfile
import zipfile
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

try:
	import kgs_manifest
except ImportError:
	from jptools import kgs_manifest


DRIVER_FILENAMES = (
	"kgs.py",
	"brailleMemo.py",
)

ADDON_BINARIES = ("DirectBM.dll",)


def find_msgfmt(repo_root: Path) -> Path:
	"""Locate GNU msgfmt executable in miscDeps/tools or on PATH."""
	candidate = repo_root / "miscDeps" / "tools" / "msgfmt.exe"
	if candidate.is_file():
		return candidate
	on_path = shutil.which("msgfmt") or shutil.which("msgfmt.exe")
	if on_path:
		return Path(on_path)
	raise FileNotFoundError(
		"msgfmt executable not found (checked miscDeps/tools/msgfmt.exe and PATH). "
		"Run 'git submodule update --init' or install GNU gettext.",
	)


def collect_driver_translation_keys(driver_paths: Iterable[Path]) -> set[tuple[str | None, str]]:
	"""Extract static (msgctxt, msgid) pairs passed to gettext functions in driver sources."""
	keys: set[tuple[str | None, str]] = set()
	for path in driver_paths:
		tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
		for node in ast.walk(tree):
			if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
				continue
			fn = node.func.id
			args = node.args
			if fn == "_" and args and isinstance(args[0], ast.Constant) and isinstance(args[0].value, str):
				keys.add((None, args[0].value))
			elif (
				fn == "pgettext"
				and len(args) >= 2
				and isinstance(args[0], ast.Constant)
				and isinstance(args[0].value, str)
				and isinstance(args[1], ast.Constant)
				and isinstance(args[1].value, str)
			):
				keys.add((args[0].value, args[1].value))
			elif (
				fn == "ngettext"
				and len(args) >= 2
				and isinstance(args[0], ast.Constant)
				and isinstance(args[0].value, str)
				and isinstance(args[1], ast.Constant)
				and isinstance(args[1].value, str)
			):
				keys.add((None, args[0].value))
			elif (
				fn == "npgettext"
				and len(args) >= 3
				and isinstance(args[0], ast.Constant)
				and isinstance(args[0].value, str)
				and isinstance(args[1], ast.Constant)
				and isinstance(args[1].value, str)
				and isinstance(args[2], ast.Constant)
				and isinstance(args[2].value, str)
			):
				keys.add((args[0].value, args[1].value))
	return keys


def _parse_po_block(
	block: list[str],
) -> tuple[str | None, str, bool, bool, list[str], list[str]] | None:
	"""Parse one blank-line-separated PO entry into metadata and preserved lines."""
	body_lines = [line for line in block if not line.startswith("#")]
	if not body_lines:
		return None

	flag_lines = [line for line in block if line.startswith("#,")]
	is_fuzzy = any("fuzzy" in [flag.strip() for flag in line[2:].split(",")] for line in flag_lines)

	fields: dict[str, list[str]] = {}
	cur_field: str | None = None
	for line in body_lines:
		matched_prefix = False
		for prefix in ("msgctxt ", "msgid ", "msgid_plural ", "msgstr "):
			if line.startswith(prefix):
				cur_field = prefix.strip()
				fields[cur_field] = [ast.literal_eval(line[len(prefix) :])]
				matched_prefix = True
				break
		if matched_prefix:
			continue
		if line.startswith("msgstr["):
			end_idx = line.index("]")
			cur_field = line[: end_idx + 1]
			fields[cur_field] = [ast.literal_eval(line[end_idx + 1 :].strip())]
		elif line.startswith('"') and cur_field is not None:
			fields[cur_field].append(ast.literal_eval(line))

	if "msgid" not in fields:
		return None

	msgctxt = "".join(fields["msgctxt"]) if "msgctxt" in fields else None
	msgid = "".join(fields["msgid"])
	has_translation = "".join(fields.get("msgstr", [])) != "" or any(
		"".join(parts) != "" for key, parts in fields.items() if key.startswith("msgstr[")
	)

	kept_flags: list[str] = []
	for fl in flag_lines:
		flags = [flag.strip() for flag in fl[2:].split(",") if flag.strip() and flag.strip() != "fuzzy"]
		if flags:
			kept_flags.append("#, " + ", ".join(flags))

	return (msgctxt, msgid, is_fuzzy, has_translation, kept_flags, body_lines)


def extract_po_subset(po_path: Path, keys: set[tuple[str | None, str]]) -> str | None:
	"""Extract translated, non-fuzzy PO entries matching *keys* alongside the PO header."""
	text = po_path.read_text(encoding="utf-8-sig")
	blocks: list[list[str]] = []
	cur_block: list[str] = []
	for line in text.splitlines() + [""]:
		if line.strip() == "":
			if cur_block:
				blocks.append(cur_block)
				cur_block = []
		else:
			cur_block.append(line)

	header_lines: list[str] | None = None
	matched_blocks: list[str] = []
	seen_keys: set[tuple[str | None, str]] = set()

	for block in blocks:
		parsed = _parse_po_block(block)
		if parsed is None:
			continue
		msgctxt, msgid, is_fuzzy, has_translation, kept_flags, body_lines = parsed
		if msgctxt is None and msgid == "":
			header_lines = body_lines
			continue
		if is_fuzzy or not has_translation or (msgctxt, msgid) not in keys or (msgctxt, msgid) in seen_keys:
			continue
		seen_keys.add((msgctxt, msgid))
		matched_blocks.append("\n".join(kept_flags + body_lines))

	if not matched_blocks:
		return None

	header_block = (
		"\n".join(header_lines)
		if header_lines is not None
		else 'msgid ""\nmsgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"'
	)
	return "\n\n".join([header_block, *matched_blocks]) + "\n"


def build_kgs_addon(repo_root: Path, version: str, out_zip: Path) -> Path:
	"""Create the kgsbraille .nvda-addon zip archive including localized manifests and .mo catalogs."""
	source_dir = repo_root / "source"
	drivers_dir = source_dir / "brailleDisplayDrivers"
	driver_paths = [drivers_dir / filename for filename in DRIVER_FILENAMES]
	translation_keys = collect_driver_translation_keys(driver_paths)
	msgfmt_path = find_msgfmt(repo_root)

	out_zip.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory() as tmp_dir_str:
		tmp_dir = Path(tmp_dir_str)
		with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
			zf.writestr("manifest.ini", kgs_manifest.build_manifest(version).encode("utf-8"))
			for filename in (*DRIVER_FILENAMES, *ADDON_BINARIES):
				zf.write(drivers_dir / filename, f"brailleDisplayDrivers/{filename}")

			for locale in sorted(kgs_manifest.LOCALIZED_MANIFESTS):
				zf.writestr(
					f"locale/{locale}/manifest.ini",
					kgs_manifest.build_manifest(version, locale).encode("utf-8"),
				)

			locale_dir = source_dir / "locale"
			for po_path in sorted(locale_dir.glob("*/LC_MESSAGES/nvda.po")):
				lang = po_path.parts[-3]
				subset_po = extract_po_subset(po_path, translation_keys)
				if subset_po is None:
					continue
				tmp_po = tmp_dir / f"{lang}.po"
				tmp_mo = tmp_dir / f"{lang}.mo"
				tmp_po.write_text(subset_po, encoding="utf-8", newline="\n")
				subprocess.check_call([str(msgfmt_path), "-c", "-o", str(tmp_mo), str(tmp_po)])
				zf.write(tmp_mo, f"locale/{lang}/LC_MESSAGES/nvda.mo")

	return out_zip


def main() -> int:
	parser = argparse.ArgumentParser(description="Pack KGS braille addon without 7z")
	parser.add_argument(
		"--version",
		default=os.environ.get("VERSION") or os.environ.get("KGSVERSION") or os.environ.get("nowdate"),
	)
	parser.add_argument(
		"--output",
		default=None,
		help="Optional output .nvda-addon path (defaults to jptools/kgsbraille-<version>.nvda-addon)",
	)
	args = parser.parse_args()

	repo_root = Path(__file__).resolve().parents[1]
	jptools_dir = repo_root / "jptools"
	version = args.version or datetime.now().astimezone().strftime("%y%m%d")
	out_zip = Path(args.output) if args.output else jptools_dir / f"kgsbraille-{version}.nvda-addon"

	build_kgs_addon(repo_root, version, out_zip)
	print(str(out_zip))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
