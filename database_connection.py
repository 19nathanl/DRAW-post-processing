import mysql.connector
import sql_commands

# connection to copy of database on local machine
db = mysql.connector.connect(
    user='',
    password='',
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
