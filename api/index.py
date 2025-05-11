from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key'

app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False
)

CORS(app, supports_credentials=True, origins=[
    "http://localhost:5500",
    "http://127.0.0.1:5500"
])

login_manager = LoginManager()
login_manager.init_app(app)

def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        database='projetizar_db',
        user='postgres',
        password='Boto,4zul'
    )

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
            user = cur.fetchone()
    if user:
        return User(id=user[0], username=user[1])
    return None

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Usuário e senha são obrigatórios!'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
            existente = cur.fetchone()
            if existente:
                return jsonify({'message': 'Usuário já existe!'}), 409

            senha_hash = generate_password_hash(password)
            cur.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', (username, senha_hash))
            conn.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
            user = cur.fetchone()

    if user and check_password_hash(user[2], password):
        user_obj = User(id=user[0], username=user[1])
        login_user(user_obj)
        return jsonify({'message': 'Login bem-sucedido!', 'usuario_id': user[0], 'username': user[1]})
    else:
        return jsonify({'message': 'Credenciais inválidas!'}), 401

# ✅ REMOVIDO login_required
@app.route('/salvar_objetivo', methods=['POST'])
def salvar_objetivo():
    data = request.json
    usuario_id = data.get('usuario_id')  # Agora vem do frontend
    como = data.get('como', '')
    quando = data.get('quando', '')
    resultados = data.get('resultados', '')
    ajudas = data.get('ajudas', '')

    if not usuario_id:
        return jsonify({'message': 'ID do usuário é obrigatório!'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO objetivos (usuario_id, como, quando, resultados, ajudas)
                VALUES (%s, %s, %s, %s, %s)
            ''', (usuario_id, como, quando, resultados, ajudas))
            conn.commit()

    return jsonify({'mensagem': 'Objetivo salvo com sucesso!'})

# ✅ REMOVIDO login_required
@app.route('/listar_objetivos', methods=['GET'])
def listar_objetivos():
    usuario_id = request.args.get('usuario_id')
    if not usuario_id:
        return jsonify({'message': 'ID do usuário é obrigatório!'}), 400

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('SELECT * FROM objetivos WHERE usuario_id = %s', (usuario_id,))
            objetivos = cur.fetchall()

    return jsonify([dict(obj) for obj in objetivos])

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Logout bem-sucedido!'})

@app.route('/deletar_usuario', methods=['POST'])
def deletar_usuario():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'message': 'Usuário é obrigatório!'}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
            user = cur.fetchone()

            if not user:
                return jsonify({'message': 'Usuário não encontrado!'}), 404

            cur.execute('DELETE FROM usuarios WHERE username = %s', (username,))
            conn.commit()

    return jsonify({'message': 'Usuário deletado com sucesso!'})

@app.route('/usuario_logado', methods=['GET'])
def usuario_logado():
    if current_user.is_authenticated:
        return jsonify({'username': current_user.username})
    else:
        return jsonify({'username': None}), 401

app = app  # Assim o Vercel entende que esse é o app Flask

