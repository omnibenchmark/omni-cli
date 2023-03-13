# omni-cli

A command line interface to query and access datasets and workflows project-wide across omnibenchmark.

## Use

Until this project reaches enough maturity to be published in pypi, you can use `poetry` to use it:

```
pip install poetry
poetry shell
```

```zsh
❯ omni_cli
Usage: omni_cli [OPTIONS] COMMAND [ARGS]...

  Interact with omnibenchmark datasets and workflows.

Options:
  --help  Show this message and exit.

Commands:
  bench     Inspect benchmarks
  dataset   Inspect datasets
  init      Initialize omnibenchmark cache
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
