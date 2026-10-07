import os
from flask import Flask, jsonify

app = Flask(__name__)

COLOR = os.getenv("APP_COLOR", "BLUE")
VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.route('/', methods=['GET'])
def index():
    return f"Payment Service {VERSION} ({COLOR} - ACTIVE)\n", 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="UP", color=COLOR, version=VERSION), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)