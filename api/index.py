from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Motor de Publicación Blackbox Activo"

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
    if request.method == 'OPTIONS': return '', 200
    try:
        data = request.get_json()
        token = data.get('accessToken')
        acc = data.get('adAccountId')
        
        # 1. Crear Campaña (Nivel 1)
        # Usamos requests directamente para evitar errores de librerías pesadas
        c_url = f"https://graph.facebook.com/v18.0/{acc}/campaigns"
        c_params = {
            'access_token': token,
            'name': 'Blackbox: ' + data.get('adTitle', 'Anuncio'),
            'objective': 'OUTCOME_TRAFFIC',
            'status': 'PAUSED'
        }
        c_res = requests.post(c_url, params=c_params).json()
        
        if 'error' in c_res:
            return jsonify({"error": c_res['error']['message']}), 400

        return jsonify({"status": "success", "campaign_id": c_res.get('id')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
