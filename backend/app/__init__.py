#!/bin/env python
"""
resource app
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import Config
import json
import datetime

# instantiate all utils
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
ma = Marshmallow()


# use app factory to enable app instantication for different purposes
#     like frontend debug, or unit test
def create_instance(config=Config):
    app = Flask(__name__)
    # apply configuration by default from object config.Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # frontend debug mock db initilization
    if app.config['DEBUG_FRONTEND']:
        from mock_data.data import mock_resources, \
            mock_users, mock_states, \
            mock_resource_records
        from mock_data.utils import insert_mockdata_to_db

        app_context = app.app_context()
        # cleanup and initiate the mocking db
        app_context.push()
        db.drop_all()
        db.create_all()
        insert_mockdata_to_db(
            db,
            mock_resources,
            mock_users,
            mock_states,
            mock_resource_records
        )

    # socketio instantiation
    socketio.init_app(app)

    # enable CORS
    CORS(app)

    def get_resources(config):
        # if config['DEBUG_FRONTEND']:
        #     return json.dumps(mock_resources)
        resources_schema = models.ResourcesSchema(many=True)
        resource = models.Resources.query.all()
        resources = json.dumps(resources_schema.dump(resource).data)
        return resources

    def modify_resource(config, res):
        resources_schema = models.ResourcesSchema(many=False)
        resource = models.Resources.query.filter(
            models.Resources.name == res['name']).first()
        # factors to be recorded
        factors = [
            'used_by',
            'state_name',
            'note'
        ]
        timestamp_factor = 'last_changed_at'
        # including timestamp
        record_factors = factors + [timestamp_factor]

        # for any changes, update and record in history
        if any(getattr(resource, factor) != res[factor] for factor in factors):
            for factor in factors:
                setattr(resource, factor, res[factor])
            timestamp = datetime.datetime.utcnow()
            timestampString = str(timestamp)
            if not config['DEBUG_FRONTEND']:
                timestamp = timestampString
            # update database resource
            setattr(resource, timestamp_factor, timestamp)

            ''' mock data
            mock_resource_history[res['name']].append(
                {factor: resource[factor] for factor in record_factors}
            )
            '''
            # print(str(mock_resource_history))
            record = {
                factor:
                    str(getattr(resource, factor)) for factor in record_factors
                }
            _record = {
                "record": json.dumps(record),
                "res_name": res['name']
                }
            db.session.add(models.Resource_records(**_record))
            db.session.commit()
        return json.dumps(resources_schema.dump(resource).data)

    def get_histories(config, name):
        '''
        history_length = app.config['HISTORY_ENTRIES_MAX']
        history = mock_resource_history.get(name, [])[-history_length:]
        '''
        records_schema = models.ResRecordsSchema(many=True)
        history = models.Resource_records.query.filter_by(
            res_name=name).order_by(models.Resource_records.id.desc())\
            .limit(config['HISTORY_ENTRIES_MAX'])
        v = [
            json.loads(r['record'])
            for r in records_schema.dump(history).data]
        # reverse it as it was desc during query
        return json.dumps({name: list(reversed(v))})

    # http server handle requests as below
    @app.route('/resources', methods=['GET'])
    def fetch_resources():
        """ get all resources """
        return jsonify(get_resources(app.config))

    @app.route('/resource/<name>/history', methods=['GET'])
    def fetch_resource_history(name):
        """ get resource history """
        # maximum history query legnth is HISTORY_ENTRIES_MAX
        return jsonify(get_histories(app.config, name))

    # socketio server handle events as below
    @socketio.on('update resource')
    def update_resource_server(res):
        updated_res = modify_resource(app.config, res)
        emit('updateResource', (updated_res), broadcast=True)

    return app


from app import models  # NOQA import models here to avoid circular imports
