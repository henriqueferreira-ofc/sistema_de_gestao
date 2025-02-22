from app import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":
    print("Servidor rodando em http://0.0.0.0:8080")
    serve(app, host='0.0.0.0', port=8080)