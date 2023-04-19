import json
import logging
import os
import shutil
import subprocess
import tempfile

import requests

from .config import get_graph_dir, is_graph_enabled
from .docker import is_docker
from .graph import load_triples

from git import Repo

from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
from omnibenchmark.renku_commands.general import renku_save
from renku.command.graph import export_graph_command

GRAPH_HOST_PATH = "/tmp/omni-graphs"
GRAPH_CONT_PATH = "/graph"
GRAPH_JSON = "graph.jsonl"

def run(docker_image=None, sparql=None):
    # --------------------------------------------------------------
    # we should automate these images, see if they exist localy etc
    if docker_image is None:
        docker_image = "renku-csf-ext"
    # --------------------------------------------------------------

    if is_docker():
        return run_from_docker(export=True)
    else:
        print("> running in host")
        shutil.rmtree(GRAPH_HOST_PATH, ignore_errors=True)
        os.makedirs(GRAPH_HOST_PATH, exist_ok=True)

        out = run_from_host_in_docker(docker_image)
        if is_graph_enabled():
            load_graph()
        if sparql is not None:
            upload_graph(sparql)
        return out

def run_from_docker(full=True, export=False):
    print("> running in docker")
    oo = get_omni_object_from_yaml('src/config.yaml')
    oo.create_dataset()
    oo.run_renku()
    oo.update_result_dataset()

    # TODO: need to check if the repo has changed within the container
    # the best strategy is probably to mount data/ as a rw volume

    if export:
        return export_graph(full=True)

def run_from_host_in_docker(docker_image):
    p = subprocess.run([
            "docker", "run",
            "--rm", "-v", "{graph_host}:{graph_container}".format(
                graph_host=GRAPH_HOST_PATH,
                graph_container=GRAPH_CONT_PATH),
            "-v", ".:/home/rstudio/work", # FIXME hardcoded user!!
            "-e", "OMNICLI_GRAPH_PATH={graph_container}".format(graph_container=GRAPH_CONT_PATH),
            docker_image])
    return p.stdout

def export_graph(full=True):
    if full:
        revision = None

    _format = "jsonld"
    strict = True

    result = (
        export_graph_command()
        .build()
        .execute(format=_format, strict=strict, revision_or_range=revision)
    )

    result = result.output.as_jsonld_string(2)
    output_dir = get_graph_output_dir()

    if output_dir:
        with open(os.path.join(output_dir, GRAPH_JSON), 'w') as f:
            f.write(result)
        return "ok"
    else:
        return result

def upload_graph(sparql):
    print("NOT IMPLEMENTED: upload graph to endpoint:", sparql)

def get_graph_output_dir():
    return os.environ.get('OMNICLI_GRAPH_PATH', None)

def load_graph():
    _serialize_graph()
    _load_in_local_graph_store()

def _serialize_graph():
    from rdflib import Graph
    g = Graph()
    g.parse(f"file://{GRAPH_HOST_PATH}/{GRAPH_JSON}", format="json-ld")
    g.serialize(f"file://{GRAPH_HOST_PATH}/graph.ttl")
    graph_len = len(list(g.triples((None, None, None))))
    print("> Got", graph_len, "triples")

def _load_in_local_graph_store():
    path = get_graph_dir()
    load_triples(f"{GRAPH_HOST_PATH}/graph.ttl")
