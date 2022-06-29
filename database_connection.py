import mysql.connector

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
    sql_command = "SELECT " \
                  \
                  "pressure_entries.id, " \
                  "pressure_entries.value, " \
                  "pressure_entries.user_id, " \
                  "pressure_entries.page_id, " \
                  "pressure_entries.field_id, " \
                  "fields.field_key, " \
                  "pressure_entries.annotation_id, " \
                  "annotations.transcription_id, " \
                  "fields.post_process_id, " \
                  "annotations.observation_date, " \
                  "pressure_entries.error_code, " \
                  "pressure_entries.corrected_value " \
                  \
                  "FROM pressure_entries " \
                  "LEFT JOIN fields " \
                  "ON fields.id = pressure_entries.field_id " \
                  "LEFT JOIN annotations " \
                  "ON pressure_entries.annotation_id = annotations.id " \
                  "LIMIT 1;"  # TODO : remove this row after testing
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result
