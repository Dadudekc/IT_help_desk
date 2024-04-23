from httpx import AsyncClient
import pytest
from app.main import app


@pytest.mark.asyncio
async def test_ask_question():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "What does IT help desk handle?"})
    assert response.status_code == 200
    assert "password resets" in response.json()['answer']
