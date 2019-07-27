from __future__ import unicode_literals, print_function
import argparse
ap = argparse.ArgumentParser()
ap.add_argument('nowdate')
ap.add_argument('fileName')
args = ap.parse_args()
with open(args.fileName, 'w') as f:
    f.write(
        """name = kgsbraille
summary = "KGS Braille Memo Driver"
version = {nowdate}
author = "Takuya Nishimoto <nishimotz@gmail.com>"
description = "KGS Driver, which supports BM Smart series, Braille Memo series, Braille Memo Pocket and Braille Tender."
url = http://www.nvda.jp/en/
minimumNVDAVersion = 2014.1.0
lastTestedNVDAVersion = 2020.1.0
""".format(nowdate=args.nowdate))
