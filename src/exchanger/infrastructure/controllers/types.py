from dataclasses import dataclass, field


@dataclass
class HttpRequest:
    method: str
    path: str
    headers: dict
    query: dict | None = field(default=None)
    body: dict | list | None = field(default=None)
    path_params: dict | None = field(default=None)


@dataclass
class HttpResponse:
    status_code: int
    headers: dict
    body: dict | list | None = field(default=None)
