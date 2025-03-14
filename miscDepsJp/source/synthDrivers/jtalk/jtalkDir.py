# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# speech engine nvdajp_jtalk
# Copyright (C) 2010-2014 Takuya Nishimoto (nishimotz.com)

import os
import sys
from glob import glob
import tempfile
import shutil
from os import getcwd


jtalk_dir = os.path.dirname(__file__)
if hasattr(sys, "frozen"):
    d = os.path.join(getcwd(), "synthDrivers", "jtalk")
    if os.path.isdir(d):
        jtalk_dir = d

configDir = getcwd()
try:
    import globalVars  # type: ignore

    configDir = globalVars.appArgs.configPath
    d = os.path.join(
        globalVars.appArgs.configPath, "addons", "nvdajp_jtalk", "synthDrivers", "jtalk"
    )
    if os.path.isdir(d):
        jtalk_dir = d
except:
    pass

dic_dir = os.path.join(jtalk_dir, "dic")

user_dics_org = [
    os.path.normpath(d) for d in glob(os.path.join(configDir, "jtusr.dic"))
]

tempDir = tempfile.mkdtemp()
user_dics = []
for u in user_dics_org:
    b = os.path.basename(u)
    d = os.path.join(tempDir, b)
    shutil.copyfile(u, d)
    user_dics.append(d)
