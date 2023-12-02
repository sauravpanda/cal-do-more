from flask import Flask

app = Flask(__name__)

@app.route('/response')
def parthit():
    return 'Parthit!'

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)