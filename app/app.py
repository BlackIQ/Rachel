from flask import Flask

app = Flask(__name__)

@app.route('/api/<message>')
def handle(message):
    if (message == "hi"):
        return {
            "response": "Hello, what can I do for you?"
        }, 200
    else:
        return {
            "response": "Sorry I didn't get that."
        }, 404