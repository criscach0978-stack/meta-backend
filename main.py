from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/launch-campaign", methods=["POST"])
def launch_campaign():
    return jsonify({
        "ok": True,
        "message": "Backend funcionando correctamente"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print("🚀 Backend activo en puerto", port)
    app.run(host="0.0.0.0", port=port)
