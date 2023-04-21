import os
import subprocess

from pathlib import Path

import yaml

OMNI_DOCKER_PREFIX = 'omnibench'


def is_docker():
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text()

# TODO: get force flag
def docker_build():
    top = _get_repo_toplevel()
    os.chdir(top)
    print('Building base image...')
    _build_base_image()

    entry = 'entrypoint.sh'
    dockerfile = 'dockerfile.omnicli'

    project = _get_base_image()

    dockerfile_tmpl = f"""FROM {project} as lfs
ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt-get update && apt-get install -y \
  git-lfs \
  && rm -rf /var/lib/apt/lists/*
USER ${{NB_USER}}

FROM lfs

RUN mkdir $HOME/orig

# For development - should be optional
RUN pip install -U pip
RUN pip install git+https://renkulab.io/gitlab/btraven/omni-cli/
RUN pip install poetry

COPY entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]"""

    entrypoint_tmpl = """#!/bin/sh
ARGS=
if [ $OMNICLI_DIRTY -eq 1 ]; then
    ARGS="--no-commit"
    rm -rf work && cp -r orig work
fi
cd work && omni_cli workflow run $ARGS"""

    with open(entry, 'w') as ep:
        ep.write(entrypoint_tmpl)
        _make_executable(entry)

    with open(dockerfile, 'w') as f:
        f.write(dockerfile_tmpl)

    print('Building extension image...')
    _build_omni_image()

    os.remove(entry)
    os.remove(dockerfile)


def _get_repo_toplevel():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip()

def _build_base_image(force=False):
    img = _get_base_image()
    subprocess.run(["docker", "build", "-t", img, "."])

def _build_omni_image(force=False):

    # TODO: receive force flag from cli
    # ---------------------------------
    # force = True
    # ---------------------------------

    img = get_omni_image()
    cmd = ["docker", "build", "-f", "dockerfile.omnicli"]
    if force:
        cmd.append('--no-cache')
    cmd = cmd + ["-t", img, "."]
    subprocess.run(cmd)
    print("> omni-cli docker image built as:", img)

def _get_base_image():
    """return name for base_image, which is the docker build of the project's Dockerfile"""
    project = _get_project_name()
    return f"{OMNI_DOCKER_PREFIX}-{project}"

def get_omni_image():
    """return name for omni_image, which is our custom extensions on top of the base image. this includes the custom entrypoint"""
    base_img = _get_base_image()
    return f"{base_img}-cli"

def _get_project_name():
    config = yaml.safe_load(open('src/config.yaml'))
    return config.get('data').get('name')

def _make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


