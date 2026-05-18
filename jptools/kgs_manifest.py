import argparse

ap = argparse.ArgumentParser()
ap.add_argument("version")
ap.add_argument("fileName")
args = ap.parse_args()
with open(args.fileName, "w") as f:
	f.write(
		"""name = kgsbraille
summary = "KGS Braille Memo Driver"
version = {version}
author = "Shuaruta Inc. / Takuya Nishimoto <info@shuaruta.com>"
description = "KGS Driver, which supports Next Touch 40, BM Air/Smart series, Braille Memo series, Braille Memo Pocket and Braille Tender."
url = https://www.nvda.jp/en/
minimumNVDAVersion = 2026.1.0
lastTestedNVDAVersion = 2026.1.0
""".format(version=args.version),
	)
