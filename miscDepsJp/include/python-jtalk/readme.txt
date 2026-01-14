A part of NonVisual Desktop Access (NVDA)
This file is covered by the GNU General Public License.
See the file COPYING for more details.
Copyright (C) 2015-2023 Takuya Nishimoto

setup:

Visual Studio 2022

Python 3.11 (win32)

> git clone https://github.com/nvdajp/python-jtalk
> cd python-jtalk
> git submodule sync
> git submodule update --init --recursive
> vcsetup.cmd
> clean.cmd
> build.cmd

> dir ..\nvdajp\source\synthDrivers\jtalk\dic /w

[.]                   [..]                  char.bin
COPYING               COPYING-bep-eng.txt   dicrc
DIC_VERSION           left-id.def           matrix.bin
pos-id.def            rewrite.def           right-id.def
sys.dic               unk.dic

> dir ..\nvdajp\source\synthDrivers\jtalk\mei /w

[.]                   [..]                  COPYRIGHT.txt
mei_normal.htsvoice   README.txt

> python jtalkRunner.py
