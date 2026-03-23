import pytest
from app.models import Agent


@pytest.mark.asyncio
async def test_list_agents(client, auth_headers, db_session):
    # Seed a test agent
    agent = Agent(slug="ceo", display_name="Victor CEO", role="CEO")
    db_session.add(agent)
    await db_session.commit()

    response = await client.get("/agents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_agent_by_slug(client, auth_headers, db_session):
    agent = Agent(slug="ceo", display_name="Victor CEO", role="CEO")
    db_session.add(agent)
    await db_session.commit()

    response = await client.get("/agents/ceo", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["slug"] == "ceo"
    assert response.json()["display_name"] == "Victor CEO"


@pytest.mark.asyncio
async def test_get_agent_not_found(client, auth_headers):
    response = await client.get("/agents/nonexistent", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_agents_requires_auth(client):
    response = await client.get("/agents")
    assert response.status_code == 403
