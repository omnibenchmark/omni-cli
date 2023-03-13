import os

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

def init_dirs():
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)

