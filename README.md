# Tensorflow SyntaxNet/DRAGNN

[![Pulls](https://img.shields.io/docker/pulls/nardeas/tensorflow-syntaxnet.svg?style=flat-square)](https://img.shields.io/docker/pulls/nardeas/tensorflow-syntaxnet.svg?style=flat-square)
[![Stars](https://img.shields.io/docker/stars/nardeas/tensorflow-syntaxnet.svg?style=flat-square)](https://img.shields.io/docker/stars/nardeas/tensorflow-syntaxnet.svg?style=flat-square)
[![Size](https://img.shields.io/imagelayers/image-size/nardeas/tensorflow-syntaxnet/latest.svg?style=flat-square)](https://img.shields.io/imagelayers/image-size/nardeas/tensorflow-syntaxnet/latest.svg?style=flat-square)

> `docker pull nardeas/tensorflow-syntaxnet`

Minimal Docker image based on Alpine with Tensorflow and SyntaxNet/DRAGNN support.

This is a production ready base image for your ML needs. Build your TF apps on top of this lean image to get the most out of your precious disk space.

Build typically takes 1-1.5 hours on a 2017 MacBook Pro.

**Compressed size:** ~199MB  
**Total size:** ~421MB  
**Tensorflow version:** 1.3.0-rc2  
**Python version:** 2.7.14

Note that the Tensorflow version depends on what is supported by [SyntaxNet](https://github.com/tensorflow/models/tree/master/research/syntaxnet). Building a working SN installation requires some additional operations not supported by TF as is.

**This version uses the latest DRAGNN mode, which is much faster than the original SyntaxNet implementation!**

## hub.docker.com

You can pull the image from [DockerHub](https://hub.docker.com/r/nardeas/tensorflow-syntaxnet/) via

```
docker pull nardeas/tensorflow-syntaxnet:latest
```

## How to actually use

You can create your own image for your TF/DRAGNN application by using this as base image.

I recommend building with a DRAGNN wrapper and some pre-trained models to make development easier.

You can obviously train your own models as well. Please note that this version doesn't include GPU support.

[Here's a good example with DRAGNN wrapper](https://github.com/ljm625/syntaxnet-rest-api) to build real applications.

Here you can download pre-trained [Parsey Universal](https://github.com/tensorflow/models/blob/master/research/syntaxnet/g3doc/universal.md) models.

## Notes

This image contains a full Tensorflow installation. Any readily available pre-trained models are excluded from this image to keep it as lean as possible. Having SyntaxNet support doesn't produce much overhead so this image is well suited for use with any other TF applications as well.

Also note that this version doesn't include Bazel ops from the original SN. In other words you won't use stuff like `bazel-bin/syntaxnet/parser_eval` - you should use DRAGNN parser instead.

*e.g load op definitions with:*

```python
from dragnn.python import load_dragnn_cc_impl
```
