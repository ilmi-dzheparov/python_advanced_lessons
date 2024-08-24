import json
from wsgiref.simple_server import make_server


class App:
    def __init__(self):
        self.routes = {}
        self.not_found_route = self.not_found

    def route(self, path):
        def decorator(func):
            def wrapper(environ, start_response):
                status = "200 OK"
                response_headers = [("Content-type", "application/json")]
                start_response(status, response_headers)
                variables = self.extract_variables(environ.get("PATH_INFO"), path)
                return [json.dumps(func(**variables)).encode()]

            self.routes[path] = wrapper
            return wrapper

        return decorator

    def not_found(self, environ, start_response):
        status = "404 Not Found"
        response_headers = [("Content-type", "text/plain")]
        start_response(status, response_headers)
        return ['{"error": "Not found"}'.encode()]

    def extract_variables(self, path, route):
        parts = path.split("/")
        route_parts = route.split("/")
        if len(parts) != len(route_parts):
            return None
        variables = {}
        for i in range(len(route_parts)):
            if route_parts[i].startswith("<") and route_parts[i].endswith(">"):
                variable_name = route_parts[i][1:-1]
                variables[variable_name] = parts[i]
        return variables

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO")
        handler = None
        for route, func in self.routes.items():
            variables = self.extract_variables(path, route)
            if variables:
                handler = func
                break
        handler = handler
        if not handler:
            handler = self.routes.get(path, self.not_found_route)
        return handler(environ, start_response)


application = App()


@application.route("/hello/<name>")
def hello_name(name):
    return {"message": f"Hello {name}!"}


@application.route("/hello")
def hello():
    return {"message": "Hello World!"}


# if __name__ == "__main__":
#
#     server = make_server("127.0.0.1", 8000, application)
#     print("Serving on port 8000...")
#     server.serve_forever()
