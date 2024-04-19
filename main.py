from flask import Flask, request
import numpy as np
import pandas as pd
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
from flask_cors import CORS


file = open("model.pkl","rb")
gbc = pickle.load(file)
file.close()

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        url = data['url']
        print(url)
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]

        pred = "It is {0:.2f} % safe to go ".format(y_pro_non_phishing*100)
        
        response = {"prediction": pred}
        return response

    response = {"prediction": "error"}
    return response


if __name__ == "__main__":
    app.run(debug=False, port=5000)