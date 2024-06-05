from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai

api = 'sk-proj-7xRsQNoIhswT7SNg4TV3T3BlbkFJypKBCmPBdXmWx85zrvIm'
client = openai.OpenAI(api_key=api)

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=["POST"])
def get_response():
    if request.method == "POST":
        query = request.json['message']
        response = ""
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            stream=True,
        )
        for chunk in stream:
             if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
                print(response)

        return jsonify({'answer': response})
 
    return jsonify({'error': 'Method Not Allowed'}), 405
   
if __name__ == '__main__':
    app.run(debug=True, port=6400)
