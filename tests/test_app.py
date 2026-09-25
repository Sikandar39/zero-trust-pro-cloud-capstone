from app import app


def test_home_page():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_about_page():

    client = app.test_client()

    response = client.get("/about")

    assert response.status_code == 200


def test_domains_page():

    client = app.test_client()

    response = client.get("/domains")

    assert response.status_code == 200


def test_programs_page():

    client = app.test_client()

    response = client.get("/programs")

    assert response.status_code == 200


def test_health_endpoint():

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json["application"] == "online"