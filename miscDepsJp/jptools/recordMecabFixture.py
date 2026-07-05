# -*- coding: utf-8 -*-
# jptools/recordMecabFixture.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 Takuya Nishimoto
#
# Record MeCab analyzer outputs for all harness cases into a JSON
# fixture (tests/mecabFixture.json in the libkuraji repository), so
# that libkuraji can replay the reference-dictionary analysis without
# MeCab. Re-run this whenever the JTalk dictionary or the harness
# test data changes, then commit the fixture in libkuraji.
#
# Usage (from repo root, with the smoke-test environment):
#   python miscDepsJp/jptools/recordMecabFixture.py [path-to-libkuraji]

import json
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
repo_root = (script_dir / ".." / "..").resolve()
jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
sys.path.insert(0, str(jtalk_dir))
sys.path.insert(0, str(script_dir))

import translator2  # noqa: E402
from mecabAnalyzer import MecabAnalyzer  # noqa: E402
import build_userdic  # noqa: E402


class RecordingAnalyzer(MecabAnalyzer):
	def __init__(self):
		self.recorded = {}

	def analyze(self, text, logwrite=None):
		lines = super().analyze(text, logwrite)
		self.recorded[text] = lines
		return lines


def main():
	if len(sys.argv) > 1:
		libkuraji_root = Path(sys.argv[1])
	else:
		libkuraji_root = repo_root.parent / "libkuraji"
	tests_dir = libkuraji_root / "tests"
	if not (tests_dir / "harness.json").exists():
		print(f"harness.json not found under {tests_dir}", file=sys.stderr)
		return 1

	def log(s):
		pass

	user_dics = build_userdic.ensure_user_dic()
	rec = RecordingAnalyzer()
	rec.initialize(log, str(jtalk_dir), str(jtalk_dir / "dic"), user_dics)
	translator2.initialize(logwrite=log, analyzer=rec)

	cases = []
	for name in ("harness.json", "nabccHarness.json", "eng2Harness.json"):
		cases.extend(json.loads((tests_dir / name).read_text(encoding="utf-8")))

	count = 0
	errors = 0
	for t in cases:
		if "text" not in t:
			continue
		nabcc = t.get("mode") == "NABCC"
		for use_foreign_quotes in (False, True):
			try:
				translator2.translateWithInPos2(
					t["text"], logwrite=log, nabcc=nabcc, use_foreign_quotes=use_foreign_quotes
				)
			except Exception as e:
				errors += 1
				print(f"ERROR {t['text']!r}: {e}", file=sys.stderr)
		count += 1

	out = tests_dir / "mecabFixture.json"
	out.write_text(
		json.dumps(rec.recorded, ensure_ascii=False, indent=1),
		encoding="utf-8",
		newline="\n",
	)
	print(f"recorded {len(rec.recorded)} analyzer calls from {count} cases -> {out}")
	return 1 if errors else 0


if __name__ == "__main__":
	sys.exit(main())
