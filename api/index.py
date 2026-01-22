import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Conector Blackbox Real-Time Activo"

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
    if request.method == 'OPTIONS': return '', 200
    try:
        data = request.get_json()
        token = data.get('accessToken')
        acc = data.get('adAccountId') # Asegúrate que sea 'act_...'
        page = data.get('pageId')
        
        # 1. Crear Campaña
        c_res = requests.post(f"https://graph.facebook.com/v18.0/{acc}/campaigns", 
            params={'access_token': token, 'name': 'Blackbox: ' + data.get('adTitle', 'Venta'), 'objective': 'OUTCOME_TRAFFIC', 'status': 'PAUSED'}).json()
        
        if 'error' in c_res: return jsonify({"status": "meta_error", "message": c_res['error']['message']}), 400
        c_id = c_res['id']

        # 2. Crear Conjunto (AdSet) - OBLIGATORIO para visibilidad
        as_res = requests.post(f"https://graph.facebook.com/v18.0/{acc}/adsets",
            params={
                'access_token': token,
                'name': 'Conjunto Blackbox',
                'campaign_id': c_id,
                'daily_budget': 5000, # 5 USD aprox
                'billing_event': 'IMPRESSIONS',
                'optimization_goal': 'REACH',
                'targeting': {'geo_locations': {'countries': ['CO']}, 'publisher_platforms': ['facebook', 'instagram']},
                'status': 'PAUSED'
            }).json()

        return jsonify({"status": "success", "campaign_id": c_id, "message": "¡Ya debería ser visible en Facebook!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
