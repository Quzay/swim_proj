import pytest
import json

@pytest.mark.integration
def test_user_register_success(client):
    response = client.post("/user/register", json ={
        "username": "Maksym",
        "email": "Qwertyn@gmail.com",
        "password": "Mak123215",
        "age": 46
        })
    assert response.status_code == 201

@pytest.mark.integration
def test_user_register_failure(client):
    response = client.post("/user/register" , json = {
        "username" : "15",
        "email" : "Qwertyn@gmail.com",
        "password" : "123",
        "age" : 3
    })
    assert response.status_code == 422

@pytest.mark.integration
def test_user_login_exists(client):
    client.post("/user/register", json={
        "username": "Maksym",
        "email": "Maks@gmail.com",
        "password": "testpass",
        "age": 25
    })
    response = client.post("/user/login", json={
        "email": "Maks@gmail.com",
        "password": "testpass"
    })
    assert response.status_code == 200

@pytest.mark.integration
def test_user_login_not_exitst(client):
    client.post("/user/register", json={
        "username": "Maksym",
        "email": "Maks@gmail.com",
        "password": "testpass",
        "age": 25
    })
    response = client.post("/user/login" , json = {
        "email": "Maks@gmail.com",
        "password": "WrongPass"
    })
    assert response.status_code == 400