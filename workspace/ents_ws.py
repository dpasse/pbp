from typing import Any, Dict

import re
import os
import json
import random
import numpy
import evaluate

from datasets import Dataset
from utils import word_tokenizer
from extr import Entity, Location
from extr_ds.manager.utils.filesystem import load_document
from extr_ds.labelers.iob import Labeler

import tensorflow as tf
from transformers import logging, \
                         pipeline, \
                         set_seed, \
                         DataCollatorForTokenClassification, \
                         AutoTokenizer, \
                         TFAutoModelForTokenClassification

from transformers.keras_callbacks import KerasMetricCallback


logging.set_verbosity_error()

epochs = 13
seed = 52

model_checkpoint = 'bert-base-cased'
model_output_checkpoint = 'transformers/nfl_pbp_token_classifier_ws'

entity_groups = [
    'PLAYER',
    'TEAM',
    'TIME',
    'PERIOD',
    'QUANTITY',
    'UNITS'
]

labels = ['O'] + \
    [f'B-{label}' for label in entity_groups] + \
    [f'I-{label}' for label in entity_groups]

label2id = { label:i for i, label in enumerate(labels) }
id2label = { i:label for i, label in enumerate(labels) }

seqeval = evaluate.load('seqeval')

if seed:
    set_seed(seed)
    random.seed(52)

def align_labels(tokenized_inputs, label_list):
    labels = []
    for word_idx in tokenized_inputs.word_ids(batch_index=0):
        label_id = -100
        if not word_idx is None:
            label =  re.sub(r'^[BI]-(.+)$', r'I-\g<1>', label_list[word_idx]) \
                if word_idx == previous_word_idx \
                else label_list[word_idx]

            label_id = label2id[label]

        labels.append(label_id)
        previous_word_idx = word_idx

    return labels

def get_dataset(tokenizer, model):
    def tokenize_and_align_labels(record):
        tokenized_inputs = tokenizer(
            record['tokens'],
            truncation=True,
            is_split_into_words=True
        )

        tokenized_inputs['labels'] = align_labels(
            tokenized_inputs,
            record['labels']
        )

        return tokenized_inputs

    ents_dataset = json.loads(
        load_document(os.path.join('5', 'ents-iob.json'))
    )

    random.shuffle(ents_dataset)

    pivot = int(len(ents_dataset) * .8)
    data_collator = DataCollatorForTokenClassification(
        tokenizer,
        return_tensors='tf'
    )

    train_dataset = Dataset.from_list(ents_dataset[:pivot])
    tf_train_set = model.prepare_tf_dataset(
        train_dataset.map(
            tokenize_and_align_labels,
            batched=False
        ),
        shuffle=True,
        collate_fn=data_collator,
    )

    test_dataset = Dataset.from_list(ents_dataset[pivot:])
    tf_test_set = model.prepare_tf_dataset(
        test_dataset.map(
            tokenize_and_align_labels,
            batched=False
        ),
        shuffle=True,
        collate_fn=data_collator,
    )

    return tf_train_set, tf_test_set

def compute_metrics(preds):
    predictions, actuals = preds
    predictions = numpy.argmax(predictions, axis=2)

    results = seqeval.compute(
        predictions=[
            [labels[p] for p, l in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, actuals)
        ],
        references=[
            [labels[l] for p, l in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, actuals)
        ]
    )

    return {
        key: results[f'overall_{key}']
        for key in ['precision', 'recall', 'f1', 'accuracy']
    }
    
def build_model():
    tokenizer = AutoTokenizer.from_pretrained(
        model_checkpoint,
        truncation=True,
    )

    model = TFAutoModelForTokenClassification.from_pretrained(
        model_checkpoint,
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id
    )

    tf_train_set, tf_test_set = get_dataset(tokenizer, model)

    optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
    model.compile(optimizer=optimizer)

    model.fit(
        x=tf_train_set,
        validation_data=tf_test_set,
        epochs=epochs,
        callbacks=[
            KerasMetricCallback(
                metric_fn=compute_metrics,
                eval_dataset=tf_test_set
            ),
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=3
            )
        ]
    )

    for model_to_save in [tokenizer, model]:
        model_to_save.save_pretrained(model_output_checkpoint)

def pipeline_test():
    classifier = pipeline(
        "ner", 
        model=model_output_checkpoint,
        aggregation_strategy='simple'
    )

    examples = [
        '(6:51 - 1st) (Shotgun) P.Mahomes scrambles right end to LAC 34 for 2 yards (S.Joseph; K.Van Noy). FUMBLES (S.Joseph), and recovers at LAC 34.',
    ]

    threshold = .5

    annotations = []
    for text in examples:
        entities = []
        for response in filter(lambda r: r['score'] >= threshold, classifier(text)):
            location = Location(start=response['start'], end=response['end'])
            entities.append(
                Entity(
                    identifier=len(entities) + 1,
                    label=response['entity_group'],
                    text=location.extract(text),
                    location=location
                )
            )

        iob = []
        label = Labeler(word_tokenizer).label(text, entities)
        for grouping in [label]:
            iob.append({
                'tokens': [tk.text for tk in grouping.tokens],
                'labels': grouping.labels,
            })

        annotations.append({
            'text': text,
            'iob': iob
        })

    print('iob2')
    print(annotations)
    

if __name__ == '__main__':
    build_model()
    pipeline_test()
