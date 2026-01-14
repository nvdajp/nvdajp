include/jtalk: libopenjtalk.dll source code 

2012-07-14 by Takuya Nishimoto (nishimotz at gmail.com)

libopenjtalk can be compiled as follows:

(1) type "cd include\jtalk"
(2) type "setenv-x86"
(3) type "all-clean", "all-build"
(4) type "all-install" to copy to source/synthDrivers/jtalk/
(4) for clean up, type "all-clean" again

or use open "CMD Shell Windows SDK x86" (nmake required)

Notice:

(1) libopenjtalk.dll does not include Mecab functions.

(2) setenv-x86 uses "C:\Program Files\Microsoft SDKs\Windows\v7.1\bin\setenv.cmd"

[end of file]
