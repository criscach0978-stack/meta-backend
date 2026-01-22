from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Motor de Diagnóstico Blackbox Activo"

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
    # Manejo de pre-vuelo para evitar errores de CORS
    if request.method == 'OPTIONS': 
        return '', 200
    
    try:
        data = request.get_json()
        token = data.get('accessToken')
        acc_id = data.get('adAccountId')
        
        # Intentar crear la campaña en Meta
        response = requests.post(
            f"https://graph.facebook.com/v18.0/{acc_id}/campaigns",
            params={
                'access_token': token,
                'name': 'Blackbox Test: ' + data.get('adTitle', 'Anuncio'),
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'PAUSED'
            }
        )
        
        meta_data = response.json()
        
        # ✅ SI HAY ERROR, ESTO LO IMPRIMIRÁ EN LA COLUMNA "MESSAGES" DE VERCEL
        if 'error' in meta_data:
            error_msg = meta_data['error'].get('message', 'Error desconocido')
            print(f"!!! ERROR DE META DETECTADO: {error_msg}")
            return jsonify({
                "status": "meta_error",
                "message": error_msg
            }), 400

        # Si todo sale bien
        print(f"✅ Campaña creada con ID: {meta_data.get('id')}")
        return jsonify({"status": "success", "id": meta_data.get('id')})
        
    except Exception as e:
        print(f"❌ ERROR INTERNO DEL SERVIDOR: {str(e)}")
        return jsonify({"status": "server_error", "message": str(e)}), 500
