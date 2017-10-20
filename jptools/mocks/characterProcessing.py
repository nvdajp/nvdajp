from __future__ import unicode_literals, print_function
import codecs

_entries = {}
_readings = {}

def setup():
	global _entries, _readings
	fname = r"..\source\locale\ja\characters.dic"
	linenum = 0
	with codecs.open(fname,"r","utf_8_sig",errors="replace") as f:
		for line in f:
			if line.isspace() or line.startswith('#'):
				continue
			line=line.rstrip('\r\n')
			temp=line.split("\t")
			if len(temp) > 1:
				key=temp.pop(0)
				code=temp.pop(0)
				rd=temp.pop(0)
				if rd.startswith('[') and rd.endswith(']'):
					_readings[key] = rd[1:-1]
					_entries[key] = temp[0]
				else:
					try:
						print("%d: can't parse '%s'" % (linenum, line))
					except UnicodeEncodeError:
						print("%d: can't parse '%r'" % (linenum, line))
			linenum += 1

setup()

def processSpeechSymbol(lang, s):
	assert lang == 'ja'
	return _entries.get(s, s)

def getCharacterReading(lang, s):
	assert lang == 'ja'
	return _readings.get(s, s)

def getCharacterDescription(lang, s):
	assert lang == 'ja'
	return [_entries.get(s, s)]
