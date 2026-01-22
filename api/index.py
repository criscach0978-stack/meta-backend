import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
    if request.method == 'OPTIONS': 
        return '', 200
    
    img_data = None 
    try:
        data = request.get_json()
        image_url = data.get('imageUrl')
        token = data.get('accessToken')
        
        if image_url and image_url != "None":
            print(f"📥 Descargando imagen...")
            res = requests.get(image_url, timeout=10)
            img_data = res.content
        
        if not img_data:
            return jsonify({"error": "No hay imagen disponible"}), 400

        print("✅ Petición procesada correctamente")
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Vercel usará la variable 'app' directamente

