import os
import re
import json
import random
import numpy
import evaluate

from datasets import Dataset
from extr_ds.manager.utils.filesystem import load_document

from transformers import logging, \
                         pipeline, \
                         set_seed, \
                         DataCollatorWithPadding, \
                         AutoTokenizer, \
                         TFAutoModelForSequenceClassification
from transformers.keras_callbacks import KerasMetricCallback


logging.set_verbosity_error()

epochs = 25

pretrained_model = 'bert-base-cased'
model_output_directory = 'transformers/nfl_pbp_relation_classifier'

labels = ['NO_RELATION', 'is_spot_of_ball']
label2id = { label:i for i, label in enumerate(labels) }
id2label = { i:label for i, label in enumerate(labels) }

e1s = [
    'TEAM'
]

e2s = [
    'QUANTITY'
]

tokens_to_add = []

for e1 in e1s:
    tokens_to_add.append(f'<e1:{e1}>')
    tokens_to_add.append(f'</e1:{e1}>')
    
for e2 in e2s:
    tokens_to_add.append(f'<e2:{e2}>')
    tokens_to_add.append(f'</e2:{e2}>')

seed = 52
set_seed(seed)

def get_dataset(tokenizer):
    data_collator = DataCollatorWithPadding(
        tokenizer,
        return_tensors='tf'
    )

    rels = json.loads(
        load_document(os.path.join('4', 'rels.json'))
    )

    random.seed(seed)
    random.shuffle(rels)

    data = []
    for row in rels:
        data.append({
            'text': row['sentence'],
            'label': label2id[row['label']]
        })

    def tokenize_function(examples):
        return tokenizer(examples["text"])

    n = len(rels)
    split_point = .8
    pivot = int(n * split_point)
    print('len#:', n, 'pivot:', pivot)
    
    train_dataset = Dataset.from_list(data[:pivot])
    tf_train_set = train_dataset.map(
        tokenize_function,
        batched=True
    ).to_tf_dataset(
        columns=['attention_mask', 'input_ids'],
        label_cols='label',
        shuffle=True,
        batch_size=4,
        collate_fn=data_collator,
    )

    test_dataset = Dataset.from_list(data[pivot:])
    tf_test_set = test_dataset.map(
        tokenize_function,
        batched=True
    ).to_tf_dataset(
        columns=['attention_mask', 'input_ids'],
        label_cols='label',
        shuffle=True,
        batch_size=4,
        collate_fn=data_collator,
    )

    return tf_train_set, tf_test_set

load_accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = numpy.argmax(predictions, axis=1)
    return load_accuracy.compute(predictions=predictions, references=labels)

def build_model():
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model,
        use_fast=True,
        truncation=True,
        padding='max_length',
    )

    tokens_added = tokenizer.add_tokens(tokens_to_add)
    print('added', tokens_added, 'tokens')

    tf_train_set, tf_test_set = get_dataset(tokenizer)

    model = TFAutoModelForSequenceClassification.from_pretrained(
        pretrained_model,
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id,
    )

    model.resize_token_embeddings(len(tokenizer))

    model.compile(optimizer="adam")

    model.fit(
        x=tf_train_set,
        validation_data=tf_test_set,
        epochs=epochs,
        callbacks=[
            KerasMetricCallback(
                metric_fn=compute_metrics,
                eval_dataset=tf_test_set,
            ),
        ]
    )

    for model_to_save in [tokenizer, model]:
        model_to_save.save_pretrained(model_output_directory)

def pipeline_test():
    tokenizer = AutoTokenizer.from_pretrained(
        model_output_directory
    )

    classifier = pipeline(
        "text-classification", 
        model=model_output_directory,
        top_k=None
    )

    examples = [
        '(4:11 - 3rd) (Shotgun) K.Murray pass deep middle to Z.Ertz to <e1>SEA</e1> <e2>43</e2> for 32 yards (R.Neal).',
        '(15:00 - 3rd) (Shotgun) T.Siemian sacked at <e1>CHI</e1> 18 for <e2>-7</e2> yards (sack split by N.Shepherd and J.Franklin-Myers).'
    ]

    vlookup = { c:b for b,c in tokenizer.get_vocab().items() }
    for text in examples:
        response = tokenizer(text)

        print(text)
        print('tokens:', [vlookup[c] for c in response['input_ids']])
        print(classifier(text))


if __name__ == '__main__':
    build_model()
    pipeline_test()
