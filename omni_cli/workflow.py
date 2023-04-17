import json
import os
import shutil
import tempfile

import requests

from git import Repo

from .docker import is_docker

base = 'https://renkulab.io/knowledge-graph/workflows/'

def run():
    if is_docker():
        return run_in_docker(export=True)
    else:
        print("> not in docker")

def run_in_docker(full=True, export=False):
    print("> run in docker")
    if export:
        return export_graph(full=True)

def export_graph(full=True):
    from renku.command.graph import export_graph_command

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
        with open(os.path.join(output_dir, 'graph.jsonl'), 'w') as f:
            f.write(result)
        return "ok"
    else:
        return result

def get_graph_output_dir():
    return os.environ.get('OMNICLI_GRAPH_PATH', None)
