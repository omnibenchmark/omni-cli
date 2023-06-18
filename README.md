# omni-cli

A command line interface to query and access datasets and workflows project-wide across omnibenchmark.

## Install

Install via pip:

```
pip install omnibench-cli
```

While developing, you can use poetry:

```
pip install poetry
poetry shell
```

## Use


```zsh
❯ omni_cli
Usage: omni_cli [OPTIONS] COMMAND [ARGS]...

  Interact with omnibenchmark datasets and workflows.

Options:
  --help  Show this message and exit.

Commands:
  bench     Inspect benchmarks
  dataset   Inspect datasets
  docker    Manipulate local docker images used for workflow runs
  epoch     Query and manipulate Orchestrator Epochs in the Knowledge...
  graph     Local knowledge graph operations
  init      Initialize omnibenchmark cache
  query     Query the local graph
  update    Update omnibenchmark cache
  workflow  Interacts with workflows

❯ omni_cli bench ls
omni_clustering
spatial-clustering

❯ omni_cli bench stages omni_clustering
omni_clustering:build
omni_clustering:data_run
omni_clustering:process_run
omni_clustering:param_run
omni_clustering:method_run
omni_clustering:metric_run
omni_clustering:summary_run
```

## Useful pointers

* [Desired Features (WIP)](https://hackmd.io/_1CE5qDTTH6Zdgu5iZwp6g)
* [omnibenchmark-py](https://github.com/omnibenchmark/omnibenchmark-py/), a `python` library to interact with omnibenchmark.
* [omnibus](https://github.com/shdam/omnibus), a `bash/R` tool to interact with `omnibenchmark` from the terminal.
* [omni_site](https://renkulab.io/gitlab/omnibenchmark/omni_site), the static site generator that powers [https://omnibenchmark.org/](https://omnibenchmark.org/).
