import inspect

from webob import Request, Response
from parse import parse


class API:

    def __init__(self):
        self.routes = {}

    def route(self, path):
        assert path not in self.routes, "Such route already exists."
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            if inspect.isclass(handler):
                handler_function = getattr(handler(), request.method.lower(), None)
                print(handler_function.__name__)
                print(handler_function(request, response, **kwargs))
                if handler_function is None:
                    raise AttributeError("Method now allowed", request.method)
                pass   # class based handler is being used
            else:
                handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."