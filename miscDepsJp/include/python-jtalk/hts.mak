HTSDIR = htsengineapi
HTSLIB = $(HTSDIR)\lib

CC = cl

CFLAGS = /O2 /Ob2 /Oi /Ot /Oy /GT /GL /TC /I $(HTSDIR)\include /DAUDIO_PLAY_NONE
LFLAGS = /LTCG

CORES = $(HTSLIB)\HTS_label.obj $(HTSLIB)\HTS_misc.obj $(HTSLIB)\HTS_model.obj $(HTSLIB)\HTS_pstream.obj $(HTSLIB)\HTS_sstream.obj $(HTSLIB)\HTS_vocoder.obj $(HTSLIB)\HTS_audio.obj

all: $(HTSLIB)\hts_engine_API.lib

$(HTSLIB)\hts_engine_API.lib: $(CORES)
	lib $(LFLAGS) /OUT:$@ $(CORES)
	copy $(HTSLIB)\hts_engine_API.lib lib\hts_engine_API.lib

.c.obj:
	$(CC) $(CFLAGS) /c $*.c /Fo$@

clean:
	del $(HTSLIB)\*.lib
	del $(HTSLIB)\*.obj

