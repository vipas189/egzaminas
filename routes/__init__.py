<<<<<<< HEAD
=======
from routes.student_register_route import student_register_route
from routes.home_route import home_route
from routes.login_route import login_route
from routes.panel_route import panel_route
from routes.register_route import register_route
>>>>>>> origin/html-design-init

# from routes.admin_routes import admin_dashboard_route

def routes(app):
<<<<<<< HEAD
    pass
=======
    student_register_route(app)
    home_route(app)
    login_route(app)
    register_route(app)
    panel_route(app)
>>>>>>> origin/html-design-init
