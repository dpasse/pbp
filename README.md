# pbp

> Named Entity and Relation Extraction models for NFL play-by-play snippets


## Scrap Data

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

## Centralize and Split Data

> create a main source file and split into dev / holdout datasets

**<i>from the project root</i>**

```cmd
cd tasks\scrap
make centralize-data
make split-data
```

**<i>output files found in "tasks/data/3/"</i>**

## Programmatically Label the Dev Dataset

> run labeling rules - [config](https://github.com/dpasse/pbp/blob/main/tasks/extract/config.py)

**<i>from the project root</i>**

```cmd
cd tasks\extract
make annotate-data
```

**<i>output files found in "tasks/data/4/"</i>**
