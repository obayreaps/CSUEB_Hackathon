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

def getGptResponse(user_input, results=1):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_input}
        ],
        max_tokens=120,
        n=results
    )
    responses = [choice['message']['content'].strip() for choice in response['choices']]
    return responses

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt')
    return jsonify({'response':  getGptResponse(user_input, 1)[0]})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    age = data.get('age')
    gender = data.get('gender')
    education = data.get('education')
    income = data.get('income')
    location = data.get('location')
    # Create the user input for GPT
    user_input = f"Short respone. Find scholarships for someone who is {age} years old, {gender}, with a {education} level education, residing in {location}, with an income of {income}. Also send the links to the scholarships if possible."
    # Get 10 responses from GPT
    responses = getGptResponse(user_input, 10)
    return jsonify({'responses': responses}), 200

if __name__ == '__main__':
    app.run(debug=True)
