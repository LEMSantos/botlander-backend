import env
from mongoengine import connect
from botlander.cli import cli

connect(
    env.DATABASE_NAME,
    host=env.DATABASE_HOST,
    username=env.DATABASE_USERNAME,
    password=env.DATABASE_PASSWORD,
    authentication_source=env.DATABASE_AUTHENTICATION_SOURCE,
)

if __name__ == '__main__':
    cli()
