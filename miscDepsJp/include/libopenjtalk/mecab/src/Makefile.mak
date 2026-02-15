
CC = cl
# Use LINK instead of CL to avoid conflict with environment variable CL (set by vcsetup.cmd)
# Environment variable CL is used by MSVC compiler for additional flags (e.g., /arch:IA32)
LINK = link

# MACHINE parameter support (x86 or x64, default to x86)
!IFNDEF MACHINE
MACHINE = x86
!ENDIF

# Common CFLAGS base
CFLAGS_BASE = /O2 /Ob2 /Oi /Ot /Oy /GT /GL /TP /EHsc /D CHARSET_SHIFT_JIS /source-charset:shift_jis /execution-charset:shift_jis /D DIC_VERSION=102 /D MECAB_WITHOUT_MUTEX_LOCK /D MECAB_DEFAULT_RC=\"dummy\" /D PACKAGE=\"open_jtalk\" /D VERSION=\"1.01\" /D HAVE_WINDOWS_H
# CFLAGS for static library and executable
CFLAGS = $(CFLAGS_BASE) /D MECAB_STATIC
# CFLAGS for DLL (add DLL_EXPORT macro)
CFLAGS_DLL = $(CFLAGS_BASE) /D DLL_EXPORT
LFLAGS = /LTCG

CORES = char_property.obj connector.obj context_id.obj dictionary.obj dictionary_compiler.obj dictionary_generator.obj dictionary_rewriter.obj eval.obj feature_index.obj iconv_utils.obj lbfgs.obj learner.obj learner_tagger.obj libmecab.obj mecab.obj nbest_generator.obj param.obj string_buffer.obj tagger.obj tokenizer.obj utils.obj viterbi.obj writer.obj

# Object files for DLL (need to be compiled with DLL_EXPORT)
CORES_DLL = char_property_dll.obj connector_dll.obj context_id_dll.obj dictionary_dll.obj dictionary_compiler_dll.obj dictionary_generator_dll.obj dictionary_rewriter_dll.obj eval_dll.obj feature_index_dll.obj iconv_utils_dll.obj lbfgs_dll.obj learner_dll.obj learner_tagger_dll.obj libmecab_dll.obj mecab_dll.obj nbest_generator_dll.obj param_dll.obj string_buffer_dll.obj tagger_dll.obj tokenizer_dll.obj utils_dll.obj viterbi_dll.obj writer_dll.obj

LIBS = mecab.lib Advapi32.lib

all: mecab.lib mecab-dict-index.exe libmecab.dll

mecab.lib: $(CORES)
	lib $(LFLAGS) /OUT:$@ $(CORES)

mecab-dict-index.exe: mecab-dict-index.obj
	$(LINK) /LTCG /OUT:$@ $(LIBS) $(@B).obj

libmecab.dll: $(CORES_DLL)
	$(LINK) /DLL /RELEASE /MACHINE:$(MACHINE) /LTCG /OUT:libmecab.dll $(CORES_DLL) Advapi32.lib /DEF:libmecab.def

.cpp.obj:
	$(CC) $(CFLAGS) /c $<

# Explicit rules for DLL object files
char_property_dll.obj: char_property.cpp
	$(CC) $(CFLAGS_DLL) /c char_property.cpp /Fo$@

connector_dll.obj: connector.cpp
	$(CC) $(CFLAGS_DLL) /c connector.cpp /Fo$@

context_id_dll.obj: context_id.cpp
	$(CC) $(CFLAGS_DLL) /c context_id.cpp /Fo$@

dictionary_dll.obj: dictionary.cpp
	$(CC) $(CFLAGS_DLL) /c dictionary.cpp /Fo$@

dictionary_compiler_dll.obj: dictionary_compiler.cpp
	$(CC) $(CFLAGS_DLL) /c dictionary_compiler.cpp /Fo$@

dictionary_generator_dll.obj: dictionary_generator.cpp
	$(CC) $(CFLAGS_DLL) /c dictionary_generator.cpp /Fo$@

dictionary_rewriter_dll.obj: dictionary_rewriter.cpp
	$(CC) $(CFLAGS_DLL) /c dictionary_rewriter.cpp /Fo$@

eval_dll.obj: eval.cpp
	$(CC) $(CFLAGS_DLL) /c eval.cpp /Fo$@

feature_index_dll.obj: feature_index.cpp
	$(CC) $(CFLAGS_DLL) /c feature_index.cpp /Fo$@

iconv_utils_dll.obj: iconv_utils.cpp
	$(CC) $(CFLAGS_DLL) /c iconv_utils.cpp /Fo$@

lbfgs_dll.obj: lbfgs.cpp
	$(CC) $(CFLAGS_DLL) /c lbfgs.cpp /Fo$@

learner_dll.obj: learner.cpp
	$(CC) $(CFLAGS_DLL) /c learner.cpp /Fo$@

learner_tagger_dll.obj: learner_tagger.cpp
	$(CC) $(CFLAGS_DLL) /c learner_tagger.cpp /Fo$@

libmecab.obj: libmecab.cpp
	$(CC) $(CFLAGS) /c libmecab.cpp /Fo$@

libmecab_dll.obj: libmecab.cpp
	$(CC) $(CFLAGS_DLL) /c libmecab.cpp /Fo$@

mecab_dll.obj: mecab.cpp
	$(CC) $(CFLAGS_DLL) /c mecab.cpp /Fo$@

nbest_generator_dll.obj: nbest_generator.cpp
	$(CC) $(CFLAGS_DLL) /c nbest_generator.cpp /Fo$@

param_dll.obj: param.cpp
	$(CC) $(CFLAGS_DLL) /c param.cpp /Fo$@

string_buffer_dll.obj: string_buffer.cpp
	$(CC) $(CFLAGS_DLL) /c string_buffer.cpp /Fo$@

tagger_dll.obj: tagger.cpp
	$(CC) $(CFLAGS_DLL) /c tagger.cpp /Fo$@

tokenizer_dll.obj: tokenizer.cpp
	$(CC) $(CFLAGS_DLL) /c tokenizer.cpp /Fo$@

utils_dll.obj: utils.cpp
	$(CC) $(CFLAGS_DLL) /c utils.cpp /Fo$@

viterbi_dll.obj: viterbi.cpp
	$(CC) $(CFLAGS_DLL) /c viterbi.cpp /Fo$@

writer_dll.obj: writer.cpp
	$(CC) $(CFLAGS_DLL) /c writer.cpp /Fo$@

clean:
	del *.exe
	del *.lib
	del *.obj
	del *.dll
