# coding: utf-8
from __future__ import unicode_literals
import time
from ctypes import *
import wx

DLLPATH = r'..\client\nvdaControllerClient32.dll'
clientLib = windll.LoadLibrary(DLLPATH)
if clientLib:
	clientLib.nvdaController_setAppSleepMode.argtypes = [c_uint, c_int]

procId = windll.kernel32.GetCurrentProcessId()

def nvdaRunning():
	if clientLib:
		res = clientLib.nvdaController_testIfRunning()
		if res == 0:
			return True
	return False

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="TestApp", size=(300,200))
		self.tc = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
		self.tc.Value = "hello\nline2\nline3\n"

		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()
		self.speakItem = self.fileMenu.Append(-1, '&Speak')
		self.Bind(wx.EVT_MENU, self.OnSpeak, self.speakItem)
		self.sleepItem = self.fileMenu.Append(-1, 'Sleep O&n')
		self.Bind(wx.EVT_MENU, self.OnSleep, self.sleepItem)
		self.wakeupItem = self.fileMenu.Append(-1, 'Sleep O&ff')
		self.Bind(wx.EVT_MENU, self.OnWakeup, self.wakeupItem)
		self.quitItem = self.fileMenu.Append(-1, '&Quit')
		self.Bind(wx.EVT_MENU, self.OnQuit, self.quitItem)
		self.menubar.Append(self.fileMenu, '&File')
		self.SetMenuBar(self.menubar)
		
		self.Centre()
		self.Show(True)

	def OnSpeak(self, event):
		if nvdaRunning():
			res = clientLib.nvdaController_speakText(self.tc.Value)

	def OnSleep(self, event):
		if nvdaRunning():
			res = clientLib.nvdaController_setAppSleepMode(procId, 1)
			print "setAppSleepMode(%d,1):%d" % (procId, res)

	def OnWakeup(self, event):
		if nvdaRunning():
			res = clientLib.nvdaController_setAppSleepMode(procId, 0)
			print "setAppSleepMode(%d,0):%d" % (procId, res)

	def OnQuit(self, event):
		self.Close()

app = wx.App(False)
frame = MyFrame()
frame.Show()
app.MainLoop()
