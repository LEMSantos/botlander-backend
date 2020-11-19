from botlander.api import app
from mongoengine import connect
from paste.translogger import TransLogger
import waitress
import env

connect(
    env.DATABASE_NAME,
    host=env.DATABASE_HOST,
    username=env.DATABASE_USERNAME,
    password=env.DATABASE_PASSWORD,
    authentication_source=env.DATABASE_AUTHENTICATION_SOURCE,
)

if __name__ == '__main__':
    waitress.serve(
        TransLogger(app, setup_console_handler=False),
        host=env.WAITRESS_HOST,
        port=env.WAITRESS_PORT,
        threads=env.WAITRESS_THREADS,
    )
