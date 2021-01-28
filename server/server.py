from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# cors settings needed to prevent CORS errors when testing on localhost
# this should be removed when we deploy to production servers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'  

@app.route("/")
@cross_origin()
def helloWorld():
  return {'text': "Hello, world!!!!"}