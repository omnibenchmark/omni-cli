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

def init_dirs():
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)

default_cfg = {
        'dirs': {
            'data': '~/OmniBenchmark/data'
        }
}

def init_rc():
    if not os.path.isfile(rc_file):
        with open(rc_file, 'w') as f:
            yaml.dump(default_cfg, f)

def _get_config():
    with os.path.open(rc_file) as f:
        return yaml.safe_load(f.read())
