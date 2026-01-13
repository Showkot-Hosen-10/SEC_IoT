from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------- Database ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # your MySQL root password
    database="iot_dashboard"
)
cursor = db.cursor(dictionary=True)

# ---------- Flask-Login ----------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------- User Class ----------
class User(UserMixin):
    def __init__(self, id, username, is_admin):
        self.id = id
        self.username = username
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user['id'], user['username'], user['is_admin'])
    return None

# ---------- Routes ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'], user['is_admin'])
            login_user(user_obj)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", current_user=current_user)

@app.route("/")
@login_required
def dashboard():
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 50")
    data = cursor.fetchall()
    return render_template("dashboard.html", data=data, current_user=current_user)

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        is_admin = True if request.form.get("is_admin") else False
        hashed = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s,%s,%s)", 
                           (username, hashed, is_admin))
            db.commit()
            flash("User created successfully!", "success")
        except:
            flash("User creation failed (maybe username exists)", "danger")

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 50")
    data = cursor.fetchall()
    return render_template("admin.html", users=users, data=data)

@app.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard"))
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    flash("User deleted!", "success")
    return redirect(url_for("admin_panel"))

# API for ESP32 to send sensor data
@app.route("/api/add_data", methods=["POST"])
def add_data():
    data = request.get_json()
    ultrasonic = data.get("ultrasonic")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    mq135 = data.get("mq135")
    current_mA = data.get("current_mA")

    sql = """INSERT INTO sensor_data (ultrasonic, temperature, humidity, mq135, current_mA)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (ultrasonic, temperature, humidity, mq135, current_mA))
    db.commit()

    return jsonify({"status": "success"}), 200

# Run Flask server accessible to ESP32
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
