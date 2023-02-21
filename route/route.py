r"""Welcome to the home page"""

from __future__ import annotations

from flask import Flask, request, jsonify, Response
from marshmallow import Schema, fields, ValidationError
from typing import Union


paths = []


class Route:

    path: str

    def __init__(self, path):
        self.path = path


class RouteMapping(Route):

    res: str

    def __init__(self, path, res):
        super().__init__(path)
        self.res = res


class RouteSchema(Schema):
    path = fields.Str()


class RouteMappingSchema(RouteSchema):
    res = fields.Str()


def create_route_mapping(path: str, res: str) -> Union[RouteMapping, None]:

    for rm in paths:
        if getattr(rm, 'path') == path:
            return None

    return RouteMapping(path=path, res=res)


def create_app():
    app = Flask(__name__)

    @app.route("/path", methods=['POST', 'PUT'])
    def with_route():

        schema = RouteMappingSchema()
        try:
            request_data = request.get_json()
            result = schema.load(request_data)
        except ValidationError as e:
            return jsonify(e.messages), 400

        route = result

        route_map = create_route_mapping(path=route.get('path'), res=route.get('res'))
        if route_map:
            paths.append(route_map)
            return {
                'status': 'ok'
            }, 200
        else:
            return {
                'status': 'already exists'
            }, 200

    @app.route("/search", methods=['GET'])
    def get_route():

        schema = RouteSchema()
        try:
            request_data = request.get_json()
            result = schema.load(request_data)
        except ValidationError as e:
            return jsonify(e.messages), 400

        path = result

        for rm in paths:
            if str(getattr(rm, 'path')) == str(path.get('path')):
                return {
                    "ok": True,
                    "message": getattr(rm, 'res'),
                }

        return {
            "ok": False,
            "message": "not found",
        }

    @app.route("/")
    def default():
        return Response(__doc__)

    @app.errorhandler(404)
    def handle_other(e):
        return 'not found', e

    return app


if __name__ == '__main__':
    app = create_app()
