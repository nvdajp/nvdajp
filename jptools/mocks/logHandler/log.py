from __future__ import unicode_literals, print_function

def info(s):
	try:
		print('INFO %s' % s)
	except UnicodeEncodeError:
		print('INFO %r' % s)

def debug(s):
	try:
		print('DEBUG %s' % s)
	except UnicodeEncodeError:
		print('DEBUG %r' % s)
