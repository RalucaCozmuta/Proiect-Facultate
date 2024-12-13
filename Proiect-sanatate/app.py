from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Configurarea aplicației
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret pentru sesiuni
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Configurare bază de date
db = SQLAlchemy(app)

# Model pentru utilizatoriclass User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Funcție pentru înregistrarea utilizatorilor
def register_user(username, password):
    if User.query.filter_by(username=username).first():
        return False  # Utilizatorul există deja
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return True

# Funcție pentru autentificare
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

# Ruta principală - redirecționează la login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta pentru înregistrare
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            flash('Cont creat cu succes!')
            return redirect(url_for('login'))
        else:
            flash('Utilizatorul există deja!')
    return render_template('register.html')

# Ruta pentru autentificare
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['user_id'] = username
            flash('Autentificare reușită!')
            return redirect(url_for('dashboard'))
        flash('Autentificare eșuată!')
    return render_template('login.html')

# Ruta pentru dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Trebuie să te autentifici.')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Ruta pentru delogare
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Delogare reușită.')
    return redirect(url_for('login'))

# Creează baza de date la prima rulare
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
