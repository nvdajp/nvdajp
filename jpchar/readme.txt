更新予定

A part of NonVisual Desktop Access (NVDA)
This file is covered by the GNU General Public License.
See the file COPYING for more details.
Copyright (C) 2015-2019 Takuya Nishimoto


copy Japanese character symbols to subversion repo

jpchar\copy_symbols_to_srt.cmd


checkCharDesc.py
====================================

character description consistency check

> cd jpchar
> py -2 checkCharDesc.py


checkSymbols.py
====================================

symbols consistency check

> cd jpchar
> py -2 checkSymbols.py


updateCharDesc.py
====================================

convert characters.dic to characterDescriptions.dic

> cd jpchar
> py -2 updateCharDesc.py > newfile.dic


emoji.txt
====================================
https://osdn.jp/ticket/browse.php?group_id=4221&tid=30841
https://github.com/nvdajp/nvdajp/issues/7


japanese_rokuten_kanji_braille.py
====================================
> cd jpchar
> py -3.6-32 japanese_rokuten_kanji_braille.py > ../source/ja-jp-rokutenkanji.tbl
