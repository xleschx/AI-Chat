import datetime
import os

import openai
from flask import Flask, render_template, request

# Set up OpenAI API key
openai.api_key_path = 'openAIKey'

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
# Keep track of chat history
chat_history = []

# Default settings
DEFAULT_ENGINE = 'text-davinci-002'
DEFAULT_MAX_TOKENS = 1240
DEFAULT_TEMPERATURE = 0.5

# Define settings page route
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Get form values
        engine = request.form['engine']
        max_tokens = request.form['max_tokens']
        temperature = request.form['temperature']

        # Set global variables to new values
        global ENGINE, MAX_TOKENS, TEMPERATURE
        ENGINE = engine
        MAX_TOKENS = int(max_tokens)
        TEMPERATURE = float(temperature)

    # Render settings page
    return render_template('settings.html', engine=ENGINE, max_tokens=MAX_TOKENS, temperature=TEMPERATURE)

# Define home page route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get user input from form
        user_input = request.form['message']

        # Add user input to chat history
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_history.append({'speaker': 'User', 'text': user_input, 'time': current_time})

        # Generate response using OpenAI
        prompt = ""
        for item in chat_history:
            prompt += f"{item['speaker']}: {item['text']}\n"

        try:
            response = openai.Completion.create(
                engine=ENGINE,
                prompt=user_input,
                max_tokens=MAX_TOKENS,
                n=1,
                stop=None,
                temperature=TEMPERATURE,
            )

            # Extract response text from OpenAI API response
            chatbot_response = response.choices[0].text.strip()

            # Add chatbot response to chat history
            chat_history.append({'speaker': 'Chatbot', 'text': chatbot_response})

        except openai.ErrorObject as e:
            # Handle API errors
            chatbot_response = f"Error: {e}"
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            chat_history.append({'speaker': 'Chatbot', 'text': chatbot_response, 'time': current_time})

        # Render home page with chat history
        return render_template('index.html', chat_history=chat_history)

    # Render home page
    return render_template('index.html')

if __name__ == "__main__":
    # Initialize global variables
    ENGINE = DEFAULT_ENGINE
    MAX_TOKENS = DEFAULT_MAX_TOKENS
    TEMPERATURE = DEFAULT_TEMPERATURE

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))