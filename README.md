# Chatbot LLM (GPT 3.5) API
## Setup
```
pip install -r requirements.txt
```
## Set API key
In file `.env`, replace the placeholder with your API key `OPENAI_API_KEY="YOUR_KEY_HERE"`
## Usage
### Run application
```
python app.py
```
### Send POST request
Use Postman or a separate terminal to send request.
```
curl -X POST -H "Content-type: application/json" --data @data.json http://127.0.0.1:5000/chatbot
```