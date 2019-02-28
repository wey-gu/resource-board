from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit
from mock_data import db_mock_resources, db_index_hash, \
  db_mock_resource_history
import json
import datetime

# configuration
DEBUG = True
HISTORY_ENTRIES_MAX = 50
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# enable CORS
CORS(app)


# http server handle requests as below
@app.route('/resources', methods=['GET'])
def fetch_resources():
    """ get all resources """
    return jsonify(json.dumps(db_mock_resources))


@app.route('/resource/<name>/history', methods=['GET'])
def fetch_resource_history(name):
    """ get resource history """
    # maximum history query legnth is HISTORY_ENTRIES_MAX
    history = db_mock_resource_history.get(name, [])[-HISTORY_ENTRIES_MAX:]
    return jsonify(json.dumps({name: history}))


# socketio server handle events as below
@socketio.on('update resource')
def update_resource_server(res):
    # factors to be recorded
    factors = [
        'used_by',
        'state',
        'note'
    ]
    timestamp_factor = 'last_changed_at'
    # including timestamp
    record_factors = factors + [timestamp_factor]
    db_res = db_mock_resources[db_index_hash[res['name']]]
    # for any changes, update and record in history
    if any(db_res[factor] != res[factor] for factor in factors):
        for factor in factors:
            db_res[factor] = res[factor]
        timestamp = datetime.datetime.utcnow().__str__()
        # update database resource
        db_res[timestamp_factor] = timestamp
        db_mock_resource_history[res['name']].append(
            {factor: db_res[factor] for factor in record_factors}
        )
    # print(str(db_res))
    emit('updateResource', (json.dumps(db_res)), broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
