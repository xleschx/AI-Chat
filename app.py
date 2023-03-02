import datetime

import openai
from flask import Flask, render_template, request

# Set up OpenAI API key
openai.api_key_path = 'openAIKey'

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
# Keep track of chat history
chat_history = []


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
                engine='text-davinci-002',
                prompt=user_input,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5,
            )

            # Extract response text from OpenAI API response
            chatbot_response = response.choices[0].text.strip()

            # Add chatbot response to chat history
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    app.run(debug=True)

