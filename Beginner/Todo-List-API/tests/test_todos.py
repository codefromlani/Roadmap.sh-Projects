import pytest

class TestTodoOperations:
    def test_create_todo_success(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description"
        }
        response = client.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == todo_data["title"]
        assert data["description"] == todo_data["description"]
        assert data["completed"] == False
        assert "id" in data

    def test_create_todo_without_auth(self, client):
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description"
        }
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 403  

    def test_create_todo_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalid-token"}
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description"
        }
        response = client.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 401

    def test_create_todo_empty_title(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        todo_data = {
            "title": "",
            "description": "Test Description"
        }
        response = client.post("/todos", json=todo_data, headers=headers)
        assert response.status_code == 422

    def test_get_todos_success(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        for i in range(3):
            todo_data = {
                "title": f"Test Todo {i+1}",
                "description": f"Test Description {i+1}"
            }
            client.post("/todos", json=todo_data, headers=headers)
        response = client.get("/todos", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "page" in data
        assert "limit" in data
        assert "total" in data
        assert len(data["data"]) == 3
        assert data["total"] == 3

    def test_get_todos_pagination(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        for i in range(5):
            todo_data = {
                "title": f"Test Todo {i+1}",
                "description": f"Test Description {i+1}"
            }
            client.post("/todos", json=todo_data, headers=headers)
        response = client.get("/todos?page=1&limit=2", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["data"]) == 2
        assert data["page"] == 1
        assert data["limit"] == 2
        assert data["total"] == 5

    def test_get_todos_without_auth(self, client):
        response = client.get("/todos")
        assert response.status_code == 403

    def test_update_todo_success(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        todo_data = {
            "title": "Original Title",
            "description": "Original Description"
        }
        create_response = client.post("/todos", json=todo_data, headers=headers)
        todo_id = create_response.json()["id"]

        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        }
        response = client.put(f"/todos/{todo_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["completed"] == True

    def test_update_nonexistent_todo(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
    
        update_data = {
            "title": "Updated Title"
        }
        response = client.put("/todos/999", json=update_data, headers=headers)
        assert response.status_code == 404

    def test_update_todo_without_auth(self, client):
        update_data = {
            "title": "Updated Title"
        }
        response = client.put("/todos/1", json=update_data)
        assert response.status_code == 403

    def test_delete_todo_success(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        todo_data = {
            "title": "To Be Deleted",
            "description": "This will be deleted"
        }
        create_response = client.post("/todos", json=todo_data, headers=headers)
        todo_id = create_response.json()["id"]
        response = client.delete(f"/todos/{todo_id}", headers=headers)
        assert response.status_code == 204
    
        get_response = client.get("/todos", headers=headers)
        todos = get_response.json()["data"]
        todo_ids = [todo["id"] for todo in todos]
        assert todo_id not in todo_ids

    def test_delete_nonexistent_todo(self, client, authenticated_user):
        token = authenticated_user["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.delete("/todos/999", headers=headers)
        assert response.status_code == 404

    def test_delete_todo_without_auth(self, client):
        response = client.delete("/todos/1")
        assert response.status_code == 403

class TestUserIsolation:
    def test_users_cannot_access_others_todos(self, client):
        user1_data = {
            "name": "User 1",
            "email": "user1@example.com",
            "password": "password123"
        }
        user1_response = client.post("/register", json=user1_data)
        user1_token = user1_response.json()["token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}
        
        todo_data = {
            "title": "User 1's Todo",
            "description": "Private todo"
        }
        todo_response = client.post("/todos", json=todo_data, headers=user1_headers)
        todo_id = todo_response.json()["id"]

        user2_data = {
            "name": "User 2",
            "email": "user2@example.com",
            "password": "password123"
        }
        user2_response = client.post("/register", json=user2_data)
        user2_token = user2_response.json()["token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}

        get_response = client.get("/todos", headers=user2_headers)
        assert len(get_response.json()["data"]) == 0

        update_data = {"title": "Hacked!"}
        update_response = client.put(f"/todos/{todo_id}", json=update_data, headers=user2_headers)
        assert update_response.status_code == 403
   
        delete_response = client.delete(f"/todos/{todo_id}", headers=user2_headers)
        assert delete_response.status_code == 403