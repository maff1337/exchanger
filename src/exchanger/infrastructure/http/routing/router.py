from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.http.routing.route import Handler, Route


class Router:
    def __init__(self) -> None:
        self._routes: list[Route] = []
    
    def add_route(
        self,
        method: str,
        path: str,
        handler: Handler
    ) -> None:
        self._routes.append(
            Route(
                method.upper(),
                path,
                handler
            )
        )
        
    def handle(self, request: HttpRequest) -> HttpResponse:
        for route in self._routes:
            if  route.method != request.method:
                continue
            
            path_params = self._match_path(
                route.path,
                request.path
            )
            
            if path_params is None:
                continue
            
            request.path_params = path_params
            
            return route.handler(request)
        
        return HttpResponse(
            status_code=404,
            headers={'Content-Type': 'application/json'},
            body={'error': 'URL Not Found'}
        )
    
    def _match_path(
        self, 
        route_path: str, 
        request_path: str
    ) -> dict[str, str] | None:
        
        route_parts = route_path.strip('/').split('/')
        request_parts = request_path.strip('/').split('/')
        
        if len(route_parts) != len(request_parts):
            return None
        
        params: dict[str, str] = {}
        
        for route_part, request_part in zip(
            route_parts,
            request_parts
        ):
            if route_part.startswith('{') and route_part.endswith('}'):
                param_name = route_part[1:-1]
                params[param_name] = request_part
                continue
            
            if route_part != request_part:
                return None
        
        return params
