async def test_register_creates_user(client):
    response = await client.post(
        "/auth/register", json={"email": "a@a.com", "password": "12345678"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "a@a.com"
    assert "hashed_password" not in data


async def test_register_duplicate_email_fails(client):
    payload = {"email": "dup@a.com", "password": "12345678"}
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 400


async def test_login_success(client):
    await client.post(
        "/auth/register", json={"email": "b@b.com", "password": "12345678"}
    )
    response = await client.post(
        "/auth/login", data={"username": "b@b.com", "password": "12345678"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password_fails(client):
    await client.post(
        "/auth/register", json={"email": "c@c.com", "password": "12345678"}
    )
    response = await client.post(
        "/auth/login", data={"username": "c@c.com", "password": "wrong"}
    )
    assert response.status_code == 401
