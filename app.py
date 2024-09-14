from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__)
api_key = os.getenv('MY_API_KEY')
openai.api_key = api_key

@app.route("/")
def index():
    # Render the page.html file
    return render_template('page.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt')
    
    # Update to use the chat completion endpoint
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-4" or another model as needed
        messages=[
            {"role": "user", "content": user_input}
        ],
        max_tokens=50
    )
    
    # Extract the response content
    return jsonify(response['choices'][0]['message']['content'].strip())

if __name__ == '__main__':
    app.run(debug=True)
