from typing import Callable
from dataclasses import dataclass

from flask import Response

from .http_method import HTTPMethod


@dataclass(frozen=True)
class RouteDescription:
    endpoint: str
    func_name: str
    func: Callable[..., Response]
    method: HTTPMethod
