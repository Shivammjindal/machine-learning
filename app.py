from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

model = joblib.load('random_forest_model_advanced.pkl')
scaler = joblib.load('scalers.pkl')
columns = joblib.load('columnss.pkl')

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    result = {
        "user" : True
    }
    return jsonify(result)

@app.route('/predict', methods=["POST"])
def predict():
    try:
        # Step 1: Receive and parse JSON input
        data = request.get_json()

        # Step 2: Convert to DataFrame
        new_data = pd.DataFrame([data])

        # Step 3: Ensure 'Amount' is numeric (convert from string if needed)
        if "Amount" in new_data.columns:
            try:
                # Remove any commas or unexpected characters from amount string
                new_data["Amount"] = new_data["Amount"].astype(str).str.replace(",", "").astype(float)
            except ValueError:
                return jsonify({"error": "Amount must be a numeric value"}), 400

        # Step 4: Apply one-hot encoding
        new_data_encoded = pd.get_dummies(new_data)

        # Step 5: Align columns with training set
        new_data_encoded = new_data_encoded.reindex(columns=columns, fill_value=0)

        # Step 6: Scale the input
        scaled = scaler.transform(new_data_encoded)

        # Step 7: Predict using the trained model
        pred = model.predict(scaled)[0]

        # Step 8: Return the result
        result = "Suspicious: Needs Verification by Bank" if pred == 1 else "Transaction is Fine"
        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)