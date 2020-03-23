import sqlite3 as sql
import pandas as pd

db_link = "database.sqlite"

def create_table(table_name):
    # Creates a table in database.sqlite file. If sqlite file not present, it will be created
    conn = sql.connect(db_link)
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE %s
                 (COURSE TEXT NOT NULL,
                 ELEMENT TEXT NOT NULL);''' % table_name)
    except:
        print("Table already exists")
    df1 = pd.read_sql_query("SELECT * from %s" % table_name, conn)
    conn.commit()
    conn.close()
    return df1

def insert(course, element,table_name = "spectrum"):
    # insert entry into the database
    conn = sql.connect(db_link)
    df1 = pd.read_sql_query("SELECT * from %s" % table_name, conn)
    df2 = pd.DataFrame(data={'COURSE': [course], 'ELEMENT': [element]})
    df3 = pd.concat([df1, df2], sort=True)
    df3.drop_duplicates(subset=['ELEMENT'], inplace=True)
    df3.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    return df3

def reset_table(table_name):
    conn = sql.connect(db_link)
    cursor = conn.cursor()
    cursor.execute("drop table %s;" % table_name)
    conn.commit()
    conn.close()
    create_table(table_name)

def compareQuery(course, newElement, table_name = "spectrum"):
    conn = sql.connect(db_link)
    # df1 = pd.read_sql_query("SELECT * from %s WHERE COURSE = '"'%s '"' " %(table_name,course), conn)
    df1 = pd.read_sql_query("SELECT * from %s "  %(table_name), conn)
    df2 = pd.DataFrame(data={'COURSE': [course], 'ELEMENT': [newElement]})
    for x in df1['ELEMENT']:
        if x == df2['ELEMENT'].values[0]:
            # print("hello")
            return True
    return False

