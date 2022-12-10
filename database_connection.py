import mysql.connector
import sql_commands
import os


# connection to copy of database on local machine
conn = mysql.connector.connect(
    #####   FOLLOWING 3 VARIABLES TO BE CONFIGURED AS NECESSARY FOR LOCAL MACHINE:   #####
    # user=os.environ.get('DRAW_local_db_user'),
    # password=os.environ.get('DRAW_local_db_pass'),
    user='Nathan',
    password='123456',
    database='climatedatarescueprocessed_test',

    host='localhost'
)

cursor = conn.cursor()


# returning raw data entries from database, with all necessary information (columns)
def raw_data():
    sql_command = sql_commands.raw_data_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result


# returning phase 1-corrected, duplicateless data entries => for phase 2
def phase_1_data():
    sql_command = sql_commands.phase_1_data_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result
