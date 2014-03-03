#speechViewer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui

class SpeechViewerFrame(wx.Frame):

	def __init__(self):
		super(SpeechViewerFrame, self).__init__(gui.mainFrame, wx.ID_ANY, _("NVDA Speech Viewer"), style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MAXIMIZE_BOX)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.SetFont(wx.Font(16,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL,False))
		self.SetTransparent(int(255.0 * 0.90))
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.textCtrl = wx.TextCtrl(self, -1,size=(500,500),style=wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.textCtrl, proportion=1, flag=wx.EXPAND)
		sizer.Fit(self)
		self.SetSizer(sizer)
		self.Show(True)

	def onClose(self, evt):
		deactivate()
		gui.mainFrame.sysTrayIcon.menu_tools_toggleSpeechViewer.Check(False)
		return
		if not evt.CanVeto():
			self.Destroy()
			return
		evt.Veto()

_guiFrame=None
isActive=False

def activate():
	global _guiFrame, isActive
	_guiFrame = SpeechViewerFrame()
	isActive=True

def appendText(text):
	if not isActive:
		return
	if not isinstance(text,basestring):
		return
	#If the speech viewer text control has the focus, we want to disable updates
	#Otherwize it would be impossible to select text, or even just read it (as a blind person).
	if _guiFrame.FindFocus()==_guiFrame.textCtrl:
		return
	_guiFrame.textCtrl.AppendText(text + "\n")

def deactivate():
	global _guiFrame, isActive
	if not isActive:
		return
	isActive=False
	_guiFrame.Destroy()
	_guiFrame = None
