import os

from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        content = request.json.get('content')

        # Chatbot should be able to answer only 1 user question
        if content.lower() == 'what services do you provide?':
            # Call local function which returns hardcoded array
            services = get_services()
            
            # Generate response using OpenAI GPT-3.5
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=f"The services we provide are: {', '.join(services)}",
                temperature=0.7,
                max_tokens=500,
                n=1
            )

            generated_answer = response.choices[0].text.strip()

            # Return the response in JSON format
            return jsonify({'answer': generated_answer})
        else:
            return jsonify({'answer': 'I can only answer the question: "What services do you provide?"'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_services():
    # Log to stdout to confirm the function call
    print(f"Local function {get_services.__name__} called")
    return ["General cleaning", "Specialized cleaning"]

if __name__ == '__main__':
    app.run(port=5000)
