import sys
if sys.version_info[0] > 2:
	open_file  = lambda name, mode, encoding : open(name, mode, encoding=encoding)
	encode_str = lambda s, encoding : s
else:
	open_file  = lambda name, mode, encoding : open(name, mode)
	encode_str = lambda s, encoding : s.encode(encoding)
import os
import datetime
s = "libopenjtalk " + datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
with open_file("libopenjtalk-timestamp.h", "w", 'utf-8') as f:
	f.write(encode_str(("#define JT_VERSION \"%s\"" % s), 'utf-8'))
	f.write(encode_str(os.linesep, 'utf-8'))
