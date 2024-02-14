from flask import Flask, rendertemplate

app = Flask(__name__)

@app.route('/')
def index():
    return rendertemplate('index.html')

if name == '__main':
    app.run(debug=True)