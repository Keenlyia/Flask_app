import os
import re
import zipfile
import rarfile
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from sqlalchemy import func

# Initialize Flask application
app = Flask(__name__)

# Configure database settings
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///SQLite.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='your_secret_key',
    UPLOAD_FOLDER='uploads'
)

# Initialize database and JWT authentication
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'zip', 'rar'}

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper functions

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_archive(file_path, extract_to):
    """Extracts ZIP and RAR archives to the specified directory"""
    try:
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif file_path.endswith('.rar'):
            with rarfile.RarFile(file_path) as rf:
                rf.extractall(extract_to)
    except Exception as e:
        print(f"Error extracting archive: {e}")

# User registration
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    db.session.add(User(username=data['username'], password=data['password']))
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# User login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        return jsonify({"access_token": create_access_token(identity=user.username)}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/")
def home():
    return render_template('index.html')

# File upload route
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    extract_archive(file_path, app.config['UPLOAD_FOLDER'])

    db.session.add(UploadedFile(filename=filename, file_path=file_path, file_type=filename.rsplit('.', 1)[1].lower()))
    db.session.commit()

    return jsonify({"message": f"File {filename} uploaded successfully!"}), 200

# Fetch uploaded files with optional filtering
@app.route("/files", methods=["GET"])
@jwt_required()
def get_files():
    query = UploadedFile.query
    for filter_key in ['filename', 'file_type', 'date']:
        filter_value = request.args.get(filter_key)
        if filter_value:
            if filter_key == 'date':
                try:
                    filter_value = datetime.strptime(filter_value, "%Y-%m-%d").date()
                    query = query.filter(func.date(UploadedFile.uploaded_at) == filter_value)
                except ValueError:
                    return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
            else:
                query = query.filter(getattr(UploadedFile, filter_key).ilike(f"%{filter_value}%"))
    return jsonify([{ "id": f.id, "filename": f.filename, "file_path": f.file_path, "uploaded_at": f.uploaded_at.strftime("%Y-%m-%d %H:%M:%S") } for f in query.all()])

# Retrieve logs with filtering options
@app.route("/logs", methods=["GET"])
@jwt_required()
def get_logs_from_files():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    keyword = request.args.get('keyword')

    log_entries = []
    log_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.+)")

    start_dt, end_dt = None, None
    if start_date and end_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    for file in UploadedFile.query.all():
        if file.file_type not in ['txt', 'log']:
            continue

        try:
            with open(file.file_path, "r", encoding="utf-8", errors='ignore') as f:
                for line in f:
                    match = log_pattern.match(line)
                    if match:
                        log_time_str, log_text = match.groups()
                        log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S")
                        if start_dt and end_dt and not (start_dt <= log_time <= end_dt):
                            continue
                        if keyword and keyword.lower() not in log_text.lower():
                            continue
                        log_entries.append({"timestamp": log_time_str, "message": log_text, "filename": file.filename})
                    elif keyword and keyword.lower() in line.lower():
                        log_entries.append({"timestamp": "N/A", "message": line.strip(), "filename": file.filename})
        except Exception as e:
            print(f"Error reading file {file.file_path}: {e}")

    return jsonify(log_entries)

# Initialize database tables
with app.app_context():
    db.create_all()

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
