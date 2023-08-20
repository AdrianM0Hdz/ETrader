"""
Adding routes with a decorator for the controller sub-classes methods
is excesiveley complicated thus this apporach is preferred
"""

from typing import List, Tuple, Callable

from flask import Flask, Response, Blueprint

from .http_method import HTTPMethod
from .route_description import RouteDescription


class Controller:
    """Controller Mixin"""

    def __init__(self, name: str, url_prefix: str):
        self.__name = name
        self.__url_prefix = url_prefix
        self.__routes_description: List[RouteDescription] = []

    def add_route(
        self, endpoint: str, func: Callable[..., Response], http_method: HTTPMethod
    ):
        self.__routes_description.append(
            RouteDescription(endpoint, func.__name__, func, http_method)
        )

    def create_blueprint_from_self(self) -> Blueprint:
        blueprint = Blueprint(self.__name, self.__name)
        for route_description in self.__routes_description:
            blueprint.add_url_rule(
                route_description.endpoint,
                route_description.func_name,
                route_description.func,
                methods=[route_description.method.value],
            )
        return blueprint

    def add_controller_to_app(self, app: Flask):
        blueprint = self.create_blueprint_from_self()
        app.register_blueprint(blueprint, url_prefix=self.__url_prefix)
