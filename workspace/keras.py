import os
import json

from sklearn.model_selection import train_test_split
from extr_ds.manager.utils.filesystem import load_document


def run_model():
    X, y = [], []
    dataset = json.loads(
        load_document(os.path.join('4', 'rels.json'))
    )

    for row in dataset:
        X.append(row['sentence'])
        y.append(row['label'])

    labels = set(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.15)

    ## tokenize

    ## small lstm

if __name__ == '__main__':
    run_model()
