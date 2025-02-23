import pytest
from app import app

def test_pagina_inicial():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_visualizacao_dados():
    client = app.test_client()
    response = client.get('/visualizar')
    assert response.status_code == 200 