from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Configuração do banco de dados SQLite (local)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# Configuração do banco de dados PostgreSQL (real)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:senha_forte@localhost:5432/proz"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)  # Permite requisições do front-end

# Modelo Aluno
class Aluno(db.Model):
    __tablename__ = "aluno"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    curso = db.Column(db.String(50), nullable=False)

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Função para identificar o banco de dados
def verificar_banco():
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        return "fake"  # SQLite (fake database)
    elif "postgresql" in app.config["SQLALCHEMY_DATABASE_URI"]:
        return "real"  # PostgreSQL (real database)
    return "unknown"  # Caso não seja SQLite ou PostgreSQL

# Rota para cadastrar um aluno
@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    data = request.get_json()

    novo_aluno = Aluno(
        nome=data["nome"],
        email=data["email"],
        telefone=data["telefone"],
        cpf=data["cpf"],
        data_nascimento=data["data_nascimento"],
        curso=data["curso"]
    )

    db.session.add(novo_aluno)
    db.session.commit()

    # Verifica o tipo de banco de dados e ajusta a resposta
    banco_tipo = verificar_banco()
    if banco_tipo == "fake":
        return jsonify({"mensagem": "Aluno cadastrado com sucesso no banco FAKE!"}), 201
    elif banco_tipo == "real":
        return jsonify({"mensagem": "Aluno cadastrado com sucesso no banco REAL!"}), 201
    else:
        return jsonify({"mensagem": "Erro ao identificar o banco de dados!"}), 500

# Rota para listar alunos
@app.route("/alunos", methods=["GET"])
def listar_alunos():
    alunos = Aluno.query.all()
    lista_alunos = [
        {
            "id": aluno.id,
            "nome": aluno.nome,
            "email": aluno.email,
            "telefone": aluno.telefone,
            "cpf": aluno.cpf,
            "data_nascimento": aluno.data_nascimento,
            "curso": aluno.curso,
        }
        for aluno in alunos
    ]
    return jsonify(lista_alunos)

# Rota para editar um aluno pelo ID
@app.route("/alunos/<int:aluno_id>", methods=["PUT"])
def editar_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)

    if not aluno:
        return jsonify({"mensagem": "Aluno não encontrado"}), 404

    data = request.get_json()
    aluno.nome = data.get("nome", aluno.nome)
    aluno.email = data.get("email", aluno.email)
    aluno.telefone = data.get("telefone", aluno.telefone)
    aluno.cpf = data.get("cpf", aluno.cpf)
    aluno.data_nascimento = data.get("data_nascimento", aluno.data_nascimento)
    aluno.curso = data.get("curso", aluno.curso)

    db.session.commit()

    return jsonify({"mensagem": "Aluno atualizado com sucesso!"})

# Rota para deletar um aluno pelo ID
@app.route("/alunos/<int:aluno_id>", methods=["DELETE"])
def deletar_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)

    if not aluno:
        return jsonify({"mensagem": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno deletado com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)
