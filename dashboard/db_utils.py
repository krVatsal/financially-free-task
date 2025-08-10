import sqlite3
import pandas as pd
import os

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def load_csv_to_sqlite(csv_path, db_path, table_name):
    df = pd.read_csv(csv_path)
    conn = create_connection(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def query_data(db_path, query):
    conn = create_connection(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    base = os.path.dirname(__file__)
    db_path = os.path.join(base, 'vehicle_data.db')
    # Four wheeler
    csv_path_4w = os.path.join(base, 'four_wheeler_data.csv')
    load_csv_to_sqlite(csv_path_4w, db_path, 'four_wheeler')
    # Three wheeler
    csv_path_3w = os.path.join(base, 'three_wheeler_data.csv')
    load_csv_to_sqlite(csv_path_3w, db_path, 'three_wheeler')
    # Two wheeler
    csv_path_2w = os.path.join(base, 'two_wheeler_data.csv')
    if os.path.exists(csv_path_2w):
        load_csv_to_sqlite(csv_path_2w, db_path, 'two_wheeler')
    print('CSVs loaded to SQLite DB.')
