from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Set your OpenAI GPT-3 API key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input for the story prompt
        user_prompt = request.form["story_prompt"]

        try:
            # Send the prompt to the GPT-3 API
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=user_prompt,
                max_tokens=200,
                temperature=0.7,
                n=1,
                stop=None,
            )

            # Get the generated story
            generated_story = response['choices'][0]['text'].strip()

            # Render the HTML template with the generated story
            return render_template(
                "index.html", user_prompt=user_prompt, generated_story=generated_story
            )

        except Exception as e:
            error_message = f"Error: {e}"
            return render_template("index.html", error_message=error_message)

    return render_template("index.html", user_prompt="", generated_story="", error_message="")

if __name__ == "__main__":
    app.run(debug=True)
