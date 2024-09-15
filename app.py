from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__)
api_key = os.getenv('API Key')
openai.api_key = api_key

def getGptResponse(user_input, results=1):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_input}
        ],
        max_tokens=100,
        n=results
    )
    responses = [choice['message']['content'].strip() for choice in response['choices']]
    return responses

@app.route('/questions.html', methods=['POST'])
def submit():
    data = request.json

    # Capturing all the form inputs from the questionnaire
    age = data.get('age')
    education_level = data.get('education-level')
    ethnicity = data.get('ethnicity')
    programs = data.get('programs')
    income = data.get('income')
    essay_required = data.get('essay')  # Checkbox, either true or false
    field_of_study = data.get('field-of-study')
    citizenship = data.get('citizenship')
    achievements = data.get('achievements')
    activities = data.get('activities')
    career_goals = data.get('career-goals')
    special_needs = data.get('special-needs')  # Checkbox, either true or false
    military_service = data.get('military-service')  # Checkbox, either true or false
    hobbies = data.get('hobbies')

    # Creating a user prompt for GPT using all the form data
    user_input = (
        f"Find scholarships for someone who is {age} years old, studying {field_of_study}. "
        f"They are a {citizenship} with {achievements}. "
        f"They are involved in {activities} and have career goals to become {career_goals}. "
        f"Ethnicity: {ethnicity}. Involved programs: {programs}. "
        f"Household income level: {income}. "
        f"Essay required: {'No' if essay_required else 'Yes'}. "
        f"Special needs: {'Yes' if special_needs else 'No'}. "
        f"Military involvement: {'Yes' if military_service else 'No'}. "
        f"Hobbies and personal interests include {hobbies}."
    )

    # Get 10 responses from GPT
    responses = getGptResponse(user_input, 10)

    return jsonify({'responses': responses}), 200

if __name__ == '__main__':
    app.run(debug=True)
