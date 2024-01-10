import os

from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)


def get_services():
    # Log to stdout to confirm the function call
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    END = '\033[0m'
    print(f"{BOLD}{GREEN} Local function {get_services.__name__} called{END}")
    
    services = ["General cleaning", "Specialized cleaning"]
    return services

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_services",
            "description": "List all cleaning services",
        }
    }
]

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        content = request.json.get('content')

        # Chatbot should be able to answer only 1 user question
        if content.lower() == 'what services do you provide?':
            messages = [request.json]

            # Generate response using OpenAI GPT-3.5
            response = client.chat.completions.create(
                model='gpt-3.5-turbo-1106',
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # Check if model wants to call a function
            if tool_calls:
                available_functions = {
                    "get_services": get_services,
                    }
                messages.append(response_message)  # Extend conversation with assistant's reply

                # Handle multiple function
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    # invoke function
                    function_response = function_to_call()
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": "".join(function_response),
                        }
                    )
                # Get a new response from the model where it can see the function response
                second_response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=messages,
                )
                generated_answer = second_response.choices[0].message.content
                
                # Return the response in JSON format
                return jsonify({'answer': generated_answer})
        else:
            return jsonify({'answer': 'I can only answer the question: "What services do you provide?"'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
