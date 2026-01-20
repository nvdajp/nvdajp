import codecs

_entries = {}
_readings = {}


def setup():
	global _entries, _readings
	linenum = 0
	fileName = r"..\source\locale\ja\characterDescriptions.dic"
	with codecs.open(fileName, "r", "utf_8_sig", errors="replace") as f:
		for line in f:
			if line.isspace() or line.startswith("#"):
				continue
			line = line.rstrip("\r\n")
			temp = line.split("\t")
			if len(temp) > 1:
				key = temp.pop(0)
				_entries[key] = temp[0]
			else:
				print("%s %d: can't parse '%s'" % (fileName, linenum, line))
	fileName = r"..\source\locale\ja\characters.dic"
	with codecs.open(fileName, "r", "utf_8_sig", errors="replace") as f:
		for line in f:
			if line.isspace() or line.startswith("#"):
				continue
			line = line.rstrip("\r\n")
			temp = line.split("\t")
			if len(temp) > 1:
				key = temp.pop(0)
				code = temp.pop(0)  # noqa: F841
				rd = temp.pop(0)
				if rd.startswith("[") and rd.endswith("]"):
					_readings[key] = rd[1:-1]
					_entries[key] = temp[0]
				else:
					print("%s %d: can't parse '%s'" % (fileName, linenum, line))
			linenum += 1


setup()


def processSpeechSymbol(lang, s):
	assert lang == "ja"
	return _entries.get(s, s)


def getCharacterReading(lang, s):
	assert lang == "ja"
	return _readings.get(s, s)


def getCharacterDescription(lang, s):
	assert lang == "ja"
	return [_entries.get(s, s)]
