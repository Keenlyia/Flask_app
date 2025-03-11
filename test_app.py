import pytest
from flask import Flask
from main import app, db, User, UploadedFile


@pytest.fixture
def client():
    # Setting up the test client for making HTTP requests during tests
    with app.test_client() as client:
        yield client


@pytest.fixture
def init_db():
    # Create all database tables before tests
    with app.app_context():
        db.create_all()

        # Check if the user already exists before adding it
        existing_user = User.query.filter_by(username="testuser").first()
        if not existing_user:
            # Add a test user if it doesn't exist
            user = User(username="testuser", password="password123")
            db.session.add(user)

        # Add a test file if needed
        file1 = UploadedFile(filename="test_log.txt", file_path="uploads/test_log.txt", file_type="txt")
        db.session.add(file1)

        db.session.commit()

    # Yield the database session to be used in the tests
    yield db


# Test for user registration
def test_register(client):
    response = client.post('/register', json={
        'username': 'user1223',
        'password': 'password123'
    })
    # Check if the registration was successful (status code 201)
    assert response.status_code == 201


# Test for user login
def test_login(client):
    response = client.post('/login', json={
        'username': 'user1223',
        'password': 'password123'
    })
    # Check if the login was successful (status code 200)
    assert response.status_code == 200
    # Check if the access token is returned in the response
    assert b"access_token" in response.data


# Test for file upload
def test_upload_file(client):
    # Create a test log file
    with open("test_log.txt", "w") as f:
        f.write("This is a test log")

    # Open the test log file for reading and upload it
    with open("test_log.txt", "rb") as f:
        response = client.post('/upload', data={
            'file': (f, 'test_log.txt')
        })

    # Check if the file upload was successful (status code 200)
    assert response.status_code == 200
    # Check if the success message is returned in the response
    assert b"File test_log.txt uploaded successfully!" in response.data


# Test for filtering logs by date
def test_get_logs_by_date(client, init_db):
    # Send a GET request to filter logs by date range
    response = client.get('/logs?start_date=2024-03-15&end_date=2024-03-18')

    # Check if the request was successful (status code 200)
    assert response.status_code == 200
    print(response.data)  # Print the test result

    # Check if logs within the date range are included in the response
    assert b"2024-03-15" in response.data
    assert b"2024-03-16" in response.data
    assert b"2024-03-17" in response.data

    # Ensure that logs before March 15th are not included
    assert b"2024-03-11" not in response.data


# Test for filtering logs by keyword
def test_get_logs_by_keyword(client):
    # Send a GET request to filter logs by the keyword "error"
    response = client.get('/logs?keyword=error')

    # Check if the request was successful (status code 200)
    assert response.status_code == 200
    # Ensure that logs containing the keyword "error" are included in the response
    assert b"error" in response.data
