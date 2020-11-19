from flask_restful import Resource, abort
from botlander.database.models import Bot
from http import HTTPStatus
import bson
from flask import send_file


class BotImageResource(Resource):

    def get(self, bot_id):
        try:
            bot = Bot.objects.get(
                id=bson.objectid.ObjectId(bot_id)
            )
        except Bot.DoesNotExist:
            abort(HTTPStatus.NOT_FOUND)
        except bson.errors.InvalidId:
            abort(HTTPStatus.NOT_FOUND)

        if not bool(bot.image):
            abort(HTTPStatus.NOT_FOUND)

        return send_file(bot.image, mimetype=f'image/{bot.image.format}')
