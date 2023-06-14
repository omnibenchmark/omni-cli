import os
import shutil
import subprocess

from .config import get_graph_dir

OXIGRAPH_BIN = 'oxigraph_server'

def run_local_graph():
    binary = oxigraph_path()
    if binary is None:
        oxigraph_missing_notice()
        return
    graph_path = get_graph_dir()
    os.makedirs(graph_path, exist_ok=True)
    print("Running oxigraph_server with --location", graph_path)
    p = subprocess.run([
        binary, "--location", graph_path, "serve"])
    return p.stdout

# TODO: deprecate - we're currently uploading triples via
# the SPARQL endpoint.
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

