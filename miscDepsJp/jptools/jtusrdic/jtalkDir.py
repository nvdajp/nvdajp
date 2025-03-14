# -*- coding: utf-8 -*-
# Copyright (C) 2014 Takuya Nishimoto <nishimotz@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
import sys
from glob import glob
import tempfile
import codecs

jtalk_dir = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "..",
        "..",
        "synthDrivers",
        "jtalk",
    )
)
if hasattr(sys, "frozen"):
    d = os.path.join(os.getcwd(), "synthDrivers", "jtalk")
    if os.path.isdir(d):
        jtalk_dir = d

dic_dir = os.path.join(jtalk_dir, "dic")

configDir = os.getcwd()
try:
    import globalVars

    configDir = os.path.abspath(globalVars.appArgs.configPath)
except:
    pass

tempDir = tempfile.mkdtemp()


def user_dic_srcs():
    user_dics = []
    for u in [os.path.normpath(d) for d in glob(os.path.join(configDir, "jtusr*.txt"))]:
        d = os.path.join(tempDir, os.path.basename(u))
        file_reader = codecs.open(u, "r", "utf-8-sig")
        file_writer = codecs.open(d, "w", "utf-8")
        for line in file_reader:
            file_writer.write(line)
        file_writer.close()
        file_reader.close()
        user_dics.append(d)
    return user_dics
