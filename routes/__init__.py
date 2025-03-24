from routes.module_route import home_route 
# from routes.student_register_route import student_register_route
# from routes.login_route import login_route
# from routes.panel_route import panel_route
# from routes.register_route import register_route
from routes.program_route import program_routes  # Pakeista iš student_routes į program_routes
from routes.student_route import student_routes

def routes(app):
    home_route(app)  
    # # student_register_route(app)
    # # login_route(app)
    # # register_route(app)
    # # panel_route(app)
    program_routes(app)  
    student_routes(app)