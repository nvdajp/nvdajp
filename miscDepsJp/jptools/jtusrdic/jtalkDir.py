# -*- coding: utf-8 -*-
# Copyright (C) 2014 Takuya Nishimoto <nishimotz@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sys
from glob import glob
import tempfile
import codecs
from pathlib import Path

jtalk_dir = (Path(__file__).parent / ".." / ".." / ".." / ".." / ".." / "synthDrivers" / "jtalk").resolve()
if hasattr(sys, "frozen"):
    d = Path.cwd() / "synthDrivers" / "jtalk"
    if d.is_dir():
        jtalk_dir = d

dic_dir = jtalk_dir / "dic"

configDir = Path.cwd()
try:
    import globalVars

    configDir = Path(globalVars.appArgs.configPath).resolve()
except Exception:
    pass

tempDir = Path(tempfile.mkdtemp())


def user_dic_srcs():
    user_dics = []
    for u in [Path(d).resolve() for d in glob(str(configDir / "jtusr*.txt"))]:
        d = tempDir / u.name
        file_reader = codecs.open(str(u), "r", "utf-8-sig")
        file_writer = codecs.open(str(d), "w", "utf-8")
        for line in file_reader:
            file_writer.write(line)
        file_writer.close()
        file_reader.close()
        user_dics.append(str(d))
    return user_dics
