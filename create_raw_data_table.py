import database_connection as db
import sql_commands as sql


###     RUN THIS FILE TO CREATE COMPOSITE RAW DATA TABLE FROM DATA ENTRIES, FIELDS AND ANNOTATIONS TABLES.        ###
###     CREATING THIS RAW DATA TABLE IS NECESSARY BECAUSE IT ALLOWS THE ADDITION OF MYSQL INDEXES, WHICH          ###
###     SPEEDS UP CODE CONSIDERABLY DURING POST-PROCESSING RUNTIME.                                               ###

db = db.db
cursor = db.cursor()


def update_raw_table(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date):
    sql_command = "INSERT INTO data_entries_raw " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date))
    db.commit()


def create_raw_data_entries():
    cursor.execute(sql.composite_raw_data_entries)
    raw_entries_joined_table = cursor.fetchall()
    for joined_entry in raw_entries_joined_table:
        update_raw_table(*joined_entry)
