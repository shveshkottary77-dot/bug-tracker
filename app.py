from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_premium_key_for_bug_tracker"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugtracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# Database Models
# ─────────────────────────────────────────────

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # Using string referencing for foreign keys to avoid order definition issues
    reported_bugs = db.relationship('Bug', foreign_keys='Bug.reporter_id', backref='reporter', lazy=True)
    assigned_bugs = db.relationship('Bug', foreign_keys='Bug.assignee_id', backref='assignee', lazy=True)

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='Medium') # Low, Medium, High, Critical
    status = db.Column(db.String(20), default='Open') # Open, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# ─────────────────────────────────────────────
# Auth Decorator
# ─────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access the dashboard.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        if not username or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('register'))
            
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please sign in.", "success")
        return redirect(url_for('login'))
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Successfully logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try again or register a new account.", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        assignee_id = request.form.get("assignee_id")
        
        if not title:
            flash("Bug title is required.", "error")
            return redirect(url_for('home'))
            
        try:
            assignee_id = int(assignee_id) if assignee_id else None
        except ValueError:
            assignee_id = None
            
        new_bug = Bug(
            title=title,
            description=description,
            priority=priority,
            status="Open",
            reporter_id=session['user_id'],
            assignee_id=assignee_id
        )
        db.session.add(new_bug)
        db.session.commit()
        flash("Bug reported successfully!", "success")
        return redirect(url_for('home'))
        
    # GET: query with filtering and search
    search_query = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()
    priority_filter = request.args.get("priority", "").strip()
    
    query = Bug.query
    
    if search_query:
        query = query.filter(
            (Bug.title.ilike(f"%{search_query}%")) | 
            (Bug.description.ilike(f"%{search_query}%"))
        )
    if status_filter:
        query = query.filter(Bug.status == status_filter)
    if priority_filter:
        query = query.filter(Bug.priority == priority_filter)
        
    bugs_list = query.order_by(Bug.created_at.desc()).all()
    
    # Statistics counts
    total_bugs = Bug.query.count()
    open_bugs = Bug.query.filter_by(status="Open").count()
    resolved_bugs = total_bugs - open_bugs
    
    # Active team members list for assignment dropdown
    users = User.query.order_by(User.username.asc()).all()
    
    return render_template(
        "index.html", 
        bugs=bugs_list, 
        total_bugs=total_bugs, 
        open_bugs=open_bugs, 
        resolved_bugs=resolved_bugs,
        users=users,
        search=search_query,
        current_status=status_filter,
        current_priority=priority_filter
    )

@app.route("/delete/<int:bug_id>")
@login_required
def delete(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    db.session.delete(bug)
    db.session.commit()
    flash(f"Bug '{bug.title}' successfully deleted.", "success")
    return redirect(url_for('home'))

@app.route("/resolve/<int:bug_id>")
@login_required
def resolve(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    bug.status = "Resolved"
    db.session.commit()
    flash(f"Bug '{bug.title}' marked as resolved!", "success")
    return redirect(url_for('home'))

# ─────────────────────────────────────────────
# Database Initializer & Server Run
# ─────────────────────────────────────────────

with app.app_context():
    db.create_all()
    # Seed default user if database has no users
    if User.query.count() == 0:
        hashed_pw = generate_password_hash("password")
        demo_user = User(username="admin", password_hash=hashed_pw)
        db.session.add(demo_user)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)