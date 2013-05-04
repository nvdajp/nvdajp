python jpBrailleRunner.py -m
python ..\txt2tags.py -t xhtml --toc __jpBrailleHarness.t2t
python -c "import sys;lines = [line.strip() for line in sys.stdin.readlines()];import re;p1 = re.compile('\<a href=[^\>]+\>');p2 = re.compile('\<\/a\>');print '\n'.join(map(lambda l:p2.sub('', p1.sub('', l)), lines))" < __jpBrailleHarness.xhtml > c:\users\nishimotz\dropbox\public\jpBrailleHarness.xhtml
