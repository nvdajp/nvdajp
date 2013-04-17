python jpBrailleRunner.py -m
python ..\txt2tags.py -t html --toc __jpBrailleHarness.t2t
rem move __jpBrailleHarness.html jpBrailleHarness.html
copy __jpBrailleHarness.html c:\users\nishimotz\dropbox\public\jpBrailleHarness.html
