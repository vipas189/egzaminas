from routes.home_route import home_route
from routes.login_route import login_route
from routes.register_route import register_route
from routes.panel_admin_route import panel_admin_route
from routes.file_upload_route import file_upload_route
from routes.panel_student_route import panel_student_route
from routes.panel_lecturer_route import panel_lecturer_route
from routes.panel_superadmin_route import panel_superadmin_route
from routes.student_route import student_routes
from routes.instructor_route import instructor_routes
from routes.program_route import program_routes
from routes.module_route import module_route


def routes(app):
    home_route(app)
    login_route(app)
    register_route(app)
    panel_admin_route(app)
    file_upload_route(app)
    panel_student_route(app)
    panel_lecturer_route(app)
    panel_superadmin_route(app)
    module_route(app)
    program_routes(app)
    student_routes(app)
    instructor_routes(app)
