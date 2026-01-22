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
        page = data.get('pageId')
        
        # 1. Crear Campaña
        c = requests.post(f"https://graph.facebook.com/v18.0/{acc}/campaigns", 
            params={'access_token': token, 'name': 'Blackbox: ' + data.get('adTitle'), 'objective': 'OUTCOME_TRAFFIC', 'status': 'PAUSED'}).json()
        
        # 2. CREAR CONJUNTO DE ANUNCIOS (AdSet) - Esto es lo que faltaba para que sea visible
        as_res = requests.post(f"https://graph.facebook.com/v18.0/{acc}/adsets",
            params={
                'access_token': token,
                'name': 'AdSet Blackbox',
                'campaign_id': c['id'],
                'daily_budget': 1000, # 10 USD aprox (en centavos según moneda)
                'billing_event': 'IMPRESSIONS',
                'optimization_goal': 'REACH',
                'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
                'targeting': {'geo_locations': {'countries': ['CO']}, 'publisher_platforms': ['facebook', 'instagram']},
                'status': 'PAUSED'
            }).json()

        # 3. Crear Anuncio Final
        requests.post(f"https://graph.facebook.com/v18.0/{acc}/ads",
            params={
                'access_token': token,
                'name': 'Anuncio Final IA',
                'adset_id': as_res['id'],
                'creative': {'image_url': data.get('imageUrl'), 'body': data.get('adBody'), 'title': data.get('adTitle')},
                'status': 'PAUSED'
            })

        return jsonify({"status": "success", "campaign_id": c['id']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
