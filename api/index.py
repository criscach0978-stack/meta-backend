from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Conector Meta-Blackbox v2 Activo"

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
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
                'name': 'Blackbox: ' + data.get('adTitle', 'Test'),
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'PAUSED'
            }
        )
        
        meta_data = response.json()
        
        # Si Meta responde con error, lo enviamos de vuelta para leerlo
        if 'error' in meta_data:
            return jsonify({
                "status": "meta_error",
                "message": meta_data['error']['message'],
                "code": meta_data['error'].get('code'),
                "error_subcode": meta_data['error'].get('error_subcode')
            }), 400

        return jsonify({"status": "success", "id": meta_data.get('id')})
        
    except Exception as e:
        return jsonify({"status": "server_error", "message": str(e)}), 500
