# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'

from flask import Blueprint
from flask_restful import Resource, reqparse
from src.utils import (
    Api,
)
from src.modules.card import (
    get_card_values,
    get_card_benefits,
    get_card_benefits_graphics,
    get_card_benefit,
    update_card_benefit,
)
from src.modules.authority import access_required
import logging
logger = logging.getLogger(__name__)

app = Blueprint('card', __name__)


class Card(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('first_code', type=str, location='args', required=True)
        self.get_parser.add_argument('last_code', type=str, location='args', required=True)
        self.get_parser.add_argument('card_id', type=str, location='args', required=True)


    @access_required
    def get(self):
        args = self.get_parser.parse_args()
        first_code = args.get('first_code')
        last_code = args.get('last_code')
        card_id = args.get('card_id')
        return get_card_values(first_code, last_code, card_id)


class Benefits(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('first_code', type=str, location='args', required=True)
        self.get_parser.add_argument('last_code', type=str, location='args', required=True)
        self.get_parser.add_argument('card_id', type=str, location='args', required=True)


    @access_required
    def get(self):
        args = self.get_parser.parse_args()
        first_code = args.get('first_code')
        last_code = args.get('last_code')
        card_id = args.get('card_id')
        return get_card_benefits(first_code, last_code, card_id)


class BenefitsGraphics(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('first_code', type=str, location='args', required=True)
        self.get_parser.add_argument('last_code', type=str, location='args', required=True)
        self.get_parser.add_argument('card_id', type=str, location='args', required=True)
        self.get_parser.add_argument('category_style', type=int, location='args', required=True)


    @access_required
    def get(self):
        args = self.get_parser.parse_args()
        first_code = args.get('first_code')
        last_code = args.get('last_code')
        card_id = args.get('card_id')
        category_style = args.get('category_style')
        return get_card_benefits_graphics(first_code, last_code, card_id, category_style)


class Benefit(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('benefit', type=list, location='json', required=True)

        self.patch_parser = reqparse.RequestParser()
        self.patch_parser.add_argument('card_id', type=str, location='json', required=True)
        self.patch_parser.add_argument('benefit_id', type=str, location='json', required=True)
        self.patch_parser.add_argument('direction', type=int, location='json', required=True)
        self.patch_parser.add_argument('count', type=int, location='json', required=True)
        self.patch_parser.add_argument('year_benefit', type=float, location='json', required=True)


    @access_required
    def post(self):
        args = self.post_parser.parse_args()
        benefit = args.get('benefit')
        return get_card_benefit(benefit)


    @access_required
    def patch(self):
        args = self.patch_parser.parse_args()
        card_id = args.get('card_id')
        benefit_id = args.get('benefit_id')
        direction = args.get('direction')
        count = args.get('count')
        year_benefit = args.get('year_benefit')
        return update_card_benefit(card_id, benefit_id, direction, count, year_benefit)


def init_app(g_app):
    api = Api(app)
    api.add_resource(Card, '', endpoint='card_value')
    api.add_resource(Benefits, '/benefits', endpoint='card_benefits')
    api.add_resource(BenefitsGraphics, '/benefits/graphics', endpoint='card_benefits_graphics')
    api.add_resource(Benefit, '/benefit', endpoint='card_benefit')

    g_app.register_blueprint(app, url_prefix='/card')