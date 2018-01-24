FROM alpine:3.7

ENV JAVA_HOME /usr/lib/jvm/default-jvm
ENV BAZEL_VERSION 0.5.4

WORKDIR /tmp

# Build directory trees
RUN mkdir -p /opt

# Build and install Tensorflow/SyntaxNet
RUN set -x \
    # Bazel
    && apk --no-cache --update add --virtual .builddeps.bazel \
        bash \
        build-base \
        linux-headers \
        python \
        openjdk8 \
        wget \
        zip \
    && mkdir /tmp/bazel \
    && wget -q -O /tmp/bazel-dist.zip https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-dist.zip \
    && unzip -q -d /tmp/bazel /tmp/bazel-dist.zip \
    && cd /tmp/bazel \
    # add -fpermissive compiler option to avoid compilation failure
    && sed -i -e '/"-std=c++0x"/{h;s//"-fpermissive"/;x;G}' tools/cpp/cc_configure.bzl \
    # add '#include <sys/stat.h>' to avoid mode_t type error
    && sed -i -e '/#endif  \/\/ COMPILER_MSVC/{h;s//#else/;G;s//#include <sys\/stat.h>/;G;}' third_party/ijar/common.h \
    # add jvm opts for circleci
    # && sed -i -E 's/(jvm_opts.*\[)/\1 "-Xmx1024m",/g' src/java_tools/buildjar/BUILD \
    && export EXTRA_BAZEL_ARGS="--jobs $(grep -c ^processor /proc/cpuinfo)" \
    && bash compile.sh \
    && cp output/bazel /usr/local/bin/ \
    # Syntaxnet with Tensorflow
    && cd /tmp \
    && apk --no-cache --update add \
      python \
      py-pip \
      jemalloc \
      libc6-compat \
    && apk --no-cache add \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
        hdf5 \
    && apk --no-cache add --virtual .builddeps.edge \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
        hdf5-dev \
    && apk --no-cache add --virtual .builddeps.tensorflow \
      git \
      bash \
      patch \
      perl \
      sed \
      swig \
      graphviz \
      python-dev \
      graphviz-dev \
    && pip install -U \
      wheel \
      mock \
      asciitree \
      numpy \
      h5py \
      autograd==1.1.13 \
      protobuf==3.3.0 \
      pygraphviz \
      backports.weakref \
    && git clone --recursive https://github.com/tensorflow/models.git \
    && cd /tmp/models/research/syntaxnet/tensorflow \
    && echo | \
        CC_OPT_FLAGS=-march=native \
        PYTHON_BIN_PATH=$(which python) \
        TF_NEED_MKL=0 \
        TF_NEED_VERBS=0 \
        TF_NEED_CUDA=0 \
        TF_NEED_GCP=0 \
        TF_NEED_JEMALLOC=0 \
        TF_NEED_HDFS=0 \
        TF_NEED_OPENCL=0 \
        TF_ENABLE_XLA=0 \
        ./configure \
    && cd .. \
    && CPU_COUNT=$(grep -c ^processor /proc/cpuinfo) \
    && bazel test --local_resources 4096,$CPU_COUNT,1.0 ... \
    && mkdir /tmp/syntaxnet_pkg \
    && bazel-bin/dragnn/tools/build_pip_package --output-dir=/tmp/syntaxnet_pkg --include-tensorflow \
    && pip install /tmp/syntaxnet_pkg/* \
    && cd /opt \
    # Cleanup
    && apk del \
        .builddeps.bazel \
        .builddeps.edge \
        .builddeps.tensorflow \
    && rm -rf /tmp/* \
    && rm -rf /root/.cache/*

WORKDIR /opt
CMD ["/bin/sh"]
