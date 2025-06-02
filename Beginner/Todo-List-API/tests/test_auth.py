import pytest

class TestUserRegistration:
    def test_register_user_sucess(self, client, test_user):
        response = client.post("/users/register", json=test_user)
        assert response.status_code == 201
        assert "token" in response.json()

    def test_register_user_duplicate_email(self, client, test_user):
        client.post("/users/register", json=test_user)
        response = client.post("/users/register", json=test_user)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_user_invalid_email(self, client):
        user_data = {
            "name": "Test User", 
            "email": "invalid-email", 
            "password": "testpassword123"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == 422
    
    def test_register_user_short_password(self, client):
        user_data = {
            "name": "Test User", 
            "email": "test@example.com", 
            "password": "123"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == 422
    
    def test_register_user_short_name(self, client):
        user_data = {
            "name": "T", 
            "email": "test@example.com", 
            "password": "testpassword123"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == 422

class TestUserLogin:
    def test_login_sucess(self, client, test_user):
        client.post("/users/register", json=test_user)
        login_data = {
            "email": test_user["email"], 
            "password": test_user["password"]
        }
        response = client.post("/users/login", json=login_data)
        assert response.status_code == 200
        assert "token" in response.json()

    def test_login_invalid_email(self, client):
        login_data = {
            "email": "nonexistent@example.com", 
            "password": "testpassword123"
        }
        response = client.post("/users/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_invalid_password(self, client, test_user):
        client.post("/users/register", json=test_user)
        login_data = {
            "email": test_user["email"], 
            "password": "wrongpassword"
        }
        response = client.post("/users/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]




# def test_register_user(client):
#     response = client.post(
#         "/auth/register",
#         json={"username": "testuser", "email": "test@example.com", "password": "password123"}
#     )
#     assert response.status_code == 200
