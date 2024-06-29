from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import requests

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client.marjosports_db 
users_collection = db.users  
transactions_collection = db.transactions 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    cpf = data.get('cpf')
    if users_collection.find_one({"cpf": cpf}):
        return jsonify({"message": "CPF já registrado."}), 400
    users_collection.insert_one(data)
    return jsonify({"message": "Usuário registrado com sucesso."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cpf = data.get('cpf')
    user = users_collection.find_one({"cpf": cpf})
    if not user:
        return jsonify({"message": "CPF não encontrado."}), 404
    if user['password'] != data.get('password'):
        return jsonify({"message": "Senha incorreta."}), 403
    return jsonify({"message": "Login bem-sucedido."}), 200


@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    cpf = data.get('cpf')
    if not users_collection.find_one({"cpf": cpf}):
        return jsonify({"message": "CPF não encontrado."}), 404

    transaction = {
        "cpf": cpf,
        "app_name": data.get('app_name'),
        "valor": data.get('valor')
    }

    result = transactions_collection.insert_one(transaction)

    transaction["_id"] = str(result.inserted_id)

    response = requests.post(
        'https://hackathon.marjosports.com.br/hackathon',
        headers={"api-key": "HACKATON_UNIESP_MARJO_2024", "Content-Type": "application/json"},
        json=transaction
    )
    
    if response.status_code == 200 or response.status_code == 201:
        return jsonify({"message": "Transação adicionada com sucesso."}), 201
    else:
        return jsonify({"message": "Erro ao adicionar transação no endpoint externo."}), response.status_code

    
@app.route('/transactions/<cpf>', methods=['GET'])
def get_transactions(cpf):
    if not users_collection.find_one({"cpf": cpf}):
        return jsonify({"message": "CPF não encontrado."}), 404
    response = requests.get(f'https://hackathon.marjosports.com.br/hackathon?cpf={cpf}', 
                            headers={"api-key": "HACKATON_UNIESP_MARJO_2024"})
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({"message": "Erro ao buscar transações."}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
