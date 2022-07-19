import mysql.connector
import sql_commands
import os

# connection to copy of database on local machine
db = mysql.connector.connect(
    user=os.environ.get('DRAW_local_db_user'),
    password=os.environ.get('DRAW_local_db_pass'),
    database='climatedatarescuetest',
    host='localhost'
)

cursor = db.cursor()


# returning raw data entries from database, with all necessary information (columns)
def raw_data():
    sql_command = sql_commands.raw_data_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result


# returning phase 1-corrected data entries from database, with all necessary information (columns)
def phase_1_corrected_data():
    sql_command = sql_commands.phase_1_corrected_data_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result
