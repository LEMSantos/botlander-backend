import env
import click
import waitress
from botlander.api import app
from paste.translogger import TransLogger


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()


@cli.command('run')
def run():
    waitress.serve(
        TransLogger(app, setup_console_handler=False),
        host=env.WAITRESS_HOST,
        port=env.WAITRESS_PORT,
        threads=env.WAITRESS_THREADS,
    )


@cli.command('seed')
def seed():
    click.echo('o database foi seedado')
