# python3
# https://github.com/nvdajp/nvdajp/issues/207
from xml.etree import ElementTree
from collections import OrderedDict

source = r"..\include\cldr\annotations\ja.xml"

cldrDict = OrderedDict()
tree = ElementTree.parse(source)
for element in tree.iter("annotation"):
	if element.attrib.get("type") == "tts":
		if "ハート" in element.text:
			cldrDict[element.attrib["cp"]] = element.text
# print(cldrDict)
assert cldrDict["\U0001f90d"] == "白いハート"


symbols = r"..\source\locale\ja\symbols.dic"

with open(symbols, encoding="utf-8") as fp:
	for cnt, line in enumerate(fp):
		line = line.rstrip()
		if line and not line.startswith("#"):
			fields = line.split("\t")
			if fields and fields[0] in cldrDict:
				if fields[1] == "ハート":
					print("symbols.dic:{} {} => {}".format(cnt + 1, repr(fields), cldrDict[fields[0]]))


characters = r"..\source\locale\ja\characters.dic"

with open(characters, encoding="utf-8") as fp:
	for cnt, line in enumerate(fp):
		line = line.rstrip()
		if line and not line.startswith("#"):
			fields = line.split("\t")
			if fields and fields[0] in cldrDict:
				if fields[2] == "[ハート]":
					print("characters.dic:{} {} => {}".format(cnt + 1, repr(fields), cldrDict[fields[0]]))


characterDescriptions = r"..\source\locale\ja\characterDescriptions.dic"

with open(characterDescriptions, encoding="utf-8") as fp:
	for cnt, line in enumerate(fp):
		line = line.rstrip()
		if line and not line.startswith("#"):
			fields = line.split("\t")
			if fields and fields[0] in cldrDict:
				print(
					"characterDescriptions.dic:{} {} => {}".format(cnt + 1, repr(fields), cldrDict[fields[0]])
				)
