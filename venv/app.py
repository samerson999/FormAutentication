from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import html
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'  

# ---------- Banco de Dados ----------
def init_db():
    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')
    print("Banco de dados inicializado.")


@app.route('/')
def home():
    if 'usuario' in session:
        return f"<h3>Bem-vindo, {session['usuario']}!</h3><a href='/logout'>Sair</a>"
    return redirect(url_for('login'))

# ---------- Registro ----------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = html.escape(request.form['nome'].strip())
        email = html.escape(request.form['email'].strip())
        senha = request.form['senha']

        # Validações
        if len(nome) < 3:
            flash("Nome deve ter pelo menos 3 caracteres.", "danger")
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash("E-mail inválido.", "danger")
        elif not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha):
            flash("Senha deve conter ao menos 8 caracteres, incluindo uma letra maiúscula e um número.", "danger")
        else:
            senha_hash = generate_password_hash(senha)
            try:
                with sqlite3.connect('usuarios.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                                   (nome, email, senha_hash))
                    conn.commit()
                flash("Usuário registrado com sucesso!", "success")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("E-mail já registrado.", "danger")

    return render_template('registro.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = html.escape(request.form['email'].strip())
        senha = request.form['senha']

        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome, senha FROM usuarios WHERE email = ?", (email,))
            resultado = cursor.fetchone()

            if resultado and check_password_hash(resultado[1], senha):
                session['usuario'] = resultado[0]
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for('home'))
            else:
                flash("E-mail ou senha incorretos.", "danger")

    return render_template('login.html')

# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da sessão.", "info")
    return redirect(url_for('login'))

# ---------- App ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
