"""
Tests for project endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.models import ProjectStatus


def test_create_project(client: TestClient):
    """Test creating a new project."""
    project_data = {
        "name": "Test Project",
        "description": "A test project",
        "status": "planning"
    }
    
    response = client.post("/api/v1/projects/", json=project_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["description"] == project_data["description"]
    assert data["status"] == project_data["status"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_project(client: TestClient):
    """Test getting a project by ID."""
    # First create a project
    project_data = {
        "name": "Test Project",
        "description": "A test project"
    }
    
    create_response = client.post("/api/v1/projects/", json=project_data)
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == project_data["name"]


def test_get_nonexistent_project(client: TestClient):
    """Test getting a project that doesn't exist."""
    response = client.get("/api/v1/projects/999")
    assert response.status_code == 404


def test_list_projects(client: TestClient):
    """Test listing projects."""
    # Create a few projects
    for i in range(3):
        project_data = {
            "name": f"Test Project {i}",
            "description": f"Test project {i}"
        }
        client.post("/api/v1/projects/", json=project_data)
    
    # List projects
    response = client.get("/api/v1/projects/")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert len(data["items"]) == 3
    assert data["total"] == 3


def test_update_project(client: TestClient):
    """Test updating a project."""
    # Create a project
    project_data = {
        "name": "Test Project",
        "description": "A test project"
    }
    
    create_response = client.post("/api/v1/projects/", json=project_data)
    project_id = create_response.json()["id"]
    
    # Update it
    update_data = {
        "name": "Updated Project",
        "status": "active"
    }
    
    response = client.put(f"/api/v1/projects/{project_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["status"] == update_data["status"]
    assert data["description"] == project_data["description"]  # Should remain unchanged


def test_delete_project(client: TestClient):
    """Test deleting a project."""
    # Create a project
    project_data = {
        "name": "Test Project",
        "description": "A test project"
    }
    
    create_response = client.post("/api/v1/projects/", json=project_data)
    project_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/api/v1/projects/{project_id}")
    assert get_response.status_code == 404
