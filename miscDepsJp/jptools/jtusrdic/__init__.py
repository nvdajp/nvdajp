# -*- coding: utf-8 -*-
# Copyright (C) 2014 Takuya Nishimoto <nishimotz@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalPluginHandler
import gui
import wx
import os
import addonHandler
import globalVars
from logHandler import log
import sys
from pathlib import Path

# Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
script_dir = Path(__file__).resolve().parent
# script_dir -> miscDepsJp/jptools/jtusrdic
# ../../.. -> repo root
repo_root = (script_dir / ".." / ".." / "..").resolve()
jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
jtalk_dir_str = str(jtalk_dir)
if jtalk_dir_str not in sys.path:
	sys.path.insert(0, jtalk_dir_str)
import jtalkDir

impPath = Path(__file__).resolve().parent
sys.path.append(str(impPath))
import plumbum

del sys.path[-1]

_addonDir = (Path(__file__).parent / ".." / "..").resolve()
_curAddon = addonHandler.Addon(str(_addonDir))
_addonSummary = _curAddon.manifest["summary"]
addonHandler.initTranslation()

mecabDictIndex = plumbum.local[str(Path(__file__).parent / "mecab-dict-index.exe")]


def editUserDicSrc(self):
	srcs = jtalkDir.user_dic_srcs()
	if srcs:
		for s in srcs:
			os.startfile(s)
	else:
		fileName = str(Path(jtalkDir.configDir) / "jtusr.txt")
		with open(fileName, "w", encoding="utf-8", errors="replace") as f:
			f.writelines(
				[
					"足手纏い,,,,名詞,形容動詞語幹,*,*,*,*,足手纏い,アシデマトイ,アシデマトイ,4/6,C1,アシデ マトイ\n",
				],
			)
		os.startfile(fileName)


def compileUserDic(self):
	log.info('system_dic "%s"' % jtalkDir.dic_dir)
	log.info('configDir "%s"' % jtalkDir.configDir)
	srcs = jtalkDir.user_dic_srcs()
	if not srcs:
		gui.messageBox(_("No source found."), _("Done"), wx.OK)
		return
	for s in srcs:
		u = str(Path(jtalkDir.configDir) / Path(s).name.replace(".txt", ".dic"))
		log.info("user_dic %s to %s" % (s, u))
		# mecab-dict-index.exe -d ..\source\synthDrivers\jtalk\dic -u jtusr.dic -f utf-8 -t utf-8 jtusr.txt
		ret = mecabDictIndex["-d", jtalkDir.dic_dir, "-u", u, "-f", "utf-8", "-t", "utf-8", s]()
		log.info(ret)
	gui.messageBox(_("Compile done."), _("Done"), wx.OK)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _addonSummary

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		if globalVars.appArgs.secure:
			return
		self.createMenu()

	def createMenu(self):
		items = gui.mainFrame.sysTrayIcon.menu.GetMenuItems()
		self.toolsMenu = items[1].GetSubMenu()
		self.editItem = self.toolsMenu.Append(
			wx.ID_ANY,
			# Translators:
			_("Edit JTalk User Dic source"),
			# Translators:
			_("Edit JTalk/Japanese Braille user dictionary source"),
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, editUserDicSrc, self.editItem)
		self.compileItem = self.toolsMenu.Append(
			wx.ID_ANY,
			# Translators:
			_("Compile JTalk User Dic"),
			# Translators:
			_("Compile JTalk/Japanese Braille user dictionary"),
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, compileUserDic, self.compileItem)

	def terminate(self):
		try:
			self.toolsMenu.RemoveItem(self.editItem)
			self.toolsMenu.RemoveItem(self.compileItem)
		except wx.PyDeadObjectError:
			pass
