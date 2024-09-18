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
author = "Takuya Nishimoto <nishimotz@gmail.com>"
description = "KGS Driver, which supports BM Smart series, Braille Memo series, Braille Memo Pocket and Braille Tender."
url = https://www.nvda.jp/en/
minimumNVDAVersion = 2019.3.0
lastTestedNVDAVersion = 2024.4.0
""".format(version=args.version)
	)
