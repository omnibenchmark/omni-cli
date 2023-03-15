import json
import os
import shutil
import tempfile

import requests

from git import Repo

from .config import local_bench_data, get_dataset_dir
from .resources import Resource

base = 'https://renkulab.io/knowledge-graph/datasets/'

def load_resources():
    """
    Load a list of Resources from the local cache
    """
    with open(local_bench_data, 'r') as f:
        data = json.load(f)
    return [Resource(**d) for d in data.values()]

def describe(uuid):
    if len(uuid) < 8:
        raise ValueError('DatasetID must be at least 8 characters long')
    res = load_resources()
    # This can be improved (by creating proper indexes by uuid and by
    # short_name), but it's good enough for now.
    for r in res:
        if r.identifier.hex.startswith(uuid):
            print(r.title)
            print(r.description)

def dataset_list():
    res = load_resources()
    return [r for r in res if r.isData()]

def download(uuid):
    if len(uuid) < 8:
        raise ValueError('DatasetID must be at least 8 characters long')

    datasets = dataset_list()
    full_id = None
    for d in datasets:
        if d.identifier.hex.startswith(uuid):
            full_id = d.identifier.hex

    r = requests.get(base + full_id)
    meta = r.json()
    parts = [part.get('atLocation') for part in meta.get('hasPart')]

    # TODO(btraven): I should check that I'm only copying the parts in here. For the time being,
    # I'm assuming all the files in the used folders go.
    data_dirs = set([os.path.split(part)[0] for part in parts])

    project = meta.get('project').get('_links')[0].get('href')
    project_meta = requests.get(project).json()
    project_git = project_meta.get('urls').get('http')

    # TODO(btraven): this would be a good time to confirm that we want to
    # import the dataset.
    # We have size information in project_meta

    project_name = project_name_from_repo(project_git)
    print(f"Cloning temporary repo from {project_git}")

    with tempfile.TemporaryDirectory() as tmpdir:
        local_repo = os.path.join(tmpdir, project_name)
        os.makedirs(local_repo)
        Repo.clone_from(project_git, local_repo)

        datasets_dir = get_dataset_dir()
        dest = os.path.join(datasets_dir, full_id)
        os.makedirs(dest, exist_ok=True)

        # TODO(btraven): It would be a good idea to store the output of "git
        # log" for the files in the dataset - and reconcile that with the
        # versioning history captured by the Knowledge Graph.

        for _dir in data_dirs:
            shutil.copytree(os.path.join(local_repo, _dir), os.path.join(dest, _dir))

    print(f"Dataset saved to {dest}")

def project_name_from_repo(repo):
    return repo.split('/')[-1].split('.git')[0]
