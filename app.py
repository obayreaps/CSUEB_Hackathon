from flask import Flask, render_template, request, jsonify
from key import apiKey
import openai

app = Flask(__name__)

openai.api_key = apiKey

@app.route('/')
def index():
    # Render the page.html file
    return render_template('page.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt')
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=user_input,
        max_tokens=50
    )
    return jsonify(response['choices'][0]['text'].strip())

if __name__ == '__main__':
    app.run(debug=True)