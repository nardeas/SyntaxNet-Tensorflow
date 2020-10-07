# Tensorflow SyntaxNet/DRAGNN

[![Pulls](https://img.shields.io/docker/pulls/nardeas/tensorflow-syntaxnet.svg)](https://img.shields.io/docker/pulls/nardeas/tensorflow-syntaxnet.svg?style=flat-square)
[![Stars](https://img.shields.io/docker/stars/nardeas/tensorflow-syntaxnet.svg)](https://img.shields.io/docker/stars/nardeas/tensorflow-syntaxnet.svg?style=flat-square)
[![](https://images.microbadger.com/badges/image/nardeas/tensorflow-syntaxnet.svg)](https://microbadger.com/images/nardeas/tensorflow-syntaxnet "Get your own image badge on microbadger.com")

> `docker pull nardeas/tensorflow-syntaxnet`

Minimal Docker image based on Alpine with Tensorflow and SyntaxNet/DRAGNN support.

This is a production ready base image for your ML needs. Build your TF apps on top of this lean image to get the most out of your precious disk space.

Build typically takes 1-1.5 hours on a 2017 MacBook Pro.

**Compressed size:** ~190MB   
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

You can create your own image for your TF application by using this as base image.

Included is an easy to use DRAGNN wrapper that works with the pre-trained CoNLL17 models. Here is a reference how you can [download the models](https://github.com/tiangolo/tensorflow-models/tree/master/research/syntaxnet/g3doc/conll2017).

[[Direct link to models archive]](https://drive.google.com/file/d/0BxpbZGYVZsEeSFdrUnBNMUp1YzQ/view)

You can obviously train your own models as well. Please note that this version doesn't include GPU support.

### Wrapper

The included DRAGNN wrapper is built into `/usr/lib/python2.7/site-packages/dragnn/wrapper` so you can simply do:

```python
from dragnn.wrapper import SyntaxNet
sn = SyntaxNet(lang="English", model_dir="/path/to/model/dir", logging=False)
sn.parse("This is an example")
```

It will output a dict:

```
{
  "input": "This is an example",
  "output": [
    {
      "break_level": 0,
      "category": "",
      "dep": "nsubj",
      "fpos": "PRON++DT",
      "head": 3,
      "label": "nsubj",
      "number": "Sing",
      "pos_tag": "DT",
      "prontype": "Dem",
      "word": "This"
    },
    {
      ...
```

Note that `lang` is the subfolder name in `model_dir` which should contain the language specific segmenter and parser models. The default directory to search for models is `/usr/local/tfmodels/`. If you have downloaded and extracted the `conll17.zip` via the instructions above, you can launch the container like this:

```
# Mount the extracted models dir on host machine as volume in container

docker run -it -v <path/to/extracted/zip>:/usr/local/tfmodels/ nardeas/tensorflow-syntaxnet
```

and the above example should work out of the box. Only provide `lang` parameter to constructor (default "English").

## Notes

This image contains a full Tensorflow installation. Any readily available pre-trained models are excluded from this image to keep it as lean as possible. Having SyntaxNet support doesn't produce much overhead so this image is well suited for use with any other TF applications as well.

Also note that this version doesn't include Bazel ops from the original SN. In other words you won't use stuff like `bazel-bin/syntaxnet/parser_eval` - you should use DRAGNN parser instead. The easiest way to get up and running fast is using the included DRAGNN wrapper.
