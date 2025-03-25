from routes.test_route import test_routes
from routes.group_route import group_routes


def routes(app):
    test_routes(app)
    group_routes(app)  