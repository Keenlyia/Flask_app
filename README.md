Flask File Upload & Log Processing API Documentation

Overview

This Flask-based API allows users to upload, extract, and filter files (TXT, ZIP, RAR). It also provides JWT authentication and log processing capabilities.

Features

User registration & authentication (JWT-based)

File upload & extraction (ZIP, RAR, TXT)

File filtering by name, type, or date

Log filtering by date range or keyword

Installation

Prerequisites

Python 3.x

pip

Clone the Repository

git clone <your-repo-url>
cd <your-repo-folder>

Install Dependencies

pip install -r requirements.txt

Database Initialization

python
>>> from app import db
>>> db.create_all()
>>> exit()

Configuration

Edit app.py to modify settings such as:

SECRET_KEY for JWT authentication

SQLALCHEMY_DATABASE_URI for database configuration

Running the Application

python app.py

API Endpoints

Authentication

Register a new user

POST /register

Request Body:

{
  "username": "user1",
  "password": "securepassword"
}

Response:

{
  "message": "User registered successfully!"
}

User Login

POST /login

Request Body:

{
  "username": "user1",
  "password": "securepassword"
}

Response:

{
  "access_token": "your_jwt_token"
}

File Management

Upload a File

POST /upload

Form Data:

file: (binary file data)

Response:

{
  "message": "File uploaded successfully!"
}

Get Uploaded Files (JWT Required)

GET /files

Optional Query Parameters:

filename: Filter by filename

file_type: Filter by file type

date: Filter by upload date (YYYY-MM-DD)

Response:

[
  {
    "id": 1,
    "filename": "logfile.txt",
    "file_path": "uploads/logfile.txt",
    "uploaded_at": "2024-03-12 10:30:15"
  }
]

Log Processing

Get Logs from Files (JWT Required)

GET /logs

Optional Query Parameters:

start_date: Start date (YYYY-MM-DD)

end_date: End date (YYYY-MM-DD)

keyword: Filter logs by keyword

Response:

[
  {
    "timestamp": "2024-03-10 12:45:32",
    "message": "ERROR Something went wrong",
    "filename": "logfile.txt"
  }
]

License

This project is licensed under the MIT License.

