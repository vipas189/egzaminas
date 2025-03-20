from routes.home_route import home_route
from routes.test_routes import test_routes


def routes(app):
    home_route(app)
    test_routes(app)  