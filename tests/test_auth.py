from httpx import AsyncClient
import pytest
from app.main import app



@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "id": 1}

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}
