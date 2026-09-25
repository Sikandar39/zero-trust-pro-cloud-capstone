import os

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "development-secret-key")


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    return psycopg2.connect(database_url)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/leadership")
def leadership():
    return render_template("leadership.html")


@app.route("/domains")
def domains():
    return render_template("domains.html")


@app.route("/programs")
def programs():
    return render_template("programs.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if name and email and message:

            connection = get_db_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO contact_messages
                (name, email, message)
                VALUES (%s, %s, %s)
                """,
                (name, email, message)
            )

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user[2], password):

            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


@app.route("/health")
def health():

    database_status = "offline"

    try:

        connection = get_db_connection()
        connection.close()

        database_status = "online"

    except Exception:
        database_status = "offline"

    return jsonify({
        "application": "online",
        "database": database_status,
        "service": "Zero Trust Pro Platform"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )