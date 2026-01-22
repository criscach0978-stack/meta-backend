import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta principal para verificar que el servidor vive
@app.route('/')
def home():
    return "✅ El servidor de Blackbox está activo y funcionando."

@app.route('/launch-campaign', methods=['POST', 'OPTIONS'])
def launch():
    if request.method == 'OPTIONS': 
        return '', 200
    
    img_data = None 
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        image_url = data.get('imageUrl')
        token = data.get('accessToken')
        
        if image_url and image_url != "None":
            res = requests.get(image_url, timeout=10)
            img_data = res.content
        
        if not img_data:
            return jsonify({"error": "No hay imagen disponible"}), 400

        # Aquí iría la subida a Meta si tienes el Token configurado
        print("✅ Petición procesada correctamente")
        return jsonify({"status": "success", "message": "Recibido correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
