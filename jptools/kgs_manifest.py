import argparse

BASE_SUMMARY = "KGS Braille Memo Driver"
BASE_DESCRIPTION = (
	"KGS Driver, which supports Next Touch 40, BM Air/Smart series, "
	"Braille Memo series, Braille Memo Pocket and Braille Tender."
)

LOCALIZED_MANIFESTS: dict[str, tuple[str, str]] = {
	"ja": (
		"KGS BrailleMemo ドライバー",
		"Next Touch 40、BM Air/Smart シリーズ、Braille Memo シリーズ、Braille Memo Pocket、Braille Tender に対応した KGS 点字ディスプレイドライバーです。",
	),
}


def build_manifest(version: str, locale: str | None = None) -> str:
	"""Return manifest.ini contents for the base package or a localized overlay."""
	if locale:
		localized = LOCALIZED_MANIFESTS.get(locale)
		if localized is None:
			raise ValueError(f"Unsupported manifest locale: {locale}")
		summary, description = localized
		return f'summary = "{summary}"\ndescription = "{description}"\n'
	return f"""name = kgsbraille
summary = "{BASE_SUMMARY}"
version = {version}
author = "Shuaruta Inc. / Takuya Nishimoto <info@shuaruta.com>"
description = "{BASE_DESCRIPTION}"
url = https://www.nvda.jp/en/
minimumNVDAVersion = 2026.1.0
lastTestedNVDAVersion = 2027.1.0
"""


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("version")
	ap.add_argument("fileName")
	ap.add_argument("--locale", default=None, help="Emit localized manifest.ini fields for the given locale")
	args = ap.parse_args()
	with open(args.fileName, "w", encoding="utf-8", newline="\n") as f:
		f.write(build_manifest(args.version, args.locale))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
