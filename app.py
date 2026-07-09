"""
Demo login module.

Intentionally partial for the pipeline demo against SCRUM-2:
  - Input validation: real format/length checks now added (SCRUM-2 requirement 1)
  - Rate limiting: NOT implemented (missing on purpose)
  - Unit tests: NOT included (missing on purpose)
  - Contains one deliberate vulnerability for Semgrep to catch: SQL query built via
    string formatting (SQL injection), plus a hardcoded secret key
"""

import re

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Deliberate vuln #1: hardcoded secret — Semgrep flags hardcoded credentials/secrets
app.secret_key = "super-secret-key-12345"

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")


def get_db():
    conn = sqlite3.connect("users.db")
    return conn


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Real input validation: presence, length, and character-set checks
    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400
    if not USERNAME_RE.match(username):
        return jsonify({"error": "username must be 3-32 alphanumeric/underscore characters"}), 400
    if len(password) < 8 or len(password) > 128:
        return jsonify({"error": "password must be 8-128 characters"}), 400

    # Deliberate vuln #2: SQL injection via string formatting instead of parameterized query
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "ok", "user": username})
    return jsonify({"error": "invalid credentials"}), 401


# No rate limiting on this route — repeated failed attempts are not throttled.
# No unit tests included in this commit.

if __name__ == "__main__":
    app.run(debug=True)
