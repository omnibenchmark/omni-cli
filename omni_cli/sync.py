import json
import os

import requests

from .config import data_dir, local_bench_data, local_orch_data

base = "https://renkulab.io/gitlab/"
omni_site = "omnibenchmark/omni_site/"

benchmarks_json = "-/raw/master/data/data_infos.json?inline=false"
orchestrator_json = "-/raw/master/data/orchestrator_infos.json?inline=false"

bench_data = base + omni_site + benchmarks_json
orch_data = base + omni_site + orchestrator_json

def download_bench_data(force=False):
    if force or not os.path.isfile(local_bench_data):
        r = requests.get(bench_data)
        data = r.json()
        with open(local_bench_data, 'w') as f:
            json.dump(data, f)

    if force or not os.path.isfile(local_orch_data):
        r = requests.get(orch_data)
        data = r.json()
        with open(local_orch_data, 'w') as f:
            json.dump(data, f)
