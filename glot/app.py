from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from .types import Scope, Receive, Send
from parse import parse


class App:
    __routes: dict = {}

    def __int__(self):
        #self.__routes: dict = {}
        pass

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope=scope, receive=receive)
        response = self.handle_request(request)
        await response(scope, receive, send)

    @staticmethod
    def default_response():
        response = HTMLResponse("<h1>Not Found</h1>")
        response.status_code = 404
        return response

    def find_handler(self, request_path):
        for path, handler in self.__routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        handler, kwargs = self.find_handler(request_path=request.scope.get("path"))
        if handler is not None:
            response = handler(request, **kwargs)
        else:
            response = self.default_response()
        return response

    def route(self, path):
        def wrapper(handler):
            self.__routes[path] = handler
            return handler
        return wrapper

