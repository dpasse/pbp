import os
import re
import json

from sklearn.model_selection import train_test_split
from extr_ds.manager.utils.filesystem import load_document

def setup_text(sentence: str) -> str:
    ## translate reserve tokens
    sentence = re.sub(r'{', '(', sentence)
    sentence = re.sub(r'}', ')', sentence)

    ## setup e1
    sentence = re.sub(
        r'<e1>(.+?)</e1>',
        r'{ \g<1> }',
        sentence
    )

    ## setup e2
    sentence = re.sub(
        r'<e2>(.+?)</e2>',
        r'{{ \g<1> }}',
        sentence
    )

    return sentence

def run_model():
    X, y = [], []
    dataset = json.loads(
        load_document(os.path.join('4', 'rels.json'))
    )

    for row in dataset:
        X.append(setup_text(row['sentence']))
        y.append(row['label'])

    labels = set(y)

    print(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.15)

    ## tokenize

    ## small lstm

if __name__ == '__main__':
    run_model()
