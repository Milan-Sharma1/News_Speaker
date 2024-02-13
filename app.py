from flask import Flask, render_template, request
import pythoncom
from win32com.client import Dispatch
import json
import requests

app = Flask(__name__)

def speak(name, headlines):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(f"Hello {name}, here are the latest headlines:")
    i = 1
    for item in headlines:
        speak.Speak(f"Headline number {i} : {item}")
        i += 1
        if i == 2:
            break

@app.route('/', methods=['GET', 'POST'])
def index():
    pythoncom.CoInitialize()
    if request.method == 'POST':
        name = request.form['name']

        url = 'http://newsapi.org/v2/top-headlines?country=in&apiKey=ce0a4af8d2814e3f97a21282f7983c8e'
        response = requests.get(url)
        data = response.json()
        headlines = [item.get("title") for item in data["articles"]]
        speak(name, headlines)

        return json.dumps(headlines[:20])
    else:
        return render_template('index.html', button_text='Get Headlines')

if __name__ == '__main__':
    app.run(debug=True)
