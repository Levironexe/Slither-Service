from flask import Flask, request, jsonify
from slither import Slither
import tempfile
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_contract():
    try:
        contract_code = request.json.get('code')
        if not contract_code:
            return jsonify({"error": "No code provided"}), 400

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.sol', delete=False) as temp_file:
            temp_file.write(contract_code.encode())
            temp_file_path = temp_file.name

        # Run Slither analysis
        slither = Slither(temp_file_path)
        
        # Get results
        results = []
        for issue in slither.detectors:
            results.append({
                "impact": issue.impact,
                "confidence": issue.confidence,
                "description": issue.description
            })

        # Clean up
        os.unlink(temp_file_path)

        return jsonify({
            "status": "success",
            "results": results
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)