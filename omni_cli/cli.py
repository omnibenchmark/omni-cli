import click

from .benchmarks import benchmark_list, stage_list
from .config import init_dirs, init_rc
from .config import enable_graph, disable_graph, is_graph_enabled
from .datasets import describe as describe_dataset
from .datasets import download as download_dataset
from .datasets import size as size_dataset
from .datasets import dataset_list
from .docker import docker_build, docker_shell
from .graph import run_local_graph, destroy_local_graph
from .sparql import query_generations, query_last_generation
from .sparql import query_generations, query_orchestrator_by_name
from .sync import download_bench_data
from .workflow import run as workflow_run

ENV_SPARQL = 'SPARQL_ENDPOINT'

@click.group()
def run():
    """Interact with omnibenchmark datasets and workflows."""
    pass

@click.command()
def describe():
    click.echo(f"Attempting to describe entity")

@click.command()
def init():
    """Initialize omnibenchmark cache"""
    click.echo(f"Initializing omnibenchmark cache...")
    init_dirs()
    init_rc()
    download_bench_data()

run.add_command(init)

@click.command()
def update():
    """Update omnibenchmark cache"""
    click.echo(f"Updating omnibenchmark cache...")
    download_bench_data(force=True)

run.add_command(update)

@click.group()
def bench():
    """Inspect benchmarks"""
    pass

@click.command()
def ls():
    """List all benchmarks"""
    for bench in benchmark_list():
        click.echo(f"{bench}")

@click.command()
@click.argument('bench_id')
def stages(bench_id):
    for stage in stage_list(bench_id):
        click.echo(f"{bench_id}:{stage}")

bench.add_command(ls)
bench.add_command(stages)
run.add_command(bench)

@click.group()
def dataset():
    """Inspect datasets"""
    pass

def add_dataset_commands():
    @click.command()
    def ls():
        """List all datasets"""
        for r in dataset_list():
            _id = r.identifier.hex[:8]
            bench = r.benchmark()
            click.echo(f"{_id}\t{bench}\t\t{r.title}")

    dataset.add_command(ls)

    @click.command()
    @click.argument('uuid')
    def describe(uuid):
        """Describe a dataset"""
        describe_dataset(uuid)

    dataset.add_command(describe)

    @click.command()
    @click.argument('uuid')
    def size(uuid):
        """Fetch size data for a dataset"""
        click.echo(f"Size for dataset {uuid}")
        size_dataset(uuid)

    dataset.add_command(size)

    @click.command()
    @click.argument('uuid')
    def download(uuid):
        """Download a dataset"""
        click.echo(f"Downloading dataset {uuid}")
        download_dataset(uuid)

    dataset.add_command(download)

add_dataset_commands()
run.add_command(dataset)

@click.group()
def workflow():
    """Interacts with workflows"""
    pass

def add_workflow_commands():
    @click.command()
    @click.argument('sparql', envvar=ENV_SPARQL, required=False)
    @click.option('-i', '--image', 'image', help="Docker image to run workflow from")
    @click.option('--commit/--no-commit', is_flag=True, default=True, show_default=True,
                  help="--no-commit leaves outputs in a dirty repo. This option skips the renku commits for each run, and is intented to debug the workflow.")
    def run(image, sparql, commit):
        """Run workflow"""
        click.echo(f"Running workflow")
        dirty = not commit
        result = workflow_run(docker_image=image, sparql=sparql, dirty=dirty)
        click.echo(result)

    workflow.add_command(run)

add_workflow_commands()
run.add_command(workflow)

@click.group()
def graph():
    """Local knowledge graph operations"""
    pass

def add_graph_commands():

    @click.command()
    def enable():
        click.echo(f"Enabling local SPARQL endpoint")
        enable_graph()

    graph.add_command(enable)

    @click.command()
    def disable():
        click.echo(f"Disabling local SPARQL endpoint")
        disable_graph()

    graph.add_command(disable)

    @click.command()
    def status():
        enabled = is_graph_enabled()
        status = 'enabled' if enabled else 'disabled'
        click.echo(f"Status: {status}")

    graph.add_command(status)

    @click.command()
    def run():
        click.echo(f"Running local SPARQL endpoint")
        run_local_graph()

    graph.add_command(run)

    @click.command()
    def destroy():
        click.echo(f"Destroy local graph")
        destroy_local_graph()

    graph.add_command(destroy)

add_graph_commands()
run.add_command(graph)

@click.group()
def docker():
    """Manipulate local docker images used for workflow runs"""
    pass

def add_docker_commands():

    @click.command()
    def build():
        """Build a docker image suitable for running omnibenchmark workflows with omni-cli"""
        click.echo(f"Building local docker image")
        docker_build()

    docker.add_command(build)

    @click.command()
    def shell():
        """Starts a bash shell in the default docker image for a given project"""
        click.echo("Starting shell within docker container for project")
        docker_shell()

    docker.add_command(shell)

add_docker_commands()
run.add_command(docker)

@click.group()
def query():
    """Query the local graph"""
    pass

def add_query_commands():

    @click.command()
    def generations():
        """Query local graph for recent generations"""
        query_generations()

    query.add_command(generations)

    @click.command()
    def last_generation():
        """Query local graph for the most recent generation"""
        query_last_generation()

    query.add_command(last_generation)

add_query_commands()
run.add_command(query)

@click.group()
def orchestrator():
    """Query and update the KG for the orchestrator runs"""
    pass

def add_orchestrator_commands():
    @click.command()
    @click.argument('name')
    def runs(name):
        """Return the most recent runs for the given benchmark name"""
        query_orchestrator_by_name(name)

    orchestrator.add_command(runs)

add_orchestrator_commands()
run.add_command(orchestrator)
