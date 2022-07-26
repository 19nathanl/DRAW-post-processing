import database_connection as db
import time


###  RUN THIS FILE TO CREATE COMPOSITE RAW DATA TABLE FROM DATA ENTRIES, FIELDS AND ANNOTATIONS TABLES.  ###
###  CREATING THIS RAW DATA TABLE IS NECESSARY BECAUSE IT ALLOWS THE ADDITION OF MYSQL INDEXES, WHICH    ###
###  SPEEDS UP CODE BY CONSIDERABLY DURING POST-PROCESSING RUNTIME.                                      ###

db = db.db
cursor = db.cursor()

# Composite table to be generated:
cursor.execute("SELECT "
               
               "data_entries.id, "
               "data_entries.value, "
               "data_entries.user_id, "
               "data_entries.page_id, "
               "data_entries.field_id, "
               "fields.field_key, "
               "data_entries.annotation_id, "
               "annotations.transcription_id, "
               "fields.post_process_id, "
               "annotations.observation_date "
               ""
               "FROM data_entries "
               "LEFT JOIN fields "
               "ON fields.id = data_entries.field_id "
               "LEFT JOIN annotations "
               "ON data_entries.annotation_id = annotations.id;")

raw_entries_joined_table = cursor.fetchall()


def update_raw_table(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date):
    sql_command = "INSERT INTO data_entries_raw " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date))
    db.commit()


start = time.time()
counter = 0
for joined_entry in raw_entries_joined_table:
    update_raw_table(*joined_entry)
    counter += 1
    print(counter)
print(time.time() - start)
