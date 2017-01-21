from peewee import MySQLDatabase, Model

conn_params = {
    "user": "internetprodaja",
    "password": "internetprodaja",
    "port": 33333
}

operational_db = MySQLDatabase('operational', **conn_params)
analytics_db = MySQLDatabase('analytics', **conn_params)


class OperationalModel(Model):
    class Meta:
        database = operational_db


class AnalyticsModel(Model):
    class Meta:
        database = analytics_db
