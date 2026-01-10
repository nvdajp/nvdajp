# _bgthread.py
# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
# Copyright (C) 2010-2012 Takuya Nishimoto (nishimotz.com)
# Copyright (C) 2013 Masamitsu Misono (043.jp)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
#
# based on NVDA (synthDrivers/_espeak.py)

from typing import Callable, Any
from logHandler import log
import threading


import queue as Queue


bgThread: threading.Thread | None = None
bgQueue: Queue.Queue[tuple[Callable[..., Any] | None, tuple[Any, ...] | None, dict[str, Any] | None]] | None = None
isSpeaking: bool = False


class BgThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)

	def run(self) -> None:
		global isSpeaking, bgQueue
		if bgQueue is None:
			return
		while True:
			item = bgQueue.get()
			func, args, kwargs = item
			if func is None:
				break
			if args is None:
				args = ()
			if kwargs is None:
				kwargs = {}
			try:
				func(*args, **kwargs)
			except Exception:
				log.error("Error running function from queue", exc_info=True)
			finally:
				isSpeaking = False
				bgQueue.task_done()


def execWhenDone(func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
	global bgQueue
	# This can't be a kwarg in the function definition because it will consume the first non-keywor dargument which is meant for func.
	mustBeAsync = kwargs.pop("mustBeAsync", False)
	if bgQueue is None:
		func(*args, **kwargs)
		return
	if mustBeAsync or bgQueue.unfinished_tasks != 0:
		# Either this operation must be asynchronous or There is still an operation in progress.
		# Therefore, run this asynchronously in the background thread.
		bgQueue.put((func, args, kwargs))
	else:
		func(*args, **kwargs)


def initialize() -> None:
	global bgThread, bgQueue
	bgQueue = Queue.Queue()
	bgThread = BgThread()
	bgThread.start()


def terminate() -> None:
	global bgThread, bgQueue
	if bgQueue is not None:
		bgQueue.put((None, None, None))
	if bgThread is not None:
		bgThread.join()
	bgThread = None
	bgQueue = None
