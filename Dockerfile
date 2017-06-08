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
          python-setuptools \
  && pip install --upgrade pip \
  && pip install Cython==0.25.2 \
  && pip install numpy==1.11.0 \
  && mkdir -p /tmp/opencv/build /tmp/opencv_contrib \
  && curl -Ls ${SOURCE_URL} | tar -xz --strip=1 -C /tmp/opencv \
  && curl -Ls ${CONTRIB_URL} | tar -xz --strip=1 -C /tmp/opencv_contrib \
  && cd /tmp/opencv/build \
  && cmake \
      -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D BUILD_PYTHON_SUPPORT=ON \
      -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib/modules/ .. \
  && make -j "$(nproc)" && make install && ldconfig \
  && cd / && rm -rf /tmp/* \
  && rm -rf /var/lib/apt/lists/*

ENV UWSGI_CPU_AFFINITY 2
ENV UWSGI_PROCESSES 4
ENV UWSGI_HARAKIRI 60

WORKDIR /webapp
COPY requirements.txt /webapp
RUN pip install -r requirements.txt
COPY . /webapp

WORKDIR /webapp/web
EXPOSE 8080

CMD ["uwsgi", "--ini", "uwsgi.ini"]
