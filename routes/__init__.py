from routes.module_route import home_route  # Pakeista į home_route vietoj module_bp
from routes.student_register_route import student_register_route
# from routes.home_route import home_route
from routes.login_route import login_route
from routes.panel_route import panel_route
from routes.register_route import register_route
from routes.program_route import student_routes

def routes(app):
    home_route(app)  # Pakeista į home_route(app) vietoj app.register_blueprint(module_bp)
    student_register_route(app)
    login_route(app)
    register_route(app)
    panel_route(app)
    student_routes(app)