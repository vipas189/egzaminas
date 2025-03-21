from routes.student_register_route import student_register_route
from routes.home_route import home_route
from routes.login_route import login_route
from routes.register_route import register_route
from routes.panel_admin_route import panel_admin_route
from routes.panel_lecturer_route import panel_lecturer_route
from routes.panel_student_route import panel_student_route


def routes(app):
    student_register_route(app)
    home_route(app)
    login_route(app)
    register_route(app)
    panel_admin_route(app)
    panel_lecturer_route(app)
    panel_student_route(app)
