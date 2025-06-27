import numpy as np
import pandas as pd
import pickle
import os
from flask import Flask, request, render_template

# Initialize Flask app
app = Flask(__name__, template_folder='template')

# Load the trained model
model_path = os.path.join('model.pkl')  # Make sure model.pkl is in the same directory
model = pickle.load(open(model_path, 'rb'))

# Home page
@app.route('/')
def index():
    return render_template('index.html')  # Displays the form

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get form input values
    input_features = [float(x) for x in request.form.values()]
    
    # Define the column names — must match the order used in training
    column_names = ['holiday', 'temp', 'rain', 'snow', 'weather', 
                    'year', 'month', 'day', 'hours', 'minutes', 'seconds']
    
    # Create DataFrame from input
    input_df = pd.DataFrame([input_features], columns=column_names)

    # Predict
    prediction = model.predict(input_df)[0]
    
    # Render result on output page
    return render_template('output.html', result=f"Estimated Traffic Volume is: {int(prediction)} units")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
