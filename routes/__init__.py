from routes.student_register_route import student_register_route
from routes.home_route import home_route
from routes.login_route import login_route
from routes.register_route import register_route


def routes(app):
    student_register_route(app)
    home_route(app)
    login_route(app)
    register_route(app)
    panel_route(app)
