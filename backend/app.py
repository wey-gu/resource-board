from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import send, emit
import json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# enable CORS
CORS(app)

mock_resources = '''
[
  {
    "name":"DC209",
    "scale":7,
    "note":"",
    "high_availability":true,
    "storage_backend":"SIO",
    "hardware_type":"HP",
    "last_changed_at":"2019-01-20",
    "last_changed_by":"Jenkins",
    "used_by":"Jenkins",
    "state":"ci"
  },
  {
    "name":"DC214",
    "scale":9,
    "note":"",
    "high_availability":true,
    "storage_backend":"SIO",
    "hardware_type":"DELL",
    "last_changed_at":"2019-02-20",
    "last_changed_by":"Jenkins",
    "used_by":"Jenkins",
    "state":"ci"
  },
  {
    "name":"DC205",
    "scale":5,
    "note":"",
    "high_availability":true,
    "storage_backend":"LVM",
    "hardware_type":"DELL",
    "last_changed_at":"2019-01-20",
    "last_changed_by":"Foo Bar",
    "used_by":"Foo Bar",
    "state":"occupied"
  },
  {
    "name":"DC223",
    "scale":1,
    "note":"",
    "high_availability":false,
    "storage_backend":"",
    "hardware_type":"DELL",
    "last_changed_at":"2019-01-23",
    "last_changed_by":"Foo Bar",
    "used_by":"",
    "state":"free"
  },
  {
    "name":"DC127",
    "scale":12,
    "note":"",
    "high_availability":true,
    "storage_backend":"SIO",
    "hardware_type":"DELL",
    "last_changed_at":"2019-01-20",
    "last_changed_by":"Foo Bar",
    "used_by":"Foo Bar",
    "state":"testing"
  },
  {
    "name":"DC188",
    "scale":6,
    "note":"",
    "high_availability":true,
    "storage_backend":"",
    "hardware_type":"DELL",
    "last_changed_at":"2019-01-23",
    "last_changed_by":"Foo Bar",
    "used_by":"",
    "state":"free"
  },
  {
    "name":"DC154",
    "scale":16,
    "note":"",
    "high_availability":true,
    "storage_backend":"",
    "hardware_type":"DELL",
    "last_changed_at":"2019-01-23",
    "last_changed_by":"Foo Bar",
    "used_by":"",
    "state":"ci"
  }
]
'''
db_mock_resources = json.loads(mock_resources)
db_index_hash = {}
for index, item in enumerate(db_mock_resources):
    db_index_hash[item['name']] = index


# http server handle requests as below
@app.route('/resources', methods=['GET'])
def fetch_resources():
    """ get all resources """
    return jsonify(json.dumps(db_mock_resources))

# socketio server handle events as below
@socketio.on('update resource')
def update_resource_server(res):
    _res = db_mock_resources[db_index_hash[res['name']]]
    _res['used_by'], _res['state'] = res['used_by'], res['state']
    # print(str(_res))
    emit('updateResource', (json.dumps(_res)), broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
