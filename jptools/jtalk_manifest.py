import argparse

ap = argparse.ArgumentParser()
ap.add_argument("nowdate")
ap.add_argument("fileName")
args = ap.parse_args()
with open(args.fileName, "w") as f:
	f.write(
		"""name = nvdajp_jtalk
summary = "JTalk Japanese TTS"
version = {nowdate}
author = "Takuya Nishimoto <nishimotz@gmail.com>"
description = "Japanese speech engine for NVDA, based on Open JTalk, MeCab and MMDAgent."
url = http://www.nvda.jp/en/
minimumNVDAVersion = 2014.1.0
lastTestedNVDAVersion = 2024.4.0
""".format(nowdate=args.nowdate)
	)
