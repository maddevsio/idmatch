FROM ubuntu:16.04

RUN set -ex \
  && apt-get update \
	&& apt-get install --no-install-recommends -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN set -ex \
  && mkdir -p /webapp/idmatch/matching/model/ \
  && wget http://www.robots.ox.ac.uk/~vgg/software/vgg_face/src/vgg_face_caffe.tar.gz \
  && tar xzf vgg_face_caffe.tar.gz -C /webapp/idmatch/matching/model/

VOLUME /webapp/idmatch/matching/model/
