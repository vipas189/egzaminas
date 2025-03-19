from routes.module_route import module_bp

def routes(app):
    app.register_blueprint(module_bp)