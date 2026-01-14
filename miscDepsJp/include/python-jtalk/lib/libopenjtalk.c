/* libopenjtalk.c
 * for nvdajp & Open JTalk 1.07
 * 2013-12-26 by Takuya Nishimoto
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>

/* Main headers */
#include "njd.h"
#include "jpcommon.h"
#include "HTS_engine.h"

/* Sub headers */
#include "text2mecab.h"
#include "mecab2njd.h"
#include "njd_set_pronunciation.h"
#include "njd_set_digit.h"
#include "njd_set_accent_phrase.h"
#include "njd_set_accent_type.h"
#include "njd_set_unvoiced_vowel.h"
#include "njd_set_long_vowel.h"
#include "njd2jpcommon.h"

#include "libopenjtalk-timestamp.h"

static short *m_buf = NULL;
static size_t m_samples = 0;
static size_t m_buf_size = 0;

char *jt_version()
{
    return JT_VERSION;
}

void jt_save_logs(char *filename, HTS_Engine *engine, NJD *njd)
{
    FILE *logfp;
    logfp = fopen(filename, "at");
    if (logfp != NULL) {
         fprintf(logfp, "[Text analysis result]\n");
         NJD_fprint(njd, logfp);
         fprintf(logfp, "\n[Output label]\n");
         HTS_Engine_save_label(engine, logfp);
         fprintf(logfp, "\n");
         HTS_Engine_save_information(engine, logfp);
         fprintf(logfp, "\n");
         fprintf(logfp, "\n");
    }
    fclose(logfp);
}

void jt_save_riff(char *filename, HTS_Engine *engine)
{
    FILE *wavfp;
    wavfp = fopen(filename, "wb");
    if (wavfp != NULL) {
        HTS_Engine_save_riff(engine, wavfp);
    }
    fclose(wavfp);
}

short *jt_speech_ptr()
{
	return m_buf;
}

static void speech_normalize(short level)
{
	int i;
	const int MAX_LEVEL = 32767;
#if 1
	const int max = 32767;
#else
	short max = 0;
	level = abs(level);
	for (i = 0; i < m_samples; i++) {
		int a;
		a = abs(m_buf[i]);
		if (max < a) max = a;
	}
#endif
	for (i = 0; i < m_samples; i++) {
		float f, g;
		f = (float)m_buf[i];
		g = f * level / max;
		if (g > MAX_LEVEL) {
			m_buf[i] = MAX_LEVEL;
		} else if (g < -MAX_LEVEL) {
			m_buf[i] = -MAX_LEVEL;
		} else {
			m_buf[i] = (short)g;
		}
	}
}

/* apply to m_buf[] */
static void trim_silence(short begin_thres, short end_thres)
{
	int i, size;
	int begin_pos = 0, end_pos = 0;
	if (begin_thres >= 0) {
		begin_thres = abs(begin_thres);
		for (i = 0; i < m_samples; i++) {
			if (abs(m_buf[i]) > begin_thres) {
				begin_pos = i;
				break;
			}
		}
	}
	end_pos = m_samples - 1;
	if (end_thres >= 0) {
		end_thres = abs(end_thres);
		for (i = m_samples - 1; i > begin_pos; i--) {
			if (abs(m_buf[i]) > end_thres) {
				end_pos = i;
				break;
			}
		}
	}
	size = end_pos - begin_pos + 1;
	memmove(m_buf, &(m_buf[begin_pos]), sizeof(short) * size);
	m_samples = size;
}

/* returns: new sample count */
int jt_speech_prepare(
	double * gsp,
	size_t ns,
	short begin_thres,
	short end_thres,
	short level)
{
	size_t i;
	double x;
	short temp;

	// prepare buffer
	if (m_buf_size < ns) {
		m_buf_size = ns;
		if (m_buf == NULL) {
			m_buf = (short *)malloc(m_buf_size * sizeof(short));
		} else {
			m_buf = (short *)realloc(m_buf, m_buf_size * sizeof(short));
		}
	}
	if (m_buf == NULL) {
		m_samples = 0;
		m_buf_size = 0;
		return 0;
	}

	// double to short
	for (i = 0; i < ns; i++) {
		x = gsp[i];
		if (x > 32767.0)
			temp = 32767;
		else if (x < -32768.0)
			temp = -32768;
		else
			temp = (short) x;
		m_buf[i] = temp;
	}
	m_samples = ns;

	trim_silence(begin_thres, end_thres);
	speech_normalize(level);
	return m_samples;
}

void jt_buf_clean()
{
	if (m_buf) {
		free(m_buf);
		m_buf = NULL;
		m_samples = 0;
		m_buf_size = 0;
	}
}
