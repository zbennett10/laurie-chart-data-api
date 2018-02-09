import os
from flask import Flask
from flask_pymongo import PyMongo
from flask import request
from flask import jsonify
from bson.json_util import dumps

app = Flask(__name__)

CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING');
if not CONNECTION_STRING:
    CONNECTION_STRING = "mongodb://localhost:27017/mama_chart";

app.config['MONGO_DBNAME'] = 'mama_chart'
app.config['MONGO_URI'] = CONNECTION_STRING

mongo = PyMongo(app)

@app.route('/test', methods=['GET'])
def get_status():
    test = mongo.db.test
    output = []
    for test in test.find():
        output.append({'message': test['message']})
    return jsonify(output[0])

@app.route('/ferritin-levels', methods=['GET'])
def get_ferritin_levels():
    ferritinlevel = mongo.db.ferritinlevel
    output = []
    for level in ferritinlevel.find():
        output.append(level)
    return jsonify(dumps(output))

if __name__ == '__main__':
    app.run(debug=True)