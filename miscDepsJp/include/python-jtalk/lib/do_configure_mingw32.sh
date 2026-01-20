# usage:
# sh /usr/bin/set-gcc-default-3.sh
# sh do_configure_mingw32.sh
# autoconf
# make
# cd lib
# make -f Makefile.mingw32 clean
# make -f Makefile.mingw32
# strip libopenjtalk.dll
export CXX='g++ -mno-cygwin'
export CC='gcc -mno-cygwin'
HTSENGINE_DIR=/cygdrive/c/work/github/htsengineapi
./configure --with-hts-engine-header-path=$HTSENGINE_DIR/include \
  --with-hts-engine-library-path=$HTSENGINE_DIR/lib \
  --build=i686-pc-mingw32 --with-charset=shift_jis 
