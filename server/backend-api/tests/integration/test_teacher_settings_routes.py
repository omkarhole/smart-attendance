import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_manage_schedule(client: AsyncClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    schedule_item = {
        "day": "Monday",
        "periods": [
            {
                "subject": "Mathematics",
                "start_time": "10:00",
                "end_time": "11:00",
                "room": "101",
            }
        ],
    }

    # Try the standard schedule creation/update route
    response = await client.post("/schedule", json=schedule_item, headers=headers)

    if response.status_code == 404:
        # Fallback to teacher-specific route
        response = await client.post(
            "/teacher/schedule", json=schedule_item, headers=headers
        )

    assert response.status_code in [200, 201, 204], (
        f"Schedule update failed: {response.text}"
    )

    if response.status_code != 204 and response.content:
        data = response.json()
        assert isinstance(data, dict)
