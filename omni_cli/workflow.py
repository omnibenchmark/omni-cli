import json
import logging
import os
import shutil
import subprocess
import tempfile

import requests


from .docker import is_docker

from git import Repo
from renku.command.graph import export_graph_command

GRAPH_HOST_PATH = "/tmp/omni-graphs"
GRAPH_CONT_PATH = "/graph"
GRAPH_JSON = "graph.json"

def run():
    if is_docker():
        return run_from_docker(export=True)
    else:
        print("> running in host")
        shutil.rmtree(GRAPH_HOST_PATH, ignore_errors=True)
        os.makedirs(GRAPH_HOST_PATH, exist_ok=True)
        # TODO get image from cli
        docker_image = "renku-csf-ext"
        out = run_from_host_in_docker(docker_image)
        summarize_graph()
        return out

def run_from_docker(full=True, export=False):
    print("> running in docker")
    # TODO do actual run    
    if export:
        return export_graph(full=True)

def run_from_host_in_docker(docker_image):
    p = subprocess.run([
            "docker", "run",
            "--rm", "-v", "{graph_host}:{graph_container}".format(
                graph_host=GRAPH_HOST_PATH,
                graph_container=GRAPH_CONT_PATH),
            "-v", ".:/home/rstudio/work",
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

def get_graph_output_dir():
    return os.environ.get('OMNICLI_GRAPH_PATH', None)

def summarize_graph():
    from rdflib import Graph
    g = Graph()
    g.parse("file://{path}/graph.jsonl".format(path=GRAPH_HOST_PATH), format="json-ld")
    graph_len = len(list(g.triples((None, None, None))))
    print("> Got", graph_len, "triples")
