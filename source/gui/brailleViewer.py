# -*- coding: utf-8 -*-
#brailleViewer.py
#brailleDisplayDrivers/DirectBM.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 Masataka.Shinke

import wx
import gui
import config
import win32api

def getScreenWorkingArea():
	left, top, dw, dh = win32api.GetMonitorInfo(1)['Work']
	return left, top, dw, dh
	

class brailleViewerFrame(wx.Frame):

	def __init__(self):
		super(brailleViewerFrame, self).__init__(gui.mainFrame, wx.ID_ANY, _("NVDA Braille Viewer"), style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MAXIMIZE_BOX)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.SetFont(wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False,"DejaVu Sans"))
		self.SetTransparent(int(255.0 * 0.90))
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.textCtrl = wx.TextCtrl(self, -1,style=wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND)
		sizer.Fit(self)
		menuBar = wx.MenuBar()
		menu = wx.Menu()
		item = menu.Append(wx.ID_ANY, _("Top"))
		self.Bind(wx.EVT_MENU, self.setLeftTop, item)
		item = menu.Append(wx.ID_ANY, _("Bottom"))
		self.Bind(wx.EVT_MENU, self.setLeftBottom, item)
		menuBar.Append(menu, _("Left"))
		menu = wx.Menu()
		item = menu.Append(wx.ID_ANY, _("Top"))
		self.Bind(wx.EVT_MENU, self.setRightTop, item)
		item = menu.Append(wx.ID_ANY, _("Bottom"))
		self.Bind(wx.EVT_MENU, self.setRightBottom, item)
		menuBar.Append(menu, _("Right"))
		self.SetMenuBar(menuBar)
		self.SetSizer(sizer)
		self.setLeftTop()
		self.Show(True)

	def setRightTop(self, *arg):
		left, top, dw, dh = getScreenWorkingArea()
		w = dw / 2
		h = dh / 2
		x = left + dw - w
		y = top
		self.SetPosition((x, y))
		self.SetSize((w, h))

	def setRightBottom(self, *arg):
		left, top, dw, dh = getScreenWorkingArea()
		w = dw / 2
		h = dh / 2
		x = left + dw - w
		y = top + h
		self.SetPosition((x, y))
		self.SetSize((w, h))

	def setLeftTop(self, *arg):
		left, top, dw, dh = getScreenWorkingArea()
		w = dw / 2
		h = dh / 2
		x = left
		y = top
		self.SetPosition((x, y))
		self.SetSize((w, h))

	def setLeftBottom(self, *arg):
		left, top, dw, dh = getScreenWorkingArea()
		w = dw / 2
		h = dh / 2
		x = left
		y = top + h
		self.SetPosition((x, y))
		self.SetSize((w, h))

	def onClose(self, evt):
		deactivate()
		gui.mainFrame.sysTrayIcon.menu_tools_toggleBrailleViewer.Check(False)

_guiFrame=None
isActive=False

def activate():
	global _guiFrame, isActive
	_guiFrame = brailleViewerFrame()
	isActive=True

def appendText(text):
	if not isActive:
		return
	if not isinstance(text,basestring):
		return
	#If the braille viewer text control has the focus, we want to disable updates
	#Otherwize it would be impossible to select text, or even just read it (as a blind person).
	if _guiFrame.FindFocus()==_guiFrame.textCtrl:
		return
	translate = __import__("synthDrivers.jtalk.translator2", globals(), locals(), ('getReadingAndBraille',))
	(sp, tr) = getattr(translate, 'getReadingAndBraille')(text, nabcc=config.conf["braille"]["expandAtCursor"])
	_guiFrame.textCtrl.SetValue(text.strip()+"\n"+sp.strip()+"\n"+tr+"\n")

def deactivate():
	global _guiFrame, isActive
	if not isActive:
		return
	isActive=False
	_guiFrame.Destroy()
	_guiFrame=None

