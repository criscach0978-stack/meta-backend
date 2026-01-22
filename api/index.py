import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
    if request.method == 'OPTIONS': return '', 200
    try:
        data = request.get_json()
        token = data.get('accessToken')
        acc = data.get('adAccountId')
        
        # Petición a Meta
        res = requests.post(f"https://graph.facebook.com/v18.0/{acc}/campaigns", 
            params={
                'access_token': token, 
                'name': 'Blackbox: ' + data.get('adTitle', 'Test'), 
                'objective': 'OUTCOME_TRAFFIC', 
                'status': 'PAUSED'
            })
        
        meta_data = res.json()
        
        # SI HAY ERROR, LO MOSTRAMOS TODO
        if 'error' in meta_data:
            print(f"❌ DETALLE DEL ERROR DE META: {meta_data['error']}")
            return jsonify({
                "status": "meta_error",
                "message": meta_data['error']['message'],
                "full_error": meta_data['error']
            }), 400

        return jsonify({"status": "success", "id": meta_data.get('id')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
