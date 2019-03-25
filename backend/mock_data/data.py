#!/bin/env python
import json

resources = '''
[
  {
    "name":"DC124",
    "scale":9,
    "note":"",
    "high_availability":true,
    "storage_backend":"SIO",
    "hardware_type":"DELL",
    "last_changed_at":"2019-03-20 12:34",
    "last_changed_by":"0",
    "used_by":"CI",
    "state_name":"ci",
    "id": 1
  },
  {
    "name":"DC127",
    "scale":17,
    "note":"System Test is using it",
    "high_availability":true,
    "storage_backend":"SIO",
    "hardware_type":"DELL",
    "last_changed_at":"2019-03-20 12:34",
    "last_changed_by":"0",
    "used_by":"Jenkins",
    "state_name":"testing",
    "id": 2
  },
  {
    "name":"DC223",
    "scale":1,
    "note":"",
    "high_availability":false,
    "storage_backend":"",
    "hardware_type":"",
    "last_changed_at":"2019-01-20 12:34",
    "last_changed_by":"0",
    "used_by":"Foo Bar",
    "state_name":"testing",
    "id": 3
  },
  {
    "name":"DC188",
    "scale":8,
    "note":"",
    "high_availability":true,
    "storage_backend":"LVM",
    "hardware_type":"DELL",
    "last_changed_at":"2019-01-23 12:34",
    "last_changed_by":"0",
    "used_by":"",
    "state_name":"ci",
    "id": 4
  },
  {
    "name":"DC154",
    "scale":8,
    "note":"",
    "high_availability":true,
    "storage_backend":"LVM",
    "hardware_type":"HP",
    "last_changed_at":"2019-02-20 12:34",
    "last_changed_by":"0",
    "used_by":"Foo Bar",
    "state_name":"ci",
    "id": 5
  },
  {
    "name":"DC209",
    "scale":7,
    "note":"",
    "high_availability":true,
    "storage_backend":"LVM",
    "hardware_type":"DELL",
    "last_changed_at":"2019-02-23 12:34",
    "last_changed_by":"0",
    "used_by":"",
    "state_name":"occupied",
    "id": 6
  },
  {
    "name":"DC214",
    "scale":7,
    "note":"",
    "high_availability":true,
    "storage_backend":"SIO",
    "hardware_type":"HP",
    "last_changed_at":"2019-02-23 00:34",
    "last_changed_by":"0",
    "used_by":"",
    "state_name":"occupied",
    "id": 7
  },
  {
    "name":"DC026",
    "scale":6,
    "note":"",
    "high_availability":true,
    "storage_backend":"SIO",
    "hardware_type":"BSP",
    "last_changed_at":"2019-01-23 12:34",
    "last_changed_by":"0",
    "used_by":"",
    "state_name":"free",
    "id": 8
  }
]
'''

users = '[{"id": 0, "name": "0"}]'
'''
[
  {
    "id": 1,
    "name": "CI"},
  {
    "id": 2,
    "name": "Tom"},
  {
    "id": 3,
    "name": "Jerry"}
]
'''

states = '''
[
  {
    "name": "ci"},
  {
    "name": "free"},
  {
    "name": "occupied"},
  {
    "name": "testing"}
]
'''


resource_records = ""
'''
[
  {
    "id": 1,
    "record": "",
    "res_name": "DC827"},
  {
    "id": 2,
    "record": "",
    "res_name": "DC235"},
  {
    "id": 3,
    "record": "",
    "res_name": "DC289"}
]
'''
dummy_record = '''
  {
    "used_by": "Tom",
    "state_name": "free",
    "note": "Test",
    "last_changed_at": "2019-03-16 06:15:56"
  }
  '''

mock_resources = json.loads(resources)
mock_users = json.loads(users)
mock_states = json.loads(states)
mock_resource_records = {}
# mock_resource_records = json.loads(resource_records)
# for r in mock_resource_records:
#     r['record'] = dummy_record

mock_resource_history = {
    item['name']: [] for item in mock_resources
}
