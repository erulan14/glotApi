from starlette.requests import Request
from starlette.responses import *
from .types import Scope, Receive, Send
from parse import parse
import asyncio
import nest_asyncio
nest_asyncio.apply()


class App:
    __routes: dict = {}

    def __int__(self):
        pass

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope=scope, receive=receive)
        response = self.__handle_request(request)
        await response(scope, receive, send)

    @staticmethod
    def __default_response():
        """Return Not Found"""
        return HTMLResponse("<h1>Not Found</h1>", status_code=404)

    @staticmethod
    def __method_not_allowed():
        """Return Method not Allowed"""
        return HTMLResponse("<h1>Method Not Allowed</h1>", status_code=405)

    def __find_handler(self, request_path, request):
        """

        :param request_path:
        :return hanlder and parse_result:
        """
        for path, obj in self.__routes.items():
            parse_result = parse(path, request_path)
            handler = obj.get("handler")
            if parse_result is not None:
                if request.method in obj.get("methods"):
                    return handler, request.method, parse_result.named,
                else:
                    return handler, None, parse_result.named
        return None, None, None

    def __handle_request(self, request):
        handler, method, kwargs = self.__find_handler(
            request_path=request.scope.get("path"),
            request=request
        )
        if handler is not None:
            if method is not None:
                response = handler(request, **kwargs)

                if isinstance(response, str):
                    response = HTMLResponse(response)

                if isinstance(response, (list, dict)):
                    response = JSONResponse(response)
            else:
                response = self.__method_not_allowed()
        else:
            response = self.__default_response()
        return response

    @staticmethod
    def get_body(request):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(request.body())
        return result

    @staticmethod
    def get_form(request):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(request.form())
        return result

    @staticmethod
    def get_json(request):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(request.json())
        return result

    @staticmethod
    def read_file(file):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(file.read())
        return result

    def route(self, path, methods=None):
        if methods is None:
            methods = ["GET"]

        def wrapper(handler):
            self.__routes[path] = {"methods": methods, "handler": handler}
            return handler
        return wrapper

