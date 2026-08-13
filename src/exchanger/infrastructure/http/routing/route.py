from collections.abc import Callable
from dataclasses import dataclass

from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse

type Handler = Callable[[HttpRequest], HttpResponse]


@dataclass
class Route:
    method: str
    path: str
    handler: Handler
