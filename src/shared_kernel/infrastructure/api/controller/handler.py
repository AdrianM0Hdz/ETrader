"""
Decorator to declare a command handler
"""
from typing import Callable
from dataclasses import is_dataclass

from flask import request, jsonify, Response


def handler(request_dataclass_type: type):
    assert is_dataclass(request_dataclass_type)

    def decorator(func: Callable):
        assert is_dataclass(func.__annotations__["return"])

        def wrapper(self, *args, **kwargs) -> Response:
            """Will decorate methods only"""
            request_body = request.get_json()

            if request_body is None:
                response = jsonify(msg="no json body provided")
                response.status = 400
                return response

            request_dto = request_dataclass_type(**request_body)

            response_dto = func(self, request_dto, *args, **kwargs)
            assert is_dataclass(response_dto)

            return jsonify(**response_dto.__dict__)

        return wrapper

    return decorator
