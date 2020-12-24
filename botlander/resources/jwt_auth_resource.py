from flask_restful import Resource, reqparse, abort
from mongoengine.queryset.visitor import Q
from werkzeug.security import check_password_hash
from http import HTTPStatus
from botlander.database.models import User
from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
)

import bson


def get_login_args():
    parser = reqparse.RequestParser()

    parser.add_argument('identity', required=True)
    parser.add_argument('password', required=True)

    args = parser.parse_args(strict=True)

    return args


def get_user_or_fail(identity, password):
    import json
    from flask import Response

    fail_response = Response(
        json.dumps({
            'message': 'Username or password is invalid.',
        }),
        status=HTTPStatus.UNAUTHORIZED,
        content_type='application/json',
    )

    try:
        user = User.objects.get(
            Q(username=identity.lower()) | Q(email=identity),
        )
    except User.DoesNotExist:
        abort(fail_response)

    if not check_password_hash(user.password, password):
        abort(fail_response)

    return user


class LoginResource(Resource):

    def post(self):
        args = get_login_args()

        user = get_user_or_fail(
            args.get('identity'),
            args.get('password'),
        )

        return {
            'message': 'Successfully logged in.',
            'user': {
                'id': str(user.id),
                'name': user.name,
                'lastname': user.lastname,
                'username': user.username,
            },
            'access_token': create_access_token(
                identity=str(user.id),
                fresh=True,
            ),
            'refresh_token': create_refresh_token(
                identity=str(user.id),
            ),
        }


class RefreshResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()

        user = User.objects.get(
            id=bson.objectid.ObjectId(user_id),
        )

        return {
            'message': 'Access token refreshed.',
            'access_token': create_access_token(
                identity=str(user.id),
                fresh=False,
            )
        }


class FreshLoginResource(Resource):

    def post(self):
        args = get_login_args()

        user = get_user_or_fail(
            args.get('identity'),
            args.get('password'),
        )

        return {
            'message': 'Successfully logged in.',
            'access_token': create_access_token(
                identity=str(user.id),
                fresh=True,
            ),
        }
