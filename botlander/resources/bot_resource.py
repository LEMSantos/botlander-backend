from flask_restful import Resource, reqparse, abort
from flask import Response, request
import json
import bson
from botlander.database.models import User
from botlander.database.models import Bot
from http import HTTPStatus
from werkzeug.datastructures import FileStorage
from mongoengine.errors import NotUniqueError
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_identity,
)


def bot_validation(bot_id):
    try:
        bot = Bot.objects.get(
            id=bson.objectid.ObjectId(bot_id)
        )
    except Bot.DoesNotExist:
        abort(HTTPStatus.NOT_FOUND)
    except bson.errors.InvalidId:
        abort(HTTPStatus.BAD_REQUEST)

    return bot


class BotResource(Resource):

    @jwt_required
    def get(self, bot_id):
        bot = bot_validation(bot_id)

        payload = json.loads(bot.to_json())

        payload['id'] = payload['_id']['$oid']
        payload['user_id'] = payload['user_id']['$oid']

        if 'image' in payload:
            payload['image'] = f'{request.base_url}/image'

        payload.pop('_id')

        return {
            'message': 'Bot found successfully',
            'bot': {
                **payload,
            }
        }

    @fresh_jwt_required
    def put(self, bot_id):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('description')
        parser.add_argument(
            'image',
            type=FileStorage,
            location='files',
        )
        parser.add_argument('telegram_token')

        args = parser.parse_args(strict=True)

        bot = bot_validation(bot_id)

        if args.get('image') is not None:
            bot.image.replace(args.get('image'))

        args.pop('image')

        bot.save()
        bot.update(**args)
        bot.reload()

        payload = json.loads(bot.to_json())

        payload['id'] = payload['_id']['$oid']
        payload['user_id'] = payload['user_id']['$oid']

        if 'image' in payload:
            payload['image'] = f'{request.base_url}/image'

        payload.pop('_id')

        return {
            'message': 'Bot updated_successfully.',
            'new_bot': {
                **payload,
            }
        }

    @fresh_jwt_required
    def delete(self, bot_id):
        bot = bot_validation(bot_id)
        bot.delete()

        return {
            'message': 'Bot deleted successfully.',
        }


class BotResourceList(Resource):

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id', required=True)

        args = parser.parse_args(strict=True)

        try:
            bots = Bot.objects(
                user_id=bson.objectid.ObjectId(args.get('user_id'))
            )
        except bson.errors.InvalidId:
            return {
                'message': 'Invalid user_id sent.',
            }, HTTPStatus.BAD_REQUEST

        payload = json.loads(bots.to_json())

        for bot in payload:
            bot['id'] = bot['_id']['$oid']
            bot['user_id'] = bot['user_id']['$oid']

            if 'image' in bot:
                bot['image'] = f'{request.base_url}/{bot.get("id")}/image'

            bot.pop('_id')

        return {
            'bots': payload,
        }

    @fresh_jwt_required
    def post(self):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('description')
        parser.add_argument(
            'image',
            type=FileStorage,
            location='files',
        )
        parser.add_argument('telegram_token')

        args = parser.parse_args(strict=True)
        args.update({
            'user_id': bson.objectid.ObjectId(user_id)
        })

        try:
            bot = Bot(
                **args,
            )
            bot.save()
        except NotUniqueError:
            return {
                'message': 'Bot already exists.',
            }, HTTPStatus.CONFLICT

        return {
            'message': 'Bot created successfully.',
        }
