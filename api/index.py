from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

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
        
        if 'error' in meta_data:
            # ✅ ESTO FORZARÁ EL ERROR EN LOS LOGS QUE ME ENVIASTE
            print(f"--- ERROR DE META DETECTADO ---")
            print(json.dumps(meta_data['error'], indent=2)) 
            return jsonify({"status": "meta_error", "message": meta_data['error']['message']}), 400

        return jsonify({"status": "success", "id": meta_data.get('id')})
    except Exception as e:
        print(f"❌ Error interno: {str(e)}")
        return jsonify({"error": str(e)}), 500
