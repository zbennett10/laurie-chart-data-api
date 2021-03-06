import os
from flask import Flask
from flask_pymongo import PyMongo
from flask import request
from flask import jsonify
from flask_cors import CORS
from bson.json_util import dumps

app = Flask(__name__)
CORS(app)

CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING');
if not CONNECTION_STRING:
    CONNECTION_STRING = "mongodb://localhost:27017/mama_chart";

app.config['MONGO_DBNAME'] = 'mama_chart'
app.config['MONGO_URI'] = CONNECTION_STRING

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def get_index():
    return jsonify({"status": "running"})

@app.route('/test', methods=['GET'])
def get_status():
    test = mongo.db.test
    output = []
    for test in test.find():
        output.append({'message': test['message']})
    return jsonify(output[0])

@app.route('/ferritin-levels', methods=['GET'])
def get_ferritin_levels():
    ferritinlevels = mongo.db.ferritinlevel
    output = []
    for level in ferritinlevels.find():
        output.append(level)
    return jsonify(dumps(output))

@app.route('/ferritin-level', methods=['POST'])
def add_ferritin_level():
    newFerritinLevel = request.get_json(silent=True)
    ferritinlevels = mongo.db.ferritinlevel
    addedLevel = ferritinlevels.insert_one(newFerritinLevel)
    return jsonify(dumps(newFerritinLevel))

@app.route('/ferritin-level', methods=['DELETE'])
def delete_ferritin_level():
    id = request.args.get('id', default = None, type = int)
    if(id != None):
        ferritinlevels = mongo.db.ferritinlevel
        deletionResult = ferritinlevels.delete_one({'id': id})
        return jsonify({"result": "success"})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)