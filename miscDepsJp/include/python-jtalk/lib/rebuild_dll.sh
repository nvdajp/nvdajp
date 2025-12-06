# for cygwin gcc3
export CXX='g++ -mno-cygwin'
export CC='gcc -mno-cygwin'
if [ -f /usr/bin/set-gcc-default-3.sh ] ; then
  bash /usr/bin/set-gcc-default-3.sh
fi
echo 'building htsengineapi'
pushd ../../htsengineapi
  if [ -f Makefile ] ; then
    make clean
  fi
  autoreconf
  autoconf
  ./configure --build=i686-pc-mingw32
  make
popd
echo 'building libopenjtalk'
pushd ..
  if [ -f Makefile ] ; then
    make clean
  fi
  autoreconf
  autoheader
  aclocal
  automake
  autoconf
  bash do_configure_mingw32.sh
  # autoconf
  make
popd
echo 'building DLL'
make -f Makefile.mingw32 clean
make -f Makefile.mingw32 clean-dll htsengineapi njd_set_unvoiced_vowel libjpcommon libopenjtalk.dll
strip libopenjtalk.dll
