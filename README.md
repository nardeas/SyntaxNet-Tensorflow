# Tensorflow SyntaxNet/DRAGNN

[![Pulls](https://img.shields.io/docker/pulls/nardeas/tensorflow-syntaxnet.svg?style=flat-square)](https://img.shields.io/docker/pulls/nardeas/tensorflow-syntaxnet.svg?style=flat-square)
[![Stars](https://img.shields.io/docker/stars/nardeas/tensorflow-syntaxnet.svg?style=flat-square)](https://img.shields.io/docker/stars/nardeas/tensorflow-syntaxnet.svg?style=flat-square)
[![Size](https://img.shields.io/imagelayers/image-size/nardeas/tensorflow-syntaxnet/latest.svg?style=flat-square)](https://img.shields.io/imagelayers/image-size/nardeas/tensorflow-syntaxnet/latest.svg?style=flat-square)

> `docker pull nardeas/tensorflow-syntaxnet:latest`

Minimal Docker image based on Alpine with Tensorflow and SyntaxNet/DRAGNN support.

This is a production ready base image for your ML needs. Build your TF apps on top of this lean image to get the most out of your precious disk space.

Build typically takes 1-1.5 hours on a 2017 MacBook Pro.

**Total size:** ~421MB  
**Tensorflow version:** 1.3.0-rc2  
**Python version:** 2.7.14

Note that the Tensorflow version depends on what is supported by SyntaxNet. Building a working SN installation requires some additional operations not supported by TF as is.

## hub.docker.com

You can pull the image from [DockerHub](https://hub.docker.com/r/nardeas/ssh-agent/) via

```
docker pull nardeas/tensorflow-syntaxnet:latest
```

## How to actually use

You can create your own image for your TF/SyntaxNet application by using this as base image.

I recommend building with a SyntaxNet wrapper and some pre-trained models to make development easier.

You can obviously train your own models as well. Please note that this version doesn't include GPU support.

[Here's an example wrapper for Python](https://github.com/short-edition/syntaxnet-wrapper)

The above wrapper will automatically download pre-trained [Parsey Universal](https://github.com/tensorflow/models/blob/master/research/syntaxnet/g3doc/universal.md) models for you. Please refer to the [README](https://github.com/short-edition/syntaxnet-wrapper/blob/master/README.md) on how to use it.

## Notes

This image contains a full Tensorflow installation. Any readily available SyntaxNet models are excluded from this image to keep it as lean as possible. Having SyntaxNet support doesn't produce much overhead so this image is well suited for use with any other TF applications as well.
