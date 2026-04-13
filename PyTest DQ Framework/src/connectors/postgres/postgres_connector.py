
import psycopg2
import pandas as pd

class PostgresConnectorContextManager:
    def __init__(self, db_host, db_name, db_user, db_password, db_port=5432):
        self.conn_params = {
            "host": db_host,
            "database": db_name,
            "user": db_user,
            "password": db_password,
            "port": db_port
        }
        self.connection = None

    def __enter__(self):
        # create conn
        self.connection = psycopg2.connect(**self.conn_params)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # close
        if self.connection:
            self.connection.close()

    def get_data_sql(self, sql):
        # exec query, result = pandas df
        return pd.read_sql_query(sql, self.connection)


