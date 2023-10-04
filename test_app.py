from fastapi.testclient import TestClient
from main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Base

DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {
    get_db: get_db,
}

client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=test_engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=test_engine)

def test_create_user():
    user_data = {
        "user": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "secretpassword"
        },
        "addresses": [
            {
                "street": "123 Main St",
                "city": "City",
                "country": "Country"
            }
        ]
    }

    response = client.post("/users/", json=user_data)

    if response.status_code != 200:
        print(response.json())
    assert response.status_code == 200

    # Verify that the response contains the expected user data
    user_response = response.json()["user"]
    assert user_response["first_name"] == "John"
    assert user_response["last_name"] == "Doe"
    assert user_response["email"] == "johndoe@example.com"
    assert "password" not in user_response

def test_get_users_by_country():
    # Send a GET request to retrieve users by country
    response = client.get("/users/?country=Country")

    # Verify that the request was successful (response code 200)
    assert response.status_code == 200

    # Verify that the response contains at least one user
    users_response = response.json()
    assert len(users_response) >= 1

    # Verify that each user has the expected fields
    for user in users_response:
        assert "first_name" in user
        assert "last_name" in user
        assert "email" in user
        assert "password" not in user or user["password"] is None
