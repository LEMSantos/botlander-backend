from flask_restful import Resource, reqparse, abort
from flask import Response
import json
import bson
from botlander.database.models import User
from http import HTTPStatus
from werkzeug.security import generate_password_hash
from mongoengine.errors import NotUniqueError
from flask_jwt_extended import (
    jwt_required,
)


class UserResource(Resource):

    @jwt_required
    def get(self, user_id):
        try:
            user = User.objects.get(
                id=bson.objectid.ObjectId(user_id)
            )
        except User.DoesNotExist:
            return {
                'message': 'User not found.',
            }, HTTPStatus.NOT_FOUND
        except bson.errors.InvalidId:
            return {
                'message': 'Invalid id sent.',
            }, HTTPStatus.BAD_REQUEST

        return {
            'message': 'User found successfully',
            'user': {
                'id': str(user.id),
                'name': user.name,
                'lastname': user.lastname,
                'email': user.email,
                'username': user.username,
            }
        }


class UserResourceList(Resource):

    def post(self):
        from validate_email import validate_email

        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('lastname', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args(strict=True)

        if not validate_email(args.get('email')):
            abort(
                Response(
                    json.dumps({
                        'message': {
                            'email': 'Email is not in the correct format.',
                        },
                    }),
                    status=HTTPStatus.BAD_REQUEST,
                    content_type='application/json',
                )
            )

        try:
            user = User(
                name=args.get('name'),
                lastname=args.get('lastname'),
                username=args.get('username'),
                email=args.get('email'),
                password=generate_password_hash(args.get('password')),
            )
            user.save()
        except NotUniqueError:
            return {
                'message': 'User already exists.'
            }, HTTPStatus.CONFLICT

        return {
            'message': 'User created successfully.'
        }
