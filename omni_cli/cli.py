import click

from .config import init_dirs
from .sync import download_bench_data
from .benchmarks import benchmark_list

@click.group()
def run():
    """Interact with omnibenchmark datasets and workflows."""
    pass

@click.command()
def describe():
    click.echo(f"Attempting to describe entity")

@click.command()
def init():
    click.echo(f"Initializing omnibenchmark cache...")
    init_dirs()
    download_bench_data()

@click.command()
def update():
    click.echo(f"Updating omnibenchmark cache...")
    download_bench_data(force=True)

@click.command()
def benchmark():
    for bench in benchmark_list():
        click.echo(f"{bench}")

@click.command()
def dataset():
    click.echo(f"Doing stuff with datasets...")

@click.command()
def workflow():
    click.echo(f"Doing stuff with workflows...")

run.add_command(init)
run.add_command(update)
run.add_command(benchmark)
run.add_command(dataset)
run.add_command(workflow)
