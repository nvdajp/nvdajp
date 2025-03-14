import datetime
import os

s = "libopenjtalk " + datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
with open("libopenjtalk\\lib\\libopenjtalk-timestamp.h", "wb") as f:
    f.write('#define JT_VERSION "%s"' % s)
    f.write(os.linesep)
