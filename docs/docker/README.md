# docker image for omni-cli

This dockerfile extends the renku/omnibenchmark base image.

Ideally, the omnibenchmark image integrates these changes. In that moment
overriding the base image will not be needed anymore.

The image we build upon (`omni-data`) is supposed to be the docker image for a
given renku project (i.e., what you obtain after a `docker build -t omni-data
.` from the root folder in a given renku repository).

## Entrypoint

We also change the entrypoint to use `omni_cli workflow run` from the `work` dir.

I consider this to be a slightly cleaner way of executing workflows.

## Build

```
docker build --no-cache -t omni-cli -f dockerfile-extend 
```

## Interactive run

With mounting the `omni_cli` folder for interactive debugging:

```
docker run --rm \
  -v "/tmp/graphs:/graph:rw"
  -v ".:/home/rstudio/work"
  -v "/home/user/omni-cli:/omni_cli"
  -e OMNICLI_GRAPH_PATH=/graph
  --entrypoint bash -it omni-cl.i
```
