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
            'path': '~/OmniBenchmark/graph'
        }
}

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
