import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from tasks.models import Task

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass"
    )

@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post("/api/auth/jwt/create/", {
        "email": user.email,
        "password": "testpass"
    })
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client

@pytest.fixture
def task(user):
    return Task.objects.create(
        user=user,
        title="Test Task",
        description="Test Description",
        deadline=timezone.now() + timezone.timedelta(days=1),
        is_completed=False,
        is_alerted=False
    )


@pytest.mark.django_db
def test_register_user(api_client):
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass123"
    }
    response = api_client.post("/api/auth/users/", data)
    assert response.status_code == 201
    assert User.objects.filter(email="newuser@example.com").exists()

@pytest.mark.django_db
def test_jwt_authentication(api_client, user):
    response = api_client.post("/api/auth/jwt/create/", {
        "email": user.email,
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_create_task(auth_client, user):
    data = {
        "title": "New Task",
        "description": "New Description",
        "deadline": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
        "is_completed": False,
        "is_alerted": False
    }
    response = auth_client.post("/api/tasks/", data, format="json")
    assert response.status_code == 201
    assert Task.objects.filter(user=user, title="New Task").exists()

@pytest.mark.django_db
def test_get_task_list(auth_client, task):
    response = auth_client.get("/api/tasks/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Test Task"

@pytest.mark.django_db
def test_get_task_detail(auth_client, task):
    response = auth_client.get(f"/api/tasks/{task.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Test Task"

@pytest.mark.django_db
def test_update_task(auth_client, task):
    data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "deadline": (timezone.now() + timezone.timedelta(days=3)).isoformat(),
        "is_completed": True,
        "is_alerted": False
    }
    response = auth_client.put(f"/api/tasks/{task.id}/", data, format="json")
    assert response.status_code == 200
    task.refresh_from_db()
    assert task.title == "Updated Task"
    assert task.is_completed is True

@pytest.mark.django_db
def test_delete_task(auth_client, task):
    response = auth_client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == 204
    assert not Task.objects.filter(id=task.id).exists()

@pytest.mark.django_db
def test_filter_tasks(auth_client, user):
    Task.objects.create(
        user=user,
        title="Completed Task",
        deadline=timezone.now() + timezone.timedelta(days=1),
        is_completed=True
    )
    Task.objects.create(
        user=user,
        title="Incomplete Task",
        deadline=timezone.now() + timezone.timedelta(days=1),
        is_completed=False
    )
    response = auth_client.get("/api/tasks/?is_completed=true")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Completed Task"