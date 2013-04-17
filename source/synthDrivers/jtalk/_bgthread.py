# _bgthread.py 
# -*- coding: utf-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#Copyright (C) 2010-2012 Takuya Nishimoto (nishimotz.com)
#Copyright (C) 2013 Masamitsu Misono (043.jp)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#
# based on NVDA (synthDrivers/_espeak.py)

from logHandler import log
import threading
import Queue

bgThread = None
bgQueue = None
isSpeaking = False

class BgThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)

	def run(self):
		global isSpeaking
		while True:
			func, args, kwargs = bgQueue.get()
			if not func:
				break
			try:
				func(*args, **kwargs)
			except:
				log.error("Error running function from queue", exc_info=True)
			finally:
				isSpeaking = False
				bgQueue.task_done()

def execWhenDone(func, *args, **kwargs):
	global bgQueue
	# This can't be a kwarg in the function definition because it will consume the first non-keywor dargument which is meant for func.
	mustBeAsync = kwargs.pop("mustBeAsync", False)
	if mustBeAsync or bgQueue.unfinished_tasks != 0:
		# Either this operation must be asynchronous or There is still an operation in progress.
		# Therefore, run this asynchronously in the background thread.
		bgQueue.put((func, args, kwargs))
	else:
		func(*args, **kwargs)

def initialize():
	global bgThread, bgQueue
	bgQueue = Queue.Queue()
	bgThread = BgThread()
	bgThread.start()

def terminate():
	global bgThread, bgQueue
	bgQueue.put((None, None, None))
	bgThread.join()
	bgThread = None
	bgQueue = None
