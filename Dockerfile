FROM ubuntu:24.04 AS base

RUN set -e

ENV DEBIAN_FRONTEND=noninteractive
ENV GIT_SSL_NO_VERIFY=1

# Install packages
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends\
        python3\
        python3-pip\
        g++\
        gcc\
        make\
        time\
        cmake\
        clang\
        python3-dev\
	curl\
        git

## Uncomment this for latex labels in plots
# WARNING: downloads cca 350 of archives
RUN apt-get install -y --no-install-recommends\
	texlive-latex-base\
	texlive-latex-extra

RUN apt-get install -y --no-install-recommends\
	ssh

COPY artifact-rv25 /opt/artifact
WORKDIR /opt/artifact/

RUN git clean -xdf
RUN git submodule update --init

# Setup the project for generating sHL monitors
WORKDIR /opt/artifact/hna
RUN git clean -xdf # in case it was not clean
RUN pip install --break-system-packages -r requirements.txt
RUN cmake . -DCMAKE_BUILD_TYPE=Release
RUN make -j2

# Setup the project for generating eHL monitors
WORKDIR /opt/artifact/hna-ifm24
RUN git clean -xdf # in case it was not clean
RUN cmake . -DCMAKE_BUILD_TYPE=Release -Dvamos_DIR=/opt/artifact/hna/vamos 
RUN make -j2

# Set up MPTs monitors
WORKDIR /opt/artifact/mpt
RUN cmake . -Dvamos_DIR=/opt/artifact/hna/vamos -DCMAKE_BUILD_TYPE=Release
RUN make -j2

# Set up RVHyper
WORKDIR /opt/artifact/rvhyper

## Set up SPOT for RVHyper
RUN curl -LRO https://www.lrde.epita.fr/dload/spot/spot-2.8.7.tar.gz
RUN tar xf spot-2.8.7.tar.gz
WORKDIR /opt/artifact/rvhyper/spot-2.8.7
RUN ./configure --enable-c++17 --disable-python --disable-debug && make -j2 && make install

# Continue with RVHyper
WORKDIR /opt/artifact/rvhyper
RUN make -j2

FROM base AS artifact-plots
RUN apt-get install -y --no-install-recommends\
	python3-matplotlib\
	python3-pandas\
	python3-seaborn

FROM artifact-plots AS artifact
WORKDIR /opt/artifact
