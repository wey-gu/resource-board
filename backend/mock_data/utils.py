#!/bin/env python
from app.models import Resources, Users, States, Resource_records
from copy import deepcopy
from datetime import datetime
from mock_data.data import mock_resources, \
    mock_users, mock_states, \
    mock_resource_records


def insert_mockdata_to_db(
        db_instance,
        mock_resources,
        mock_users,
        mock_states,
        mock_resource_records):
    db = db_instance
    for r in mock_resources:
        _r = deepcopy(r)
        _r['last_changed_at'] = datetime.strptime(
            r['last_changed_at'], '%Y-%m-%d %H:%M')
        _ = Resources(**_r)
        db.session.add(_)
    for u in mock_users:
        _ = Users(**u)
        db.session.add(_)
    for s in mock_states:
        _ = States(**s)
        db.session.add(_)
    for r in mock_resource_records:
        _ = Resource_records(**r)
        db.session.add(_)
    db.session.commit()


hash_name_to_index = {}

for index, item in enumerate(mock_resources):
    hash_name_to_index[item['name']] = index


def build_mockdb(app, db):
    """ build mocking db for test """
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
