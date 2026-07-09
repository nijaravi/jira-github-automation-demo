"""
Demo login module.

Intentionally partial for the pipeline demo against SCRUM-2:
  - Input validation: only checks that fields are non-empty (partial, not real validation)
  - Rate limiting: NOT implemented (missing on purpose)
  - Unit tests: NOT included (missing on purpose)
  - Contains one deliberate vulnerability for Semgrep to catch: SQL query built via
    string formatting (SQL injection), plus a hardcoded secret key
"""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Deliberate vuln #1: hardcoded secret — Semgrep flags hardcoded credentials/secrets
app.secret_key = "super-secret-key-12345"


def get_db():
    conn = sqlite3.connect("users.db")
    return conn


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Partial input validation — only checks presence, not format/length/injection chars
    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

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
