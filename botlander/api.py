from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from botlander.resources import (
    UserResource,
    UserResourceList,
    LoginResource,
    RefreshResource,
    FreshLoginResource,
    BotResource,
    BotResourceList,
    BotImageResource,
)
from flask_jwt_extended import JWTManager
import env


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = env.JWT_SECRET_KEY
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = env.JWT_REFRESH_TOKEN_EXPIRES
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = env.JWT_ACCESS_TOKEN_EXPIRES

# user
api.add_resource(UserResource, '/user/<string:user_id>')
api.add_resource(UserResourceList, '/user')


# bot
api.add_resource(BotResource, '/bot/<string:bot_id>')
api.add_resource(BotResourceList, '/bot')

##### bot image
api.add_resource(BotImageResource, '/bot/<string:bot_id>/image')


# auth
api.add_resource(LoginResource, '/auth/login')
api.add_resource(RefreshResource, '/auth/refresh')
api.add_resource(FreshLoginResource, '/auth/fresh-login')
