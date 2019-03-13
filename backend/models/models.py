db_engine = sa.create_engine('sqlite:///db.sqlite')
metadata = sa.MetaData()


# Table definition - users
# 
users_table = sa.Table("users", metadata,
    sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True),
    sa.Column('name', sa.String, nullable=True))

# Table definition - resources
# 
resources_table = sa.Table("resources", metadata,
    sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True),
    sa.Column('name', sa.String, nullable=True),
    sa.Column('scale', sa.Integer, nullable=True),
    sa.Column('note', sa.String, nullable=True),
    sa.Column('is_ha', sa.Boolean, nullable=True),
    sa.Column('hardware_type', sa.String, nullable=True),
    sa.Column('changed_at', sa.DateTime, nullable=True),
    sa.Column('changed_by_user_id', sa.String, nullable=True),
    sa.Column('state_id', sa.String, nullable=True))

# Table definition - states
# 
states_table = sa.Table("states", metadata,
    sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True),
    sa.Column('name', sa.String, nullable=True))

# Table definition - resource_record
# 
resource_record_table = sa.Table("resource_record", metadata,
    sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True),
    sa.Column('res_id', sa.Integer, nullable=True),
    sa.Column('record', sa.String, nullable=True))


# Mapping Objects
class users():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<users('%s', '%s')>" % (self.id, self.name)

class resources():
    def __init__(self, id, name, scale, note, is_ha, hardware_type, changed_at, changed_by_user_id, state_id):
        self.id = id
        self.name = name
        self.scale = scale
        self.note = note
        self.is_ha = is_ha
        self.hardware_type = hardware_type
        self.changed_at = changed_at
        self.changed_by_user_id = changed_by_user_id
        self.state_id = state_id

    def __repr__(self):
        return "<resources('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.name, self.scale, self.note, self.is_ha, self.hardware_type, self.changed_at, self.changed_by_user_id, self.state_id)

class states():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<states('%s', '%s')>" % (self.id, self.name)

class resource_record():
    def __init__(self, id, res_id, record):
        self.id = id
        self.res_id = res_id
        self.record = record

    def __repr__(self):
        return "<resource_record('%s', '%s', '%s')>" % (self.id, self.res_id, self.record)


# Declare mappings
mapper(users, users_table)
mapper(resources, resources_table)
mapper(states, states_table)
mapper(resource_record, resource_record_table)

# Create a session
session = sessionmaker(bind=db_engine)