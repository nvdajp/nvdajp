# -*- coding: utf-8 -*-
#jptools/jpBrailleRunner.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 Masataka.Shinke, Takuya Nishimoto
# h1: カナと記号のテスト
# h2: テキスト解析とマスあけのテスト

# from __future__ import unicode_literals
import sys
sys.path.append(r'..\source\synthDrivers\jtalk')
from harness import tests
import os
import sys
import optparse
import datetime
import cStringIO
import timeit

jtalk_dir = os.path.join(os.getcwdu(), '..', 'source', 'synthDrivers', 'jtalk')
sys.path.append(jtalk_dir)

import translator1
import translator2

def __write(file, s=""):
	file.write(s.encode('utf-8', 'ignore'))

def __writeln(file, s=""):
	file.write(s.encode('utf-8', 'ignore') + "\n")

output = None

def __print(s=""):
	global output
	output.write(s.encode('utf-8', 'ignore') + "\n")

def dot_numbers(s):
	ret = []
	for c in s:
		code = ord(c)
		if code == 0x20 or code == 0x2800:
			ret.append('0')
		elif 0x2801 <= code and code <= 0x28ff:
			ar = []
			if code & 0x01: ar.append('1')
			if code & 0x02: ar.append('2')
			if code & 0x04: ar.append('3')
			if code & 0x08: ar.append('4')
			if code & 0x10: ar.append('5')
			if code & 0x20: ar.append('6')
			if code & 0x40: ar.append('7')
			if code & 0x80: ar.append('8')
			ret.append(u''.join(ar))
	return u' '.join(ret)

def pass1():
	global output
	outfile = '__h1output.txt'
	with open(outfile, 'w') as f:
		count = 0
		for t in tests:
			if t.has_key('output'):
				result, inpos1 = translator1.translateWithInPos(t['input'])
				if t.has_key('inpos1'):
					correct_inpos1 = ','.join(['%d' % n for n in t['inpos1'] ])
				else:
					correct_inpos1 = None
				result_inpos1 = ','.join(['%d' % n for n in inpos1])
				if result != t['output'] or \
						(correct_inpos1 and result_inpos1 != correct_inpos1) or \
						(len(result) != len(inpos1)):
					count+=1 
					f.write("input: " + t['input'].encode('utf-8') + "\n")
					f.write("result: " + result.encode('utf-8') + "\n")
					f.write("correct: " + t['output'].encode('utf-8') + "\n")
					if correct_inpos1:
						f.write("correct_inpos1: " + correct_inpos1 + "\n")
					f.write("result_inpos1: " + result_inpos1 + "\n")
					if 'comment' in t:
						f.write("comment: " + t['comment'].encode('utf-8') + "\n")
					f.write("\n")
		print 'h1: %d error(s). see %s' % (count, outfile)
	
def pass2(verboseMode=False):
	global output
	outfile = '__h2output.txt'
	with open(outfile, 'w') as f:
		output = cStringIO.StringIO()
		translator2.initialize(jtalk_dir, __print)
		log = output.getvalue()
		output.close()
		f.write(log)
		f.write("\n")
		count = 0
		for t in tests:
			if t.has_key('text'):
				output = cStringIO.StringIO()
				result, pat, inpos1, inpos2 = translator2.translateWithInPos2(
					t['text'], logwrite=__print)
				log = output.getvalue()
				output.close()
				# inpos2
				if t.has_key('inpos2'):
					correct_inpos2 = ','.join(['%d' % n for n in t['inpos2'] ])
				else:
					correct_inpos2 = None
				# inpos1
				if t.has_key('inpos1'):
					correct_inpos1 = ','.join(['%d' % n for n in t['inpos1'] ])
				else:
					correct_inpos1 = None
				# merged inpos
				inpos, outpos = translator2.mergePositionMap(
					inpos1, inpos2, len(pat), len(t['text']))
				if t.has_key('inpos'):
					correct_inpos = ','.join(['%d' % n for n in t['inpos'] ])
				else:
					correct_inpos = None
				# result
				result_inpos2 = ','.join(['%d' % n for n in inpos2])
				result_inpos1 = ','.join(['%d' % n for n in inpos1])
				result_inpos  = ','.join(['%d' % n for n in inpos])
				result_outpos = ','.join(['%d' % n for n in outpos])
				# output
				isError = False
				if result != t['input'] or \
						(correct_inpos2 and result_inpos2 != correct_inpos2) or \
						(correct_inpos and result_inpos != correct_inpos):
					isError = True
					count+=1 
				if isError or verboseMode:
					f.write("text   : " + t['text'].encode('utf-8') + "\n")
					f.write("correct: " + t['input'].encode('utf-8') + "\n")
					f.write("result : " + result.encode('utf-8') + "\n")
					f.write("pat    : " + pat.encode('utf-8') + "\n")
					if correct_inpos2:
						f.write("cor_in2: " + correct_inpos2 + "\n")
					if correct_inpos1:
						f.write("cor_in1: " + correct_inpos1 + "\n")
					if correct_inpos:
						f.write("cor_in : " + correct_inpos + "\n")
					f.write("res_in2: " + result_inpos2 + "\n")
					f.write("res_in1: " + result_inpos1 + "\n")
					f.write("res_in : " + result_inpos + "\n")
					f.write("res_out: " + result_outpos + "\n")
					if 'comment' in t and t['comment']:
						f.write("comment: " + t['comment'].encode('utf-8') + "\n")
					f.write("\n")
					f.write(log)
					f.write("\n")
		print 'h2: %d error(s). see %s' % (count, outfile)

def make_doc():
	outfile = '__jpBrailleHarness.t2t'
	timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
	with open(outfile, 'w') as f:
		__writeln(f, u"""
NVDA 日本語版 点訳テストケース """ + timestamp + u"""

%!Target: xhtml
%!Encoding: UTF-8

目次
%%toc

""")
		count = 0
		for t in tests:
			# 'note' はテストケースではなく説明の記述
			if t.has_key('note'):
				__writeln(f)
				__writeln(f, t['note'])
				__writeln(f)
				continue
			count += 1
			__writeln(f, u"番号: %d" % count)
			
			if t.has_key('text'):
				__writeln(f, u"- 日本語: " + t['text'].replace(u'　', u'□').replace(' ', u'□'))
			if t.has_key('input'):
				__writeln(f, u"- カナ表記: " + t['input'].replace(' ', u'□'))
			if t.has_key('output'):
				__writeln(f, u"- 点字: " + t['output'].replace(' ', u'□'))
			if t.has_key('output'):
				__writeln(f, u"- ドット番号: " + dot_numbers(t['output']))
			if t.has_key('comment'):
				__writeln(f, u"- コメント: " + t['comment'])
			__writeln(f, u"-")

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option("-1", "--pass1only",
					  action="store_true",
					  dest="pass1_only",
					  default="False",
					  help="pass1 only timeit")
	parser.add_option("-2", "--pass2only",
					  action="store_true",
					  dest="pass2_only",
					  default="False",
					  help="pass2 only timeit")
	parser.add_option("-v", "--verbose",
					  action="store_true",
					  dest="verbose",
					  default="False",
					  help="pass2 only timeit")
	parser.add_option("-m", "--makedoc",
					  action="store_true",
					  dest="make_doc",
					  default="False",
					  help="make t2t document of harness")
	parser.add_option("-n", "--number",
					  action="store",
					  dest="number",
					  type="int",
					  default=1,
					  help="number for timeit")
	parser.add_option("-o", "--outposTest",
					  action="store_true",
					  dest="outpos_test",
					  default=False,
					  help="outpos test")
	(options, args) = parser.parse_args()

	if options.outpos_test == True:
		# translate([b'louis/tables/en-us-g2.ctb'], 'Hello world!')
		inPos  = [0, 0, 1, 2, 3, 4, 5, 6, 6, 11]
		inlen  = len('Hello world!')
		outlen = len(',hello _w6')
		outPos = translator2.makeOutPos(inPos, inlen, outlen)
		print outPos 
		assert outPos == [1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 9]
	elif options.make_doc == True:
		make_doc()
	elif options.pass1_only == True:
		t = timeit.Timer(stmt=pass1)
		print t.timeit(number=options.number)
	elif options.pass2_only == True:
		t = timeit.Timer(stmt=pass2)
		print t.timeit(number=options.number)
	elif options.verbose == True:
		pass2(verboseMode=True)
	else:
		pass1()
		pass2()

