from flask import Flask, render_template, request, redirect, url_for 
from agric_bot import AgricultureBot
from gemini_api import GeminiAPI

app = Flask(__name__)

# Initialize the Agriculture Bot and Agriculture API
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

if __name__ == '__main__':
    app.run(debug=True)
