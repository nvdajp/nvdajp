
CC = cl

CFLAGS = /O2 /Ob2 /Oi /Ot /Oy /GT /GL /TC /I ../njd /D CHARSET_UTF_8 /source-charset:utf-8 /execution-charset:utf-8
LFLAGS = /LTCG

CORES = njd_set_accent_type.obj

all: njd_set_accent_type.lib

njd_set_accent_type.lib: $(CORES)
	lib $(LFLAGS) /OUT:$@ $(CORES)

.c.obj:
	$(CC) $(CFLAGS) /c $<

clean:
	del *.lib
	del *.obj
