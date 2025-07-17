def test_register_success(client):
    response = client.post(
        "/api/register",
        json={
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Account created successfully"


def test_register_duplicate_email(client):
    # Register once
    client.post(
        "/api/register",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane@example.com",
            "password": "secret123",
        },
    )
    # Register again with same email
    response = client.post(
        "/api/register",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 401
    assert "already exists" in response.get_json()["error"]


def test_register_invalid_email_format(client):
    response = client.post(
        "/api/register",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane-example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 400
    assert "value is not a valid email" in response.get_json()["error"][0]["msg"]


def test_register_password_too_short(client):
    password = "1234"
    response = client.post(
        "/api/register",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane@example.com",
            "password": password,
        },
    )
    assert response.status_code == 400
    assert len(password) < response.get_json()["error"][0]["ctx"]["min_length"]


def test_login_success(client):
    # Register first
    client.post(
        "/api/register",
        json={
            "firstName": "Max",
            "lastName": "Payne",
            "email": "max@example.com",
            "password": "bullet",
        },
    )
    # Now login
    response = client.post(
        "/api/login", json={"email": "max@example.com", "password": "bullet"}
    )
    assert response.status_code == 200
    assert "Login successful" in response.get_json()["message"]


def test_login_invalid_password(client):
    client.post(
        "/api/register",
        json={
            "firstName": "Max",
            "lastName": "Payne",
            "email": "max@example.com",
            "password": "bullet",
        },
    )
    response = client.post(
        "/api/login", json={"email": "max@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid password"


def test_login_invalid_email_format(client):
    response = client.post(
        "/api/login",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane-example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 400
    assert "value is not a valid email" in response.get_json()["error"][0]["msg"]


def test_login_password_too_short(client):
    password = "1234"
    response = client.post(
        "/api/login",
        json={
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane@example.com",
            "password": password,
        },
    )
    assert response.status_code == 400
    assert len(password) < response.get_json()["error"][0]["ctx"]["min_length"]


def test_me_not_authenticated(client):
    response = client.get("/api/me")
    assert response.status_code == 401
    assert response.get_json()["message"] == "Not authenticated"
