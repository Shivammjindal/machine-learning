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
        data = request.get_json()
        new_data = pd.DataFrame([data])

        new_data_encoded = pd.get_dummies(new_data)
        new_data_encoded = new_data_encoded.reindex(columns=columns, fill_value=0)

        scaled = scaler.transform(new_data_encoded)

        # Predict
        pred = model.predict(scaled)[0]
        result = "Suspecious Need to be Varified by Bank" if pred == 1 else "You Transaction is Fine"

        return jsonify({"prediction": result})
    
    except Exception as e:
        return jsonify({"error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)