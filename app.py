from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'juanss'
app.config['MYSQL_PASSWORD'] = 'contra'
app.config['MYSQL_DB'] = 'base_db'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

mysql = MySQL(app)
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", (username, password, False))
            mysql.connection.commit()
            flash('Registro exitoso! Puedes iniciar sesión ahora.')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al registrar el usuario. Asegúrate de que el nombre de usuario no esté en uso.')
        finally:
            cursor.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            if check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['is_admin'] = user[3]
                return redirect(url_for('protected') if user[3] else url_for('home'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('Usuario no encontrado')
        cursor.close()
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/protected')
def protected():
    if 'user_id' in session and session.get('is_admin'):
        return render_template('admin_dashboard.html')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
