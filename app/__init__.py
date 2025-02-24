from flask import Flask

def create_app():
    app = Flask(__name__, 
                template_folder='templates',  
                static_folder='static')
    
    with app.app_context():
        from .scripts import dashboard
        app = dashboard.init_dashboard(app)
    
    # Registrar blueprints
    from app.routes.main_routes import main_bp
    from app.routes.graph_routes import graph_bp
    from app.routes.diagnostic_routes import diagnostic_bp
    from app.routes.data_routes import data_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(graph_bp)
    app.register_blueprint(diagnostic_bp)
    app.register_blueprint(data_bp)
    
    return app