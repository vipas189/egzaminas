from routes.home_route import home_route
from routes.login_route import login_route
from routes.panel_superadmin_route import panel_superadmin_route
from routes.panel_admin_route import panel_admin_route
from routes.file_upload_route import file_upload_route



def routes(app):
    home_route(app)
    login_route(app)
    panel_superadmin_route(app)
    panel_admin_route(app)
    file_upload_route(app)
    
   
