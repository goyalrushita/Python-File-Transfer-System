
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    render_template_string,
    flash
)
from werkzeug.utils import secure_filename
from pathlib import Path
from functools import wraps

app = Flask(__name__)

# Demo secret: change this before any deployment
app.secret_key = "change-this-demo-secret"

# Project folders
BASE_DIR = Path(__file__).resolve().parent
SERVER_FOLDER = BASE_DIR / "server_files"
SERVER_FOLDER.mkdir(parents=True, exist_ok=True)

# Demo credentials
USERNAME = "admin"
PASSWORD = "1234"


# -------------------- HTML AND CSS --------------------

PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>File Transfer Dashboard</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f1f5fb;
            color: #1e293b;
        }

        .header {
            background: #173b70;
            color: white;
            padding: 24px 20px;
        }

        .header-inner {
            max-width: 1000px;
            margin: auto;
        }

        .header h1 {
            margin: 0 0 8px;
            font-size: 30px;
        }

        .header p {
            margin: 0;
            color: #dbeafe;
        }

        .container {
            max-width: 1000px;
            margin: 28px auto;
            padding: 0 20px;
        }

        .welcome {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 22px;
        }

        .welcome h2 {
            margin: 0 0 6px;
        }

        .muted {
            color: #64748b;
            margin: 0;
            line-height: 1.5;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1.4fr;
            gap: 22px;
            align-items: start;
        }

        .card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
            min-width: 0;
        }

        .card h2,
        .card h3 {
            margin-top: 0;
            margin-bottom: 16px;
        }

        input[type="text"],
        input[type="password"],
        input[type="file"] {
            display: block;
            width: 100%;
            margin: 12px 0 18px;
        }

        input[type="text"],
        input[type="password"] {
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
        }

        input[type="file"] {
            padding: 12px;
            border: 1px dashed #94a3b8;
            border-radius: 8px;
            background: #f8fafc;
        }

        button,
        .btn {
            display: inline-block;
            border: none;
            border-radius: 8px;
            padding: 11px 16px;
            background: #245caa;
            color: white;
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
            cursor: pointer;
            text-align: center;
        }

        button:hover,
        .btn:hover {
            background: #173b70;
        }

        .logout {
            background: #475569;
        }

        .messages {
            margin-bottom: 18px;
        }

        .message {
            padding: 12px 15px;
            border-radius: 8px;
            background: #dcfce7;
            color: #166534;
            overflow-wrap: anywhere;
        }

        .file-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 14px 0;
            border-bottom: 1px solid #e2e8f0;
        }

        .file-row:last-child {
            border-bottom: none;
        }

        .file-info {
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 0;
        }

        .file-icon {
            font-size: 25px;
            flex-shrink: 0;
        }

        .file-name {
            font-weight: bold;
            overflow-wrap: anywhere;
        }

        .file-size {
            font-size: 13px;
            color: #64748b;
            margin-top: 5px;
        }

        .empty {
            color: #64748b;
            background: #f8fafc;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
        }

        .login-card {
            max-width: 440px;
            margin: 45px auto;
        }

        @media (max-width: 700px) {
            .grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 25px;
            }

            .container {
                margin-top: 20px;
                padding: 0 14px;
            }

            .card {
                padding: 18px;
            }

            .file-row {
                align-items: flex-start;
            }

            .btn {
                padding: 10px;
                flex-shrink: 0;
            }
        }

        @media (max-width: 380px) {
            .file-row {
                flex-direction: column;
            }
        }
    </style>
</head>

<body>
    <header class="header">
        <div class="header-inner">
            <h1>File Transfer System</h1>
            <p>Python-based file upload and download dashboard</p>
        </div>
    </header>

    <main class="container">

        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <div class="messages">
            {% for message in messages %}
            <div class="message">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        {% endwith %}

        {% if not logged_in %}

        <section class="card login-card">
            <h2>Welcome back</h2>
            <p class="muted">Login to manage your files.</p>

            <form method="post" action="{{ url_for('login') }}">
                <label for="username">Username</label>
                <input
                    id="username"
                    name="username"
                    type="text"
                    required
                >

                <label for="password">Password</label>
                <input
                    id="password"
                    name="password"
                    type="password"
                    required
                >

                <button type="submit">Login</button>
            </form>
        </section>

        {% else %}

        <div class="welcome">
            <div>
                <h2>Welcome, {{ username }}!</h2>
                <p class="muted">
                    Manage your uploaded and stored files.
                </p>
            </div>

            <form method="post" action="{{ url_for('logout') }}">
                <button class="logout" type="submit">Logout</button>
            </form>
        </div>

        <div class="grid">

            <section class="card">
                <h3>Upload a file</h3>
                <p class="muted">
                    Choose a file from your computer.
                </p>

                <form
                    method="post"
                    action="{{ url_for('upload') }}"
                    enctype="multipart/form-data"
                >
                    <input type="file" name="file" required>
                    <button type="submit">Upload File</button>
                </form>
            </section>

            <section class="card">
                <h3>Files on server</h3>
                <p class="muted">
                    Available files are listed below.
                </p>

                {% if files %}
                    {% for file in files %}
                    <div class="file-row">
                        <div class="file-info">
                            <span class="file-icon">&#128196;</span>
                            <div>
                                <div class="file-name">
                                    {{ file.name }}
                                </div>
                                <div class="file-size">
                                    {{ file.size }} bytes
                                </div>
                            </div>
                        </div>

                        <a
                            class="btn"
                            href="{{ url_for(
                                'download',
                                filename=file.name
                            ) }}"
                        >Download</a>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="empty">
                        No files yet. Upload a file to get started.
                    </div>
                {% endif %}
            </section>

        </div>

        {% endif %}
    </main>
</body>
</html>
"""


# -------------------- LOGIN PROTECTION --------------------

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("home"))

        return function(*args, **kwargs)

    return wrapper


# -------------------- HOME / DASHBOARD --------------------

@app.route("/")
def home():
    files = []

    if session.get("username"):
        for path in SERVER_FOLDER.iterdir():
            # Hide .gitkeep and other hidden files
            if path.is_file() and not path.name.startswith("."):
                files.append({
                    "name": path.name,
                    "size": path.stat().st_size
                })

        files.sort(key=lambda item: item["name"].lower())

    return render_template_string(
        PAGE,
        logged_in=bool(session.get("username")),
        username=session.get("username"),
        files=files
    )


# -------------------- LOGIN --------------------

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username == USERNAME and password == PASSWORD:
        session.clear()
        session["username"] = username
        flash("Login successful!")
    else:
        flash("Incorrect username or password.")

    return redirect(url_for("home"))


# -------------------- UPLOAD FILE --------------------

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    uploaded = request.files.get("file")

    if not uploaded or not uploaded.filename:
        flash("Please choose a file.")
        return redirect(url_for("home"))

    filename = secure_filename(uploaded.filename)

    if not filename:
        flash("Invalid filename.")
        return redirect(url_for("home"))

    destination = SERVER_FOLDER / filename

    uploaded.save(str(destination))

    flash("File uploaded successfully!")
    return redirect(url_for("home"))


# -------------------- DOWNLOAD FILE --------------------

@app.route("/download/<filename>")
@login_required
def download(filename):
    safe_name = secure_filename(filename)

    if not safe_name or safe_name != filename:
        return "Invalid filename", 400

    path = SERVER_FOLDER / safe_name

    if not path.is_file():
        return "File not found", 404

    return send_from_directory(
        str(SERVER_FOLDER),
        safe_name,
        as_attachment=True
    )


# -------------------- LOGOUT --------------------

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("You have logged out.")

    return redirect(url_for("home"))


# -------------------- RUN APPLICATION --------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )
