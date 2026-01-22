from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/meta", methods=["POST"])
def launch_campaign():
    data = request.json

    # Simulación segura (NO Facebook real)
    return jsonify({
        "ok": True,
        "id": "SIM_CAMPAIGN_123456",
        "message": "Campaña simulada correctamente"
    }), 200


@app.route("/api/meta", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
