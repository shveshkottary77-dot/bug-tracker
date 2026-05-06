from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps

app = Flask(__name__)
app.secret_key = "super_secret_premium_key_for_bug_tracker"

bugs = []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Please log in to access the dashboard.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username == "admin" and password == "password":
            session['logged_in'] = True
            session['username'] = username
            flash("Successfully logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try admin / password.", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        bug = request.form.get("bug")
        if bug:
            bugs.append({"name": bug, "status": "Open"})
        return redirect(url_for('home'))
        
    total_bugs = len(bugs)
    open_bugs = sum(1 for b in bugs if b['status'] == 'Open')
    resolved_bugs = total_bugs - open_bugs
    
    return render_template("index.html", 
                           bugs=bugs, 
                           total_bugs=total_bugs, 
                           open_bugs=open_bugs, 
                           resolved_bugs=resolved_bugs)

@app.route("/delete/<int:index>")
@login_required
def delete(index):
    if 0 <= index < len(bugs):
        bugs.pop(index)
    return redirect(url_for('home'))

@app.route("/resolve/<int:index>")
@login_required
def resolve(index):
    if 0 <= index < len(bugs):
        bugs[index]["status"] = "Resolved"
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)