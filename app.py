from flask import Flask, request, jsonify

app = Flask(__name__)

# Health check endpoint
@app.route("/")
def home():
    return jsonify({"message": "Welcome Lia! Flask API is running "}), 200

# Prediction endpoint (dummy ML logic)
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "value" not in data:
        return jsonify({"error": "Please provide a numeric 'value'"}), 400
    
    val = float(data["value"])
    prediction = val * 1.5  # simple transformation (mock model)
    return jsonify({"input": val, "prediction": prediction}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
