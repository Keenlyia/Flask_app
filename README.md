# 🚀 Flask File Upload & Log Processing API

This Flask-based API allows users to upload, extract, and filter files (TXT, ZIP, RAR). It also provides JWT authentication and log processing capabilities.

---

## ✨ Features

- 🔐 **User registration & authentication** (JWT-based)
- 📂 **File upload & extraction** (ZIP, RAR, TXT)
- 🔎 **File filtering** by name, type, or date
- 📝 **Log filtering** by date range or keyword

---

## ⚙️ Installation

### 📌 Prerequisites
- 🐍 Python 3.x
- 📦 pip

### 📥 Clone the Repository
```sh
git clone <your-repo-url>
cd <your-repo-folder>
```

### 📌 Install Dependencies
```sh
pip install -r requirements.txt
```

### 🛠 Database Initialization
```sh
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

---

## 🛠 Configuration
Edit `app.py` to modify settings such as:
- `SECRET_KEY` for JWT authentication
- `SQLALCHEMY_DATABASE_URI` for database configuration

---

## ▶️ Running the Application
```sh
python app.py
```

---

## 📡 API Endpoints

### 🔑 Authentication
#### 📝 Register a New User
```http
POST /register
```
**Request Body:**
```json
{
  "username": "user1",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "message": "User registered successfully!"
}
```

#### 🔐 User Login
```http
POST /login
```
**Request Body:**
```json
{
  "username": "user1",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "access_token": "your_jwt_token"
}
```

---

### 📂 File Management
#### 📤 Upload a File
```http
POST /upload
```
**Form Data:**
- `file`: (binary file data)

**Response:**
```json
{
  "message": "File uploaded successfully!"
}
```

#### 📋 Get Uploaded Files (JWT Required)
```http
GET /files
```
**Optional Query Parameters:**
- `filename`: Filter by filename
- `file_type`: Filter by file type
- `date`: Filter by upload date (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": 1,
    "filename": "logfile.txt",
    "file_path": "uploads/logfile.txt",
    "uploaded_at": "2024-03-12 10:30:15"
  }
]
```

---

### 📝 Log Processing
#### 📑 Get Logs from Files (JWT Required)
```http
GET /logs
```
**Optional Query Parameters:**
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `keyword`: Filter logs by keyword

**Response:**
```json
[
  {
    "timestamp": "2024-03-10 12:45:32",
    "message": "ERROR Something went wrong",
    "filename": "logfile.txt"
  }
]
```

---

## 📜 License
This project is licensed under the MIT License.
