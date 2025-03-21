from routes.home_route import home_route
from routes.login_route import login_route
from routes.panel_route import panel_route


def routes(app):
    home_route(app)
    login_route(app)
    panel_route(app)
   
