from peewee import SqliteDatabase, Model


operational_db = SqliteDatabase('operational.db')
analytics_db = SqliteDatabase('analytics.db')


class OperationalModel(Model):
    class Meta:
        database = operational_db


class AnalyticsModel(Model):
    class Meta:
        database = analytics_db
