from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os

load_dotenv() # carrega as variáveis do arquivo .env

app = Flask(__name__)

def calcular_numero_de_vida(data_nascimento):
    # remove caracteres não numéricos e verifica se a entrada é válida
    data_nascimento = data_nascimento.replace('-', '').replace('/', '')
    if not data_nascimento.isdigit() or len(data_nascimento) not in [8, 6]:
        raise ValueError("Data de nascimento inválida. Use o formato DD/MM/AAAA.")
    
    # soma os dígitos da data de nascimento
    soma = sum(int(digito) for digito in data_nascimento)
    
    # reduz a soma a um único dígito ou a um número mestre
    while soma > 9 and soma not in [11, 22, 33]:
        soma = sum(int(digito) for digito in str(soma))
    
    return soma

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data_nascimento = request.form.get('data_nascimento')
        try:
            numero_de_vida = calcular_numero_de_vida(data_nascimento)
            return render_template('index.html', numero_de_vida=numero_de_vida)
        except ValueError as ve:
            return render_template('index.html', error=str(ve))
    return render_template('index.html')

@app.route('/api/numero_de_vida', methods=['POST'])
def api_numero_de_vida():
    data = request.json
    data_nascimento = data.get('data_nascimento', '')
    try:
        numero_de_vida = calcular_numero_de_vida(data_nascimento)
        return jsonify({"numero_de_vida": numero_de_vida})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

if __name__ == '__main__':
    app.run(debug=True)
