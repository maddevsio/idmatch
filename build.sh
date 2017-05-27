mkdir tmp
cd tmp/
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

cd opencv_contrib/
git checkout 8634252

cd ../opencv/
git checkout 70bbf17

mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules/  ..
make -j3
sudo make install

cd ../

rm -rf opencv*
