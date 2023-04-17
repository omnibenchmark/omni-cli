import click

from .config import init_dirs, init_rc
from .sync import download_bench_data
from .benchmarks import benchmark_list, stage_list
from .datasets import describe as describe_dataset
from .datasets import download as download_dataset
from .datasets import size as size_dataset
from .datasets import dataset_list
from .workflow import run as workflow_run

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
    def run():
        """Run workflow"""
        click.echo(f"Running workflow")
        result = workflow_run()
        click.echo(result)

    workflow.add_command(run)

add_workflow_commands()
run.add_command(workflow)

run.add_command(workflow)
