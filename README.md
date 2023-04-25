# pbp

> Named Entity and Relation Extraction models for NFL play-by-play snippets


## 1. Scrap Data

> scrap game ids and play-by-play text from ESPN for 2022 NFL regular season.

**<i>from the project root</i>**

```cmd
cd tasks\scrap
```

```cmd
make scrap-schedules
```

**<i>output files found in "tasks/data/1/"</i>**

```cmd
make scrap-pbp
```

**<i>output files found in "tasks/data/2/"</i>**

## 2. Centralize and Split Data

> create a main source file and split into dev / holdout datasets

**<i>from the project root</i>**

```cmd
cd tasks\scrap
make centralize-data
make split-data
```

**<i>output files found in "tasks/data/3/"</i>**

## 3. Programmatically Label the Dev Dataset

> run labeling rules - [config](https://github.com/dpasse/pbp/blob/main/tasks/extract/config.py)

**<i>from the project root</i>**

```cmd
cd tasks\extract
make annotate-data
```

**<i>output files found in "tasks/data/4/"</i>**

## 4. Build CRF Model from Programmatically Labeled Dev Dataset

> run labeling rules - [config](https://github.com/dpasse/pbp/blob/main/tasks/extract/config.py)

**<i>from the project root</i>**

```cmd
cd tasks\extract
make ner
```

**<i> compare crf vs rule-based models</i>**

```python
from extr_ds.validators import check_for_differences

for i, outcomes in enumerate(zip(y_pred, y_train)):
    differences = check_for_differences(outcomes[1], outcomes[0])
    if differences.has_diffs:
        print(i)
        for diff in differences.diffs_between_labels:
            print(train_sents[i][diff.index])
            print(diff.diff_type)
            print()
```

