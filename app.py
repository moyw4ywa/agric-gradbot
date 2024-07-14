from flask import Flask, render_template, request, redirect, url_for 
from agric_bot import AgricultureBot
from gemini_api import GeminiAPI
import os
from google.oauth2 import service_account
from google.cloud import aiplatform_v1

# Ensure correct import for GenerativeServiceClient
try:
    from google.generativeai.generative_models_v1beta import GenerativeServiceClient
except ModuleNotFoundError:
    # Handle error if the module is not found
    print("Module 'google.generativeai.generative_models_v1beta' not found")

app = Flask(__name__)

# Load API key from environment variables
api_key = os.getenv('GOOGLE_API_KEY')

# Create credentials for AI Platform Prediction Service
if api_key:
    credentials = service_account.Credentials.from_service_account_info(api_key)
    client = aiplatform_v1.PredictionServiceClient(credentials=credentials)
else:
    print("GOOGLE_API_KEY not found in environment variables")

# Initialize the Agriculture Bot and Gemini API
agriculture_bot = AgricultureBot()
gemini_api = GeminiAPI()

@app.route('/')
def index():
    return render_template('index.html', agriculture_advice=None, agriculture_response=None)

@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            agriculture_advice, agriculture_response = get_response(user_input)
            return render_template('index.html', agriculture_advice=agriculture_advice, agriculture_response=agriculture_response)
        else:
            return "Please enter a question or describe an agricultural concern."

@app.route('/main_app')
def main_app():
    return redirect("https://www.example.com")

@app.route('/subscribe')
def subscribe():
    return redirect("https://agrigrow-signup.onrender.com")

def get_response(user_input):
    agriculture_advice = agriculture_bot.get_agricultural_advice(user_input)
    agriculture_response = gemini_api.generate_response(user_input)
    return agriculture_advice, agriculture_response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
