import pymysql.cursors
import collections
import json

DatabaseCredential = collections.namedtuple("DatabaseCredential", ["host", "port", "user", "password", "database"])

def createCredential(host, port, user, password, database):
    return DatabaseCredential(host, port, user, password, database)

def createConnection(credential):
    return pymysql.connect(host=credential.host,
                                 port=credential.port,
                                 user=credential.user,
                                 password=credential.password,
                                 db=credential.database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

def execute(connection, sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()

def bulkInsert(connection, sql, data):
    with connection.cursor() as cursor:
        affected = cursor.executemany(sql, data)
        print("Inserted {} rows", affected)
        connection.commit()
