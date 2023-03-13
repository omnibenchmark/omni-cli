import click

from .config import init_dirs
from .sync import download_bench_data
from .benchmarks import benchmark_list, stage_list

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
    download_bench_data()

@click.command()
def update():
    """Update omnibenchmark cache"""
    click.echo(f"Updating omnibenchmark cache...")
    download_bench_data(force=True)

@click.group()
def bench():
    """Inspect benchmarks"""
    pass

@click.command()
def ls():
    for bench in benchmark_list():
        click.echo(f"{bench}")

@click.command()
@click.argument('bench_id')
def stages(bench_id):
    for stage in stage_list(bench_id):
        click.echo(f"{bench_id}:{stage}")

@click.command()
def dataset():
    """Inspect datasets"""
    click.echo(f"Doing stuff with datasets...")

@click.command()
def workflow():
    """Interacts with workflows"""
    click.echo(f"Doing stuff with workflows...")

bench.add_command(ls)
bench.add_command(stages)

run.add_command(init)
run.add_command(update)
run.add_command(bench)
run.add_command(dataset)
run.add_command(workflow)
