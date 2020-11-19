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

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
