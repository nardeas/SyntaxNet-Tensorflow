import os
import re

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from dragnn.protos import spec_pb2
from dragnn.python import graph_builder
from dragnn.python import spec_builder
from dragnn.python import load_dragnn_cc_impl
from google.protobuf import text_format

from syntaxnet import sentence_pb2
from syntaxnet.ops import gen_parser_ops

# /usr/lib/python2.7/site-packages/h5py/__init__.py:36: FutureWarning:
# Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated.
import warnings
warnings.filterwarnings("ignore")

# TODO: Functionality to automatically download CoNLL models
class ModelFetcher:
    def __init__(self, model_dir="/usr/local/tfmodels"):
        pass

    def download(self, lang):
        pass

class SyntaxNet(object):

    def __init__(self, lang="English", model_dir="/usr/local/tfmodels/", logging=False):
        if not logging:
            tf.logging.set_verbosity(tf.logging.ERROR)
        self.segmenter = self.load_model(os.path.join(model_dir, lang, "segmenter"), "spec.textproto")
        self.parser = self.load_model(os.path.join(model_dir, lang), "parser_spec.textproto")

    def rename_vars(self, base_dir, checkpoint_name="checkpoint"):
        new_checkpoint_vars = {}
        reader = tf.train.NewCheckpointReader(os.path.join(base_dir, checkpoint_name))
        for old_name in reader.get_variable_to_shape_map():
            if old_name.endswith("weights"):
                new_name = old_name.replace("weights", "kernel")
            else:
                new_name = old_name
            new_checkpoint_vars[new_name] = tf.Variable(reader.get_tensor(old_name))

        saver = tf.train.Saver(new_checkpoint_vars)
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.save(sess, os.path.join(base_dir, "new." + checkpoint_name))
            for filename in os.listdir(base_dir):
                if "checkpoint" in filename:
                    if not "new." and not ".old" in filename:
                        os.rename(os.path.join(base_dir, filename), os.path.join(base_dir, "old." + filename))
                    if "new." in filename:
                        os.rename(os.path.join(base_dir, filename), os.path.join(base_dir, filename.replace("new.", "")))

    def load_model(self, base_dir, master_spec_name, checkpoint_name="checkpoint", rename=True):
        try:
            master_spec = spec_pb2.MasterSpec()
            with open(os.path.join(base_dir, master_spec_name)) as f:
                text_format.Merge(f.read(), master_spec)
            spec_builder.complete_master_spec(master_spec, None, base_dir)

            graph = tf.Graph()
            with graph.as_default():
                hyperparam_config = spec_pb2.GridPoint()
                builder = graph_builder.MasterBuilder(master_spec, hyperparam_config)
                annotator = builder.add_annotation(enable_tracing=True)
                builder.add_saver()

            sess = tf.Session(graph=graph)
            with graph.as_default():
                builder.saver.restore(sess, os.path.join(base_dir, checkpoint_name))

            def annotate_sentence(sentence):
                with graph.as_default():
                    return sess.run([annotator['annotations'], annotator['traces']],
                                    feed_dict={annotator['input_batch']: [sentence]})
        except:
            if rename:
                self.rename_vars(base_dir, checkpoint_name)
                return self.load(base_dir, master_spec_name, checkpoint_name, False)
            raise Exception('Cannot load model: spec expects references to */kernel tensors instead of */weights.\
            Try running with rename=True or run rename_vars() to convert existing checkpoint files into supported format')

        return annotate_sentence

    def parse_attribute(self, input, todo_dict):
        pattern = re.compile(r'\"[^"]*\"')
        result = list(pattern.findall(input))
        for i in range(0, len(result), 2):
            todo_dict[filter(None, result[i].split('"'))[0].lower()] = filter(None, result[i + 1].split('"'))[0]
        return todo_dict

    def parse(self, sentence, raw=False):
        parsed = self.annotate(sentence)

        # Token format
        if raw == True:
            return [token for token in parsed.token]

        # Dict format
        else:
            result = {
                "input": parsed.text,
                "output": []
            }
            for token in parsed.token:
                temp = {
                    "word": token.word,
                    "label": token.label,
                    "dep": token.label,
                    "break_level": token.break_level,
                    "category": token.category,
                    "head": token.head
                }
                temp = self.parse_attribute(str(token.tag), temp)
                # Fix for getting back the pos_tag
                temp["pos_tag"] = temp["fpos"].split("++")[1]
                result["output"].append(temp)

            return result

    def annotate(self, text):
        sentence = sentence_pb2.Sentence(
            text=text,
            token=[sentence_pb2.Token(word=text, start=-1, end=-1)]
        )
        with tf.Session(graph=tf.Graph()) as tmp_session:
            char_input = gen_parser_ops.char_token_generator([sentence.SerializeToString()])
            preprocessed = tmp_session.run(char_input)[0]
        segmented, _ = self.segmenter(preprocessed)

        annotations, traces = self.parser(segmented[0])

        assert len(annotations) == 1
        assert len(traces) == 1

        return sentence_pb2.Sentence.FromString(annotations[0])

if __name__ == '__main__':
    import json
    sn = SyntaxNet()
    print json.dumps(sn.parse("This is an example"), sort_keys=True, indent=2)
