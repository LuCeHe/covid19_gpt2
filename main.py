import os

import tensorflow as tf
import tensorflow_datasets
from transformers import *

# Load dataset, tokenizer, model from pretrained model/vocabulary
from GenericTools.KerasTools.clr_callback import CyclicLR
from GenericTools.KerasTools.convenience_tools import plot_history
from GenericTools.SacredTools.VeryCustomSacred import CustomExperiment
from GenericTools.StayOrganizedTools.utils import email_results

CDIR = os.path.dirname(os.path.realpath(__file__))
ex = CustomExperiment('fineture_transformer', base_dir=CDIR, GPU=1)


@ex.config
def config():
    epochs = 0
    data_repeats = max(1, epochs)

@ex.automain
def main(epochs, data_repeats, _log):
    sacred_dir = os.path.join(*[CDIR, ex.observers[0].basedir, '1'])

    tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
    model = TFBertForSequenceClassification.from_pretrained('bert-base-cased')
    data = tensorflow_datasets.load('glue/mrpc')
    _log.info(data)

    # Prepare dataset for GLUE as a tf.data.Dataset instance
    train_dataset = glue_convert_examples_to_features(data['train'], tokenizer, max_length=128, task='mrpc')
    valid_dataset = glue_convert_examples_to_features(data['validation'], tokenizer, max_length=128, task='mrpc')
    train_dataset = train_dataset.shuffle(100).batch(64).repeat(data_repeats)
    valid_dataset = valid_dataset.batch(64).repeat(data_repeats)

    # Prepare training: Compile tf.keras model with optimizer, loss and learning rate schedule
    optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
    model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

    # Train and evaluate using tf.keras.Model.fit()
    history = model.fit(train_dataset, epochs=epochs, steps_per_epoch=115,
                        validation_data=valid_dataset, validation_steps=7)

    historyplotpath = os.path.join(*[sacred_dir, 'history.pdf'])
    plot_history(history, historyplotpath, epochs)

    print(model.inputs)

    # Load the TensorFlow model in PyTorch for inspection
    model.save_pretrained('./experiments/tmp/')
    #pytorch_model = BertForSequenceClassification.from_pretrained('./experiments/tmp/', from_tf=True)

    # Quickly test a few predictions - MRPC is a paraphrasing task, let's see if our model learned the task
    sentence_0 = "This research was consistent with his findings."
    sentence_1 = "His findings were compatible with this research."
    sentence_2 = "His findings were not compatible with this research."
    inputs_1 = tokenizer.encode_plus(sentence_0, sentence_1, add_special_tokens=True, return_tensors='pt')
    inputs_2 = tokenizer.encode_plus(sentence_0, sentence_2, add_special_tokens=True, return_tensors='pt')

    # del inputs_1["special_tokens_mask"]  # <---- add this
    # del inputs_2["special_tokens_mask"]  # <---- add this

    print(inputs_1.keys())
    pred_1 = model.predict(**inputs_1)[0].argmax().item()
    pred_2 = model.predict(**inputs_2)[0].argmax().item()
    print("sentence_1 is", "a paraphrase" if pred_1 else "not a paraphrase", "of sentence_0")
    print("sentence_2 is", "a paraphrase" if pred_2 else "not a paraphrase", "of sentence_0")

    email_results(
        folders_list=[sacred_dir],
        name_experiment=' finetuning transformer ',
        receiver_emails=['manucelotti@gmail.com'])
