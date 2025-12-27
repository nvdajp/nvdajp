# -*- coding: utf-8 -*-
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

user_dics_org = [
    Path(d).resolve() for d in glob(str(configDir / "jtusr.dic"))
]

tempDir = Path(tempfile.mkdtemp())
user_dics = []
for u in user_dics_org:
    b = u.name
    d = tempDir / b
    shutil.copyfile(str(u), str(d))
    user_dics.append(str(d))
