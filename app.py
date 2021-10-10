import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort

# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')   # Abre uma conexão do banco de dados
    conn.row_factory = sqlite3.Row          # Define o atributo row_factory ao sqlite3.Row para que tenha acesso baseado em nome às colunas
    return conn                             # retorna o objeto de conexão conn que utilizará para acesar o banco de dados

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()              # Abre a conexão ao banco de dados
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()                            # Fecha a conexão 
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

