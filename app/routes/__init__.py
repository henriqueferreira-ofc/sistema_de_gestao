from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Importa e registra os blueprints (módulos)
    from app.routes.main_routes import main_bp
    from app.routes.data_routes import data_bp
    from app.routes.graph_routes import graph_bp
    from app.routes.diagnostic_routes import diagnostic_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(graph_bp)
    app.register_blueprint(diagnostic_bp)

    return app
