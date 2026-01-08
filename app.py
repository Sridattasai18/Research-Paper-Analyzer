from flask import Flask, render_template, jsonify
from routes.ingestion import ingest_bp
from routes.query import query_bp
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Phase 5: Routing
app.register_blueprint(ingest_bp)
app.register_blueprint(query_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Ensure data dir exists for deliverables
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
