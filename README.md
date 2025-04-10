# 🔐 Sistema de Registro e Login com Flask

Aplicação web simples de autenticação de usuários usando **Flask**, **SQLite** e **Bootstrap**.  
Inclui validação de dados, hash de senha e controle de sessão.

---

## 🚀 Funcionalidades

- Registro de usuário com validações:
- Nome: mínimo de 3 caracteres
- E-mail válido
- Senha: mínimo de 8 caracteres, 1 número e 1 letra maiúscula
- Login com autenticação segura
- Hash de senha com Werkzeug
- Interface responsiva com Bootstrap
- Banco de dados local (SQLite)

---

## 🛠 Tecnologias

- Python 3
- Flask
- SQLite
- Bootstrap 5

---

## ▶️ Como rodar o projeto

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/login-flask.git
cd login-flask

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install flask werkzeug

# Execute o app
python app.py

Acesse: http://localhost:5000
