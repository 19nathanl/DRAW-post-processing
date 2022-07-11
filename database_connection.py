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


# accessing all data entries in database, with all necessary information (columns)
def db_data():
    sql_command = sql_commands.main_command
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result
