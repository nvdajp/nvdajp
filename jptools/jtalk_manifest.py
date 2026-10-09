import argparse

ap = argparse.ArgumentParser()
ap.add_argument("nowdate")
ap.add_argument("fileName")
args = ap.parse_args()
with open(args.fileName, "w") as f:
	f.write(
		f"""name = nvdajp_jtalk
summary = "JTalk Japanese TTS"
version = {args.nowdate}
author = "Takuya Nishimoto <nishimotz@gmail.com>"
description = "Japanese speech engine for NVDA, based on Open JTalk, MeCab and MMDAgent."
url = https://www.nvda.jp/en/
minimumNVDAVersion = 2014.1.0
lastTestedNVDAVersion = 2027.1.0
""",
	)
