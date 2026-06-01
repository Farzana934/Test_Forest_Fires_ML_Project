import pickle
from flask import Flask, request, render_template
import numpy as np

application = Flask(__name__)
app = application

# Load model and scaler
ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scaler.pkl', 'rb'))

sample = [[30, 50, 15, 0, 85, 10, 5, 1, 0]]

scaled = standard_scaler.transform(sample)
print("Prediction:", ridge_model.predict(scaled))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predictData", methods=['GET', 'POST'])
def predict_datapoint():

    if request.method == "POST":
        try:
            # Debugging prints
            print("Form Data Received:")
            print(request.form)

            print("Scaler expects:", standard_scaler.n_features_in_)

            Temperature = float(request.form.get('Temperature'))
            RH = float(request.form.get('RH'))
            Ws = float(request.form.get('Ws'))
            Rain = float(request.form.get('Rain'))
            FFMC = float(request.form.get('FFMC'))
            DMC = float(request.form.get('DMC'))
            ISI = float(request.form.get('ISI'))
            Classes = float(request.form.get('Classes'))
            Region = float(request.form.get('Region'))

            features = [[
                Temperature,
                RH,
                Ws,
                Rain,
                FFMC,
                DMC,
                ISI,
                Classes,
                Region
            ]]

            print("Received Features:", features)

            new_data = standard_scaler.transform(features)

            print("Scaled Data:", new_data)

            result = ridge_model.predict(new_data)

            print("Prediction:", result)

            return render_template(
                'home.html',
                results=round(result[0], 2)
            )

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"ERROR: {str(e)}"

    return render_template('home.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)