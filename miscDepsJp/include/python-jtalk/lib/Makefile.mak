# Makefile.mak
# libopenjtalk by Takuya Nishimoto
# for nmake 
# based on Open-JTalk

target: libopenjtalk-timestamp.h libopenjtalk.obj libopenjtalk.dll

CC = cl
LINK = link
CFLAGS = /O2 /Ob2 /Oi /Ot /Oy /GT /GL /TC 

OJTDIR = ../libopenjtalk
HTSDIR = ../htsengineapi
JPCOMMONDIR = ../jpcommon

INCLUDES = -I$(OJTDIR)/text2mecab \
           -I$(OJTDIR)/mecab/src \
           -I$(OJTDIR)/mecab2njd \
           -I$(OJTDIR)/njd \
           -I$(OJTDIR)/njd_set_pronunciation \
           -I$(OJTDIR)/njd_set_digit \
           -I$(OJTDIR)/njd_set_accent_phrase \
           -I$(OJTDIR)/njd_set_accent_type \
           -I$(OJTDIR)/njd_set_unvoiced_vowel \
           -I$(OJTDIR)/njd_set_long_vowel \
           -I$(OJTDIR)/njd2jpcommon \
           -I$(OJTDIR)/mecab2njd \
           -I$(JPCOMMONDIR) \
           -I$(OJTDIR)/mecab \
           -I$(HTSDIR)/include \
           -I$(HTSDIR)/lib \
           -I.

LDADD = $(OJTDIR)/text2mecab/text2mecab.lib \
           $(OJTDIR)/mecab2njd/mecab2njd.lib \
           $(OJTDIR)/njd/njd.lib \
           $(OJTDIR)/njd_set_pronunciation/njd_set_pronunciation.lib \
           $(OJTDIR)/njd_set_digit/njd_set_digit.lib \
           $(OJTDIR)/njd_set_accent_phrase/njd_set_accent_phrase.lib \
           $(OJTDIR)/njd_set_accent_type/njd_set_accent_type.lib \
           $(OJTDIR)/njd_set_unvoiced_vowel/njd_set_unvoiced_vowel.lib \
           $(OJTDIR)/njd_set_long_vowel/njd_set_long_vowel.lib \
           $(OJTDIR)/njd2jpcommon/njd2jpcommon.lib \
           $(JPCOMMONDIR)/jpcommon.lib \
           HTS_Engine_API.lib

HTS_gstream_ex.c:
	copy ..\htsengineapi\lib\HTS_gstream.c HTS_gstream_ex.c
	patch HTS_gstream_ex.c HTS_gstream_ex.patch

HTS_engine_ex.c:
	copy ..\htsengineapi\lib\HTS_engine.c HTS_engine_ex.c
	patch HTS_engine_ex.c HTS_engine_ex.patch

libopenjtalk-timestamp.h:
	python make_timestamp.py

.c.obj:
	$(CC) $(INCLUDES) $(CFLAGS) /c $*.c /Fo$@

libopenjtalk.dll: libopenjtalk.obj HTS_gstream_ex.obj HTS_engine_ex.obj
	$(LINK) /DLL /RELEASE /MACHINE:x86 /LTCG /OUT:libopenjtalk.dll \
	libopenjtalk.obj HTS_gstream_ex.obj HTS_engine_ex.obj $(LDADD) /DEF:libopenjtalk.def

clean:	
	del /Q *.dll *.obj
	del /Q libopenjtalk-timestamp.h
	del /Q HTS_engine_ex.c
	del /Q HTS_gstream_ex.c
