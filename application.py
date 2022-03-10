from flask import Flask
from flask_cors import CORS

# import any blueprints from routes folder
app = Flask(__name__)

@app.route('/token')
def get_token():
    return {'message': 'got to the token endpoint'}

@app.route('/jobs')
def get_jobs():
    return {'message': 'got to the jobs endpoint'}
CORS(app)

if __name__ == "__main__":
    app.debug = True
    app.run()
