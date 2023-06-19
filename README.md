# omnibench-cli

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

## Local Graph Server

The local graph needs `oxigraph_server` to be installed.

You can install it with `cargo`:

```zsh
❯ cargo install oxigraph_server
    Updating crates.io index
  Downloaded oxigraph_server v0.3.18
  Downloaded 1 crate (34.4 KB) in 1.93s
  Installing oxigraph_server v0.3.18
    Updating crates.io index
    
[... long build follows ...]


```

Now you can start the graph server (which supports Federated SPARQL. You can
configure a different graph for annotations:

```zsh
❯ omni_cli graph enable
Enabling local SPARQL endpoint
❯ omni_cli graph run
Running local SPARQL endpoint
Running oxigraph_server with --location /home/user/OmniBenchmark/graph
Listening for requests at http://localhost:7878
❯ omni_cli graph run --annotations
Running local SPARQL endpoint
Running oxigraph_server with --location /home/user/OmniBenchmark/annotations
Listening for requests at http://localhost:8080
```

Do note, however, that no authentication or TLS endpoint is configured by
default. If you plan to deploy the graph in production, is up to you to make
sure you deploy an authentication frontend (support in the client is still
needed, see #2).

## Useful pointers

* [Initial Functionality Requests](https://hackmd.io/_1CE5qDTTH6Zdgu5iZwp6g)
* [omnibenchmark-py](https://github.com/omnibenchmark/omnibenchmark-py/), a `python` library to interact with omnibenchmark.
* [omnibus](https://github.com/shdam/omnibus), a `bash/R` tool to interact with `omnibenchmark` from the terminal.
* [omni_site](https://renkulab.io/gitlab/omnibenchmark/omni_site), the static site generator that powers [https://omnibenchmark.org/](https://omnibenchmark.org/).
