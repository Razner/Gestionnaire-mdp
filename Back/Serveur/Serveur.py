from flask import Flask, rendertemplate

app = Flask(__name__)

@app.route('/')
def index():
    return rendertemplate('index.html')

if __name__ == '__main':
    app.run(debug=True)