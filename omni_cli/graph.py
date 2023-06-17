import os
import shutil
import subprocess

from .config import get_graph_dir, get_annotations_dir
from .config import _get_annotation_endpoint

OXIGRAPH_BIN = 'oxigraph_server'

def run_local_graph(annotations=False):
    binary = oxigraph_path()
    if binary is None:
        oxigraph_missing_notice()
        return

    if not annotations:
        graph_path = get_graph_dir()
    else:
        graph_path = get_annotations_dir()

    os.makedirs(graph_path, exist_ok=True)
    print("Running oxigraph_server with --location", graph_path)
    cmd = [binary, "--location", graph_path, "serve"]

    if annotations:
        bind = _get_annotation_endpoint()
        cmd = cmd + ["--bind", bind]

    p = subprocess.run(cmd)
    return p.stdout

# TODO: deprecate for regular use - we're currently uploading triples via the SPARQL endpoint.
# this method might still be useful for quick dumping for testing etc, but we need to ensure
# the server is not running to avoid race conditions and possible locks.
def load_triples(triples):
    print("> load into local graph server")
    # TODO should sanitize triple path (to be under project path)
    binary = oxigraph_path()
    if binary is None:
        oxigraph_missing_notice()
        return
    graph_path = get_graph_dir()
    if not os.path.isdir(graph_path):
        os.makedirs(graph_path, exist_ok=True)
    p = subprocess.run([
        binary, "--location", graph_path, "load",
        "--file", triples])
    return p.stdout

def oxigraph_missing_notice():
    print("oxigraph_server is missing. Please refer to https://crates.io/crates/oxigraph_server for installation options")
    print("Have a nice day!")

def oxigraph_path():
    return shutil.which(OXIGRAPH_BIN)

def destroy_local_graph():
    print("> NOT IMPLEMENTED: destroy local graph")

