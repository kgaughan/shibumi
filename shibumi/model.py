import bottle
import bottle_peewee
import peewee


# Set PEEWEE_CONNECTION in the environment.
db = bottle_peewee.PeeweePlugin()


class BaseModel(peewee.Model):

    class Meta:
        database = db.proxy


class User(BaseModel):

    class Meta:
        db_table = 'users'

    uname = peewee.FixedCharField(max_length=32)
    pwd = peewee.FixedCharField(max_length=32)
    name = peewee.CharField(max_length=64)


class Page(BaseModel):

    class Meta:
        db_table = 'pages'

    slug = peewee.CharField(max_length=150, unique=True)
    time_c = peewee.DateTimeField()
    time_m = peewee.DateTimeField()
    user_c = peewee.ForeignKeyField(User, db_column='user_id_c', related_name='pages')
    user_m = peewee.ForeignKeyField(User, db_column='user_id_m')
    title = peewee.CharField(max_length=255)
    content = peewee.TextField()
    style = peewee.CharField(max_length=64)


class Entry(BaseModel):

    class Meta:
        db_table = 'weblog'

    title = peewee.CharField(max_length=255)
    link = peewee.CharField(max_length=511, unique=True, null=True)
    via = peewee.CharField(max_length=511, null=True)
    time_c = peewee.DateTimeField()
    time_m = peewee.DateTimeField()
    user_c = peewee.ForeignKeyField(User, db_column='user_id_c', related_name='entries')
    user_m = peewee.ForeignKeyField(User, db_column='user_id_m')
    note = peewee.TextField()

    @classmethod
    def get_feed(cls):
        return cls.select().order_by(cls.time_m.desc()).limit(50)

    @classmethod
    def get_latest(cls):
        return cls.select().order_by(cls.time_c.desc()).limit(50)

    @classmethod
    def get_most_recent_modification(cls):
        return cls.select(peewee.fn.Max(cls.time_m)).scalar(convert=True)

def create_tables():
    for table in [User, Page, Entry]:
        db.database.create_table(table)
