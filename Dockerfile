FROM ubuntu:16.04

MAINTAINER MadDevs <rock@maddevs.io>

ENV OPENCV_VER 3.2.0
ENV SOURCE_URL https://github.com/opencv/opencv/archive/${OPENCV_VER}.tar.gz
ENV CONTRIB_URL https://github.com/opencv/opencv_contrib/archive/${OPENCV_VER}.tar.gz

RUN set -ex \
  && apt-get update \
	&& apt-get install --no-install-recommends -y \
          build-essential \
          libtool \
          autoconf \
          automake \
          pkg-config \
          cmake \
          curl \
          libatlas-base-dev \
          libboost-all-dev \
          libgflags-dev \
          libgoogle-glog-dev \
          libhdf5-serial-dev \
          libleveldb-dev \
          liblmdb-dev \
          libopencv-dev \
          libprotobuf-dev \
          libsnappy-dev \
          protobuf-compiler \
          libtbb2 \
          libdc1394-22-dev \
          libdc1394-22-dev \
          libleptonica-dev \
          libgtk2.0-dev \
          libavcodec-dev \
          libavformat-dev \
          libswscale-dev \
          libtbb-dev \
          libjpeg-dev \
          libpng-dev \
          libtiff-dev \
          libjasper-dev \
          libtesseract-dev \
          tesseract-ocr \
          tesseract-ocr-eng \
          tesseract-ocr-rus \
          tesseract-ocr-kir \
          python2.7-dev \
          python-pip \
          python-numpy \
          python-setuptools \
          python-scipy \
  && pip install --upgrade pip \
  && pip install Cython==0.25.2 \
  && rm -rf /var/lib/apt/lists/*

# install opencv
RUN mkdir -p /tmp/opencv/build /tmp/opencv_contrib \
  && curl -Ls ${SOURCE_URL} | tar -xz --strip=1 -C /tmp/opencv \
  && curl -Ls ${CONTRIB_URL} | tar -xz --strip=1 -C /tmp/opencv_contrib \
  && cd /tmp/opencv/build \
  && cmake \
      -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D BUILD_PYTHON_SUPPORT=ON \
      -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib/modules/ .. \
  && make -j "$(nproc)" && make install && ldconfig \
  && cd / && rm -rf /tmp/*

# install caffe
ENV CAFFE_VER 1.0
ENV CAFFE_SRC /tmp/caffe
RUN set -ex \
  && mkdir -p ${CAFFE_SRC}/build \
  && curl -Ls https://github.com/BVLC/caffe/archive/${CAFFE_VER}.tar.gz | tar -xz --strip=1 -C ${CAFFE_SRC} \
  && for req in $(cat ${CAFFE_SRC}/python/requirements.txt) pydot; do pip install $req; done \
  && cd ${CAFFE_SRC}/build \
  && cmake \
      -DCPU_ONLY=1 \
      -DOPENCV_VERSION=3 \
      -D CMAKE_INSTALL_PREFIX=/usr/local .. \
  && make -j"$(nproc)" && make install && ldconfig \
  && cd / && rm -rf /tmp/*

ENV PYCAFFE_ROOT /usr/local/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH

ENV UWSGI_CPU_AFFINITY 2
ENV UWSGI_PROCESSES 4
ENV UWSGI_HARAKIRI 60

WORKDIR /webapp
COPY requirements.txt /webapp
RUN pip install -r requirements.txt
COPY . /webapp
RUN mkdir -p /webapp/web/uploads

WORKDIR /webapp/web
EXPOSE 8080

CMD ["uwsgi", "--ini", "uwsgi.ini"]
