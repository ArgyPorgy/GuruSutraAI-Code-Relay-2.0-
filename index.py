from flask import Flask, render_template, request
import json
import random
import os

app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, "dataset.json")

with open(json_file_path, "r") as file:
    quotes_data = json.load(file)

def generate_quote(category=None):
    if category:
        quotes = [quote for quote in quotes_data if quote["category"] == category]
    else:
        quotes = quotes_data
    quote = random.choice(quotes)
    return quote["quote"] + " - " + quote["author"]

@app.route('/')
def render():
    return render_template('index.html', generated_quote=None)

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    
    if prompt.strip():  
        if "sad" in prompt.lower(): 
            generated_quote = generate_quote(category="sadness")
        elif "depressed" in prompt.lower():
            generated_quote = generate_quote(category="spirituality")
        elif "good enough" in prompt.lower():
            generated_quote = generate_quote(category="insecurity")
        else:
            generated_quote = generate_quote()
    else:
        # If the input is empty, set the response text to an empty string
        generated_quote = ""

    return render_template('index.html', generated_quote=generated_quote)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
