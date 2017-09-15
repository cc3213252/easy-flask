# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'

from flask import Blueprint
from flask_restful import Resource, reqparse
from src.utils import (
    Api,
)
from src.modules.act import (
    get_acts_values,
    get_acts_graphics,
}
from src.utils.flk import make_response
from src.modules.authority import access_required
import logging
logger = logging.getLogger(__name__)

app = Blueprint('act', __name__)


class Acts(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'act_ids', type=list, location='json', required=True)

    # for test
    def get(self):
        return make_response(data = {'act_id': 1430, 'name': '买一送一'})


    @access_required
    def post(self):
        args = self.post_parser.parse_args()
        act_ids = args.get('act_ids')
        return get_acts_values(act_ids)


class ActsGraphics(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'act_ids', type=list, location='json', required=True)
        self.post_parser.add_argument('category_style', type=int, location='json')

    @access_required
    def post(self):
        args = self.post_parser.parse_args()
        act_ids = args.get('act_ids')
        category_style = args.get('category_style')
        return get_acts_graphics(act_ids, category_style)


def init_app(g_app):
    api = Api(app)
    api.add_resource(Acts, '', endpoint='card_acts')
    api.add_resource(ActsGraphics, '/graphics', endpoint='card_acts_graphics')

    g_app.register_blueprint(app, url_prefix='/acts')