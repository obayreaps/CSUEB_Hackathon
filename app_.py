from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__, static_folder='templates/static')
api_key = os.getenv('OPENAI_API_KEY')  # Make sure you have this API key set up properly
openai.api_key = api_key

@app.route("/")
def index():
    # Render the main_menu.html file
    return render_template('main_menu.html')

@app.route('/main_menu.html')
def main_menu():
    return render_template('main_menu.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/userRegistration.html')
def registration():
    return render_template('userRegistration.html')

@app.route('/questions.html')
def questions():
    return render_template('questions.html')

@app.route('/scholarship.html')
def scholarships():
    return render_template('scholarship.html')

def getGptResponse(user_input, results=1):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_input}
        ],
        max_tokens=120,
        n=results
    )
    # Update this to include both the response text and URLs
    responses = [
        {
            'text': choice['message']['content'].strip(),
            'url': extract_url(choice['message']['content'])  # Extract URLs from response text if any
        }
        for choice in response['choices']
    ]
    return responses

# Example URL extraction function (adjust as necessary)
def extract_url(text):
    import re
    urls = re.findall(r'(https?://\S+)', text)
    return urls[0] if urls else None

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt')
    return jsonify({'response': getGptResponse(user_input, 1)[0]})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    # Extract all the fields from the submitted form data
    age = data.get('age')
    education = data.get('education-level')
    ethnicity = data.get('ethnicity')
    programs = data.get('programs')
    income = data.get('income')
    essay = 'No Essay' if data.get('essay') else 'Essay required'
    field_of_study = data.get('field-of-study')
    citizenship = data.get('citizenship')
    achievements = data.get('achievements')
    activities = data.get('activities')
    career_goals = data.get('career-goals')
    special_needs = 'Yes' if data.get('special-needs') else 'No'
    military_service = 'Yes' if data.get('military-service') else 'No'
    hobbies = data.get('hobbies')

    # Create the user input for GPT
    user_input = (
        f"Find scholarships for someone who is {age} years old, identifies as {ethnicity}, "
        f"with a {education} education level, involved in {programs}, has a household income of {income}, "
        f"{essay}, studying {field_of_study}, with citizenship status as {citizenship}. "
        f"They have achievements in {achievements}, involved in extracurricular activities such as {activities}, "
        f"with career goals of {career_goals}. Special needs: {special_needs}. "
        f"Military service: {military_service}. Hobbies: {hobbies}. "
        "Provide links to relevant scholarships if possible."
    )

    # Get GPT responses including links
    responses = getGptResponse(user_input, 10)

    # Print responses and return them in JSON format
    print(responses)
    return jsonify({'responses': responses}), 200

if __name__ == '__main__':
    app.run(debug=True)
