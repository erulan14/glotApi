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
        response = self.__handle_request(request)
        await response(scope, receive, send)

    @staticmethod
    def __default_response():
        """
        Return Not Found
        """
        response = HTMLResponse("<h1>Not Found</h1>")
        response.status_code = 404
        return response

    def __find_handler(self, request_path):
        """

        :param request_path:
        :return hanlder and parse_result:
        """
        for path, handler in self.__routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def __handle_request(self, request):
        handler, kwargs = self.__find_handler(request_path=request.scope.get("path"))
        if handler is not None:
            response = handler(request, **kwargs)
        else:
            response = self.__default_response()
        return response

    def route(self, path):
        def wrapper(handler):
            self.__routes[path] = handler
            return handler
        return wrapper

