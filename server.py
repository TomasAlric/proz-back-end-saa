import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

USAR_BANCO_REAL = all([
    os.getenv("DB_URL"),
    os.getenv("DB_USER"),
    os.getenv("DB_PASS"),
    os.getenv("DB_NAME")
])

if USAR_BANCO_REAL:
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
        f"{os.getenv('DB_URL')}/{os.getenv('DB_NAME')}"
    )
    mensagem_db = "Banco de dados real conectado!"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fake.db"
    mensagem_db = "Usando database fake!"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    curso = db.Column(db.String(50), nullable=False)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Servidor Rodando!", "database": mensagem_db})


@app.route("/cadastro", methods=["POST"])
def cadastrar_aluno():
    data = request.get_json()

    # Extrai os dados do JSON
    nome = data.get("nome")
    email = data.get("email")
    telefone = data.get("telefone")
    cpf = data.get("cpf")
    data_nascimento = data.get("data_nascimento")
    curso = data.get("curso")

    if not all([nome, email, telefone, cpf, data_nascimento, curso]):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    if USAR_BANCO_REAL:
        novo_aluno = Aluno(
            nome=nome, email=email, telefone=telefone,
            cpf=cpf, data_nascimento=data_nascimento, curso=curso
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify({"message": "Aluno cadastrado com sucesso no banco real!", "aluno": data}), 201
    else:
        return jsonify({"message": "Aluno cadastrado no database fake!", "aluno": data}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
