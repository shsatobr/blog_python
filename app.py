import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
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
app.config['SECRET_KEY'] = 'y7rduqpXL8fVKln'

@app.route('/')
def index():
    conn = get_db_connection()              # Abre a conexão ao banco de dados
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()                            # Fecha a conexão 
    return render_template('index.html', posts=posts)

# Função para mostrar as páginas
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

# Função para inclusão de dados
@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Titulo e requerido')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) values (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

# Função para alteração de dados
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Titulo é necessário')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? where id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)

# Função para exclusão de dados
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excuido com sucesso!'.format(post['title']))
    return redirect(url_for('index'))


