import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Motor de Publicación Real Blackbox Activo"

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
    if request.method == 'OPTIONS': 
        return '', 200
    
    try:
        data = request.get_json()
        # Extraemos los datos que envía tu App
        token = data.get('accessToken')
        ad_account_id = data.get('adAccountId')
        page_id = data.get('pageId')
        image_url = data.get('imageUrl')
        ad_title = data.get('adTitle', 'Anuncio Blackbox')
        ad_body = data.get('adBody', 'Generado con IA')

        # 1. Subir la Imagen a Meta para obtener el Hash
        img_res = requests.post(
            f"https://graph.facebook.com/v18.0/{ad_account_id}/advideos" if ".mp4" in image_url else f"https://graph.facebook.com/v18.0/{ad_account_id}/adimages",
            params={'access_token': token, 'url': image_url}
        )
        img_hash = img_res.json().get('images', {}).get('bytes', {}).get('hash') or img_res.json().get('hash')

        # 2. Crear la Campaña
        campaign_res = requests.post(
            f"https://graph.facebook.com/v18.0/{ad_account_id}/campaigns",
            params={
                'access_token': token,
                'name': f"Blackbox: {ad_title}",
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'PAUSED' # La creamos pausada para que tú la revises primero
            }
        ).json()
        campaign_id = campaign_res.get('id')

        # 3. Crear el Anuncio (Ad Creative)
        creative_res = requests.post(
            f"https://graph.facebook.com/v18.0/{ad_account_id}/adcreatives",
            params={
                'access_token': token,
                'name': f"Creative {ad_title}",
                'object_story_spec': {
                    'page_id': page_id,
                    'link_data': {
                        'image_hash': img_hash,
                        'message': ad_body,
                        'link': 'https://facebook.com/' + page_id,
                        'call_to_action': {'type': 'LEARN_MORE'}
                    }
                }
            }
        ).json()

        return jsonify({
            "status": "success", 
            "message": "Campaña creada en Meta",
            "campaign_id": campaign_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
