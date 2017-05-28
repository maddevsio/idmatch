# idmatch

## System requirements:
Ensure you have enough RAM. I failed to build opencv with 1gb of RAM, works OK with 6gb of RAM.
compiler tools and needed libraries

### Opencv3:

```
$ sudo apt-get install build-essential
$ sudo apt-get install libtool autoconf
$ sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
$ sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
```

Get fresh opencv:
Select stable version 3.2.0 for development:

```
$ cd ~/<my_working_directory>
$ git clone https://github.com/opencv/opencv.git
$ wget https://github.com/opencv/opencv/archive/3.2.0.tar.gz
$ cd opencv-3.2.0
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local  ..
$ make -j3
$ sudo make install
```

### Tesseract OCR:

```
$ sudo apt-get install tesseract-ocr
$ sudo apt-get install tesseract-ocr-kir 
```

### Caffe v1.0

Ubuntu installation:
```
sudo apt-get install python-dev python-pip build-essential  
sudo apt-get install libatlas-base-dev libopenblas-dev  
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler  
sudo apt-get install --no-install-recommends libboost-all-dev  
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev  
```
Compilation:
```
$ wget https://github.com/BVLC/caffe/archive/1.0.tar.gz
tar xvf 1.0.tar.gz
cd caffe-1.0/
cp Makefile.config.sample Makefile.config
```
Be sure to set your Python paths in Makefile.config first.

Update this strings in Makefile.config:
```
-# CPU_ONLY := 1
-# OPENCV_VERSION := 3
-INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
-LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib

+CPU_ONLY := 1
+OPENCV_VERSION := 3
+INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/
+LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial/
```

After changing Makefile.config:
```
make all -j4
make test
make runtest
```
Python bindings:

```
pip install numpy
make pycaffe
```

Caffe levels are:
```
0 - debug
1 - info (still a LOT of outputs)
2 - warnings
3 - errors
export GLOG_minloglevel = '3'
```

### Application requirements:
pip install -r requirements.txt

## Usage:

Command line interface:
```
# Running CLI
$ ./cli.py --img <path/to/image>
$ ./cli.py --help
```

Running web server
```
$ gunicorn web.server:app -b 127.0.0.1:8000
```
