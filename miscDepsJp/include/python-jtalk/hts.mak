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

$(HTSLIB)\HTS_label.obj: $(HTSLIB)\HTS_label.c
	$(CC) $(CFLAGS) /c $(HTSLIB)\HTS_label.c /Fo$@

$(HTSLIB)\HTS_misc.obj: $(HTSLIB)\HTS_misc.c
	$(CC) $(CFLAGS) /c $(HTSLIB)\HTS_misc.c /Fo$@

$(HTSLIB)\HTS_model.obj: $(HTSLIB)\HTS_model.c
	$(CC) $(CFLAGS) /c $(HTSLIB)\HTS_model.c /Fo$@

$(HTSLIB)\HTS_pstream.obj: $(HTSLIB)\HTS_pstream.c
	$(CC) $(CFLAGS) /c $(HTSLIB)\HTS_pstream.c /Fo$@

$(HTSLIB)\HTS_sstream.obj: $(HTSLIB)\HTS_sstream.c
	$(CC) $(CFLAGS) /c $(HTSLIB)\HTS_sstream.c /Fo$@

$(HTSLIB)\HTS_vocoder.obj: $(HTSLIB)\HTS_vocoder.c
	$(CC) $(CFLAGS) /c $(HTSLIB)\HTS_vocoder.c /Fo$@

$(HTSLIB)\HTS_audio.obj: $(HTSLIB)\HTS_audio.c
	$(CC) $(CFLAGS) /c $(HTSLIB)\HTS_audio.c /Fo$@

clean:
	del $(HTSLIB)\*.lib
	del $(HTSLIB)\*.obj

