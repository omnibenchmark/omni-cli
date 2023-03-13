import json

from .config import local_bench_data
from .resources import Resource

def load_resources():
    """
    Load a list of Resources from the local cache
    """
    with open(local_bench_data, 'r') as f:
        data = json.load(f)
    return [Resource(**d) for d in data.values()]

def describe(dataset_id):
    if len(dataset_id) < 8:
        raise ValueError('DatasetID must be at least 8 characters long')
    res = load_resources()
    # This can be improved (by creating proper indexes by uuid and by
    # short_name), but it's good enough for now.
    for r in res:
        if r.identifier.hex.startswith(dataset_id):
            print(r.title)
            print(r.description)

def dataset_list():
    res = load_resources()
    return [r for r in res if r.isData()]
