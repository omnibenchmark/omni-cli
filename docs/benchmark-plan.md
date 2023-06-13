# Benchmark plan file format

This file describes the format used in the `benchmark-plan.md` file. The
benchmark plan contains the master description for the whole benchmark.

It is encoded in `yaml` (but other formats are possible, like json, as long as
they maintain compatible semantics).

NOTE: the `.gitlab-ci.yaml` file can be (re)generated in the future from a
single authoritative source like the `benchmark-plan.md`.

There are three main distinct parts in the benchmark plan:

## 1. Benchmark metadata

- name: the short name of the benchmark. all of the projects need to refer to the same name. 
- base: the base URL for the repos referred in the file. This base URL can be
  overridden by different methods (see description for the `benchmark.work` file
  below).

## 2. Stages array

The stages block is a sorted array of the serial steps a benchmark will
progress through its execution.

## 3. Data sources

As many blocks as stages are defined in the stages section. No guarantee of
sequentiality is made for the repos pointed in here.

The repos included in the repos array can use different formats:

- 1. `namespace/project` format - it will prepend the base specified in the metadata
  block. Benchmark maintainer should make sure that the repositories are
  publicly accessible, or provide git credentials otherwise.
- 2. https://domain.tld/repo.git - full URL, including a fully qualified domain
- 3. `../rel/path/to/repo` - a relative file path in the local file system.
- 4. `/absolute/path/to/repo` - an absolute path in the local file system.

Additionally, a link to a repository expressed in the `namespace/project` form
can be dereferenced by means of a `benchmark.work` local file. This behavior can
be disabled by setting `local_override` to `false`.

```yaml
benchmark:
  - name: iris_example
  - base: https://renkulab.io/gitlab/omnibenchmark/
  - local_override: true

stages:
  - data
  - process
  - parameter
  - method
  - metric
  - summary

data:
  repos:
    - iris_example/iris-dataset
    - iris_example/iris-noisy

process:
  repos:
    - iris_example/iris-filter

method:
  repos:
    - iris_example/iris-random-forest
    - iris_example/iris-lda

metric:
  repos:
    - iris_example/iris-accuracy
    - iris_example/iris-accuracy-pval

summary:
  repos:
    - iris_example/irirs-summary-metrics
```
