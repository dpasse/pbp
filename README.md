# pbp

> Named Entity and Relation Extraction models for NFL play-by-play snippets


## Process

1. Scrap Data
2. Centralize Data
    - combine multiple files into a single one
3. Build Dataset / Model
    1. Split
        - splits random subset for managable inspection - 1% at random
    2. ITERATE
        1. Annotate Data
            - builds a redacted file for quick visual inspection
        2. Inspect Data
            - if issues, fix and annotate again
            - may require a complete reset of "gold standard" dataset
        3. Save
            - add data to be used in model building - "gold standard"
        4. Build Model


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

## 2. Centralize Data

> create a main source file and split into dev / holdout datasets

**<i>from the project root</i>**

```cmd
cd tasks\scrap
make centralize-data
```

**<i>output files found in "tasks/data/3/"</i>**

## 3. Build Dataset / Model

**<i>from the project root</i>**

```cmd
cd workspace
```

### 1. Split Data - small percentage at random

```cmd
extr-ds --split
```

**<i>output files found in "workspace/2/"</i>**

### 2. Programmatically Label Named Entities (Iterate)

```cmd
extr-ds --annotate
```

**<i>output files found in "workspace/3/"</i>**

### 3. Programmatically Label Relations (Iterate)

```cmd
extr-ds --relate
```

**<i>output files found in "workspace/3/"</i>**

### 4. Save data for model building

```cmd
extr-ds --save
```

**<i>output files found in "tasks/data/4/"</i>**

### 5. Build CRF Model

```cmd
make crf
```
