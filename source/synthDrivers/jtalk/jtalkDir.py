# A part of NonVisual Desktop Access (NVDA)
# speech engine nvdajp_jtalk
# Copyright (C) 2010-2014 Takuya Nishimoto (nishimotz.com)

import sys
from glob import glob
import tempfile
import shutil
from pathlib import Path


jtalk_dir = Path(__file__).parent
if hasattr(sys, "frozen"):
	d = Path.cwd() / "synthDrivers" / "jtalk"
	if d.is_dir():
		jtalk_dir = d

configDir = Path.cwd()
try:
	import globalVars  # type: ignore

	if globalVars.appArgs.configPath:
		configDir = Path(globalVars.appArgs.configPath)
		d = Path(globalVars.appArgs.configPath) / "addons" / "nvdajp_jtalk" / "synthDrivers" / "jtalk"
		if d.is_dir():
			jtalk_dir = d
except Exception:
	pass

dic_dir = jtalk_dir / "dic"
dic_cmudict_dir = jtalk_dir / "dic_cmudict"

user_dics_org = [Path(d).resolve() for d in glob(str(configDir / "jtusr.dic"))]

tempDir = Path(tempfile.mkdtemp())
user_dics = []
for u in user_dics_org:
	b = u.name
	d = tempDir / b
	shutil.copyfile(str(u), str(d))
	user_dics.append(str(d))


def resolve_dic_config(eng_dic: str = "bep") -> tuple[Path, list[str]]:
	"""Resolve (dic_dir, user_dics) for the selected English reading dictionary mode ('bep' or 'cmudict')."""
	mode = (eng_dic or "bep").strip().lower()
	active_user_dics = list(user_dics)
	if mode == "cmudict":
		if (dic_cmudict_dir / "sys.dic").is_file():
			return dic_cmudict_dir, active_user_dics
		for candidate in (dic_dir / "jteng_cmudict.dic", configDir / "jteng_cmudict.dic"):
			if candidate.is_file():
				staged = tempDir / candidate.name
				if not staged.is_file():
					try:
						shutil.copyfile(str(candidate), str(staged))
					except OSError:
						staged = candidate
				if str(staged) not in active_user_dics:
					active_user_dics.append(str(staged))
				break
	return dic_dir, active_user_dics
