# do_configure_ubuntu.sh
export CXX='g++'
export CC='gcc'
HTSENGINE=`pwd`/../htsengineapi
sh ./configure --with-hts-engine-header-path=$HTSENGINE/include \
  --with-hts-engine-library-path=$HTSENGINE/lib \
  --with-charset=shift_jis

