# for ubuntu 9.04
export CXX='g++'
export CC='gcc'
echo 'do not forget: sudo apt-get install autoconf libtool'
echo 'building htsengineapi'
pushd ../../htsengineapi
  # make clean
  autoreconf
  autoconf
  CC='gcc -fPIC' ./configure
  make clean
  make
popd
echo 'building libopenjtalk'
pushd ..
  # make clean
  autoreconf
  autoconf
  bash do_configure_ubuntu.sh
  make clean
  make
popd
echo 'building DLL'
make -f Makefile.ubuntu clean
make -f Makefile.ubuntu target
strip .libs/libopenjtalk.so.0.0.0

