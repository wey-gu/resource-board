import json

mock_resources = '''
[
  {
    "name":"DC289",
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
    "name":"DC294",
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
    "name":"DC235",
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
    "name":"DC273",
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
    "name":"DC827",
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
    "name":"DC908",
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
    "name":"DC1254",
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
db_mock_resource_history = {
  item['name']: [] for item in db_mock_resources
  }
