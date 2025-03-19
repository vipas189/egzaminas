from routes.home_route import home_route
from routes.admin_routes import admin_routes

def routes(app):
    home_route(app)
    admin_routes(app)
