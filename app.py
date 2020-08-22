import secrets, os
from flask import Flask
app = Flask(__name__)
os.environ['PORT'] = '5000'


@app.route("/")
def index():
    return "<h1>Hello Azure!</h1><h3>This is a new change</h3>"

if __name__ == '__main__':
    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key
    port = int(os.environ['PORT'])
    app.run(debug=True, host='0.0.0.0', port=port)