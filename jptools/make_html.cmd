python jpBrailleRunner.py -m
python ..\txt2tags.py -t xhtml --toc __jpBrailleHarness.t2t
python -c "import sys;lines = [line.strip() for line in sys.stdin.readlines()];import re;p = re.compile(r'<a href=\x22(mailto|http):[^>]+>([^<]+)</a>');print '\n'.join(map(lambda l:p.sub(r'\2', l), lines))" < __jpBrailleHarness.xhtml > c:\users\nishimotz\dropbox\public\jpBrailleHarness.xhtml
