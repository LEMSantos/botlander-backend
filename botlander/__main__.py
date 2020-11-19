from mongoengine import connect
connect(
    env.DATABASE_NAME,
    host=env.DATABASE_HOST,
    username=env.DATABASE_USERNAME,
    password=env.DATABASE_PASSWORD,
    authentication_source=env.DATABASE_AUTHENTICATION_SOURCE,
)
