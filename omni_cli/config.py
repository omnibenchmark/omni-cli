import os
import yaml

_home = os.path.expanduser('~')

app_name = "omnibenchmark-cli"

xdg_data_home = os.environ.get('XDG_DATA_HOME') or \
            os.path.join(_home, '.local', 'share')

xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.join(_home, '.config')

data_dir = os.path.join(xdg_data_home, app_name)

config_dir = os.path.join(xdg_config_home, app_name)

local_bench_data = os.path.join(data_dir, "omni_data.json")
local_orch_data = os.path.join(data_dir, "orch_data.json")

rc_file = os.path.join(config_dir, "omni_cli.yaml")

default_cfg = {
        'dirs': {
            'datasets': '~/OmniBenchmark/datasets'
        },
        'graph': {
            'enabled': False,
            'path': '~/OmniBenchmark/graph',
            'annotations_endpoint': 'localhost:8080',
            'graph_endpoint': 'localhost:7878'
        }
}

DEFAULT_GRAPH_ENDPOINT = "localhost:7878"
DEFAULT_ANNOTATIONS_ENDPOINT = "localhost:8080"

def init_dirs():
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)

def init_rc():
    if not os.path.isfile(rc_file):
        _write_config(default_cfg)

def get_dataset_dir():
    c = _get_config()
    path = c.get('dirs').get('datasets')
    return os.path.expanduser(path)

def get_graph_dir():
    c = _get_config()
    path = c.get('graph').get('path')
    return os.path.expanduser(path)

def get_annotations_dir():
    c = _get_config()
    path = c.get('graph').get('annotations_path', '~/OmniBenchmark/annotations' )
    return os.path.expanduser(path)

def get_graph_endpoint_query():
    endp = _get_graph_endpoint()
    return f"http://{endp}/query"

def get_graph_endpoint_update():
    endp = _get_graph_endpoint()
    return f"http://{endp}/update"

def get_annotation_endpoint_query():
    endp = _get_annotation_endpoint()
    return f"http://{endp}/query"

def get_annotation_endpoint_update():
    endp = _get_annotation_endpoint()
    return f"http://{endp}/update"

def _get_graph_endpoint():
    c = _get_config()
    return c.get('graph').get(
            'graph_endpoint', 
            DEFAULT_GRAPH_ENDPOINT)

def _get_annotation_endpoint():
    c = _get_config()
    return c.get('graph').get(
            'annotations_endpoint', 
            DEFAULT_ANNOTATIONS_ENDPOINT)

def enable_graph():
    c = _get_config()
    c['graph']['enabled'] = True
    _write_config(c)

def disable_graph():
    c = _get_config()
    c['graph']['enabled'] = False
    _write_config(c)

def is_graph_enabled():
    c = _get_config()
    return c['graph']['enabled']

def _get_config():
    with open(rc_file) as f:
        return yaml.safe_load(f.read())

def _write_config(c):
    with open(rc_file, 'w') as f:
        yaml.dump(c, f)
