# file used to store commands for creating, editing and managing MySQL tables throughout post-processing workflow

import mysql.connector.errors
import database_connection as db
import sql_commands as sql

db_conn = db.conn
cursor = db.cursor


# adds 'post_process_id' column to fields table, necessary before creating raw data table for post-processing
def add_ppid_column_fields_table():
    try:
        add_ppid_column = "ALTER TABLE fields ADD COLUMN post_process_id INT;"
        cursor.execute(add_ppid_column)
    except mysql.connector.errors.ProgrammingError:
        pass


# update fields table in DRAW database with relevant post_process_id's (e.g. '1' for pressure values)
def update_fields_ppid(post_process_id, field_id_tuple):
    if type(field_id_tuple) != tuple:
        field_id_tuple = '({})'.format(field_id_tuple)
    add_post_process_ids = "UPDATE fields " \
                           "SET post_process_id = {} " \
                           "WHERE id IN {};".format(post_process_id, field_id_tuple)
    cursor.execute(add_post_process_ids)
    db_conn.commit()


# command to create composite raw data table from data entries, fields and annotations tables; creating this table is necessary as it enables the
# addition of indexes (which speeds up code considerably during runtime) and standardizes organization of data in DRAW post-processing
def create_raw_data_table():
    cursor.execute("DROP TABLE IF EXISTS data_entries_raw;")
    cursor.execute(sql.composite_raw_data_entries)


# create 'data_entries_corrected' table to store values after cleaned in phase 1
def create_corrected_data_table():
    cursor.execute("DROP TABLE IF EXISTS data_entries_corrected;")
    create_table = "CREATE TABLE data_entries_corrected AS SELECT * FROM data_entries_raw LIMIT 0;"
    cursor.execute(create_table)
    add_flagged_column = "ALTER TABLE data_entries_corrected ADD flagged INT NOT NULL;"
    cursor.execute(add_flagged_column)
    db_conn.commit()


# create 'data_entries_corrected_duplicateless' table to store values after reconciled (post-phase 1)
def create_duplicateless_table():
    cursor.execute("DROP TABLE IF EXISTS data_entries_corrected_duplicateless;")
    cursor.execute("CREATE TABLE IF NOT EXISTS data_entries_corrected_duplicateless AS SELECT * FROM data_entries_corrected LIMIT 0;")
    cursor.execute("SELECT COUNT(*) FROM data_entries_corrected_duplicateless;")
    count = cursor.fetchall()[0][0]
    if count != 0:
        cursor.execute("DELETE FROM data_entries_corrected_duplicateless;")
        db_conn.commit()


# creates 'data_entries_corrected_final' table for post-phase 2 processed data
def create_final_corrected_table():
    cursor.execute("DROP TABLE IF EXISTS data_entries_corrected_final;")
    create_table = "CREATE TABLE data_entries_corrected_final AS SELECT * FROM data_entries_corrected_duplicateless LIMIT 0;"
    cursor.execute(create_table)


# creates 'data_entries_phase_{}_errors' table for error and edit documentation
def create_error_edit_table(phase):
    cursor.execute("DROP TABLE IF EXISTS data_entries_phase_{}_errors;".format(phase))
    cursor.execute(sql.create_error_edit_table(phase))


# adds entry to "data_entries_corrected" table
def add_to_corrected_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db_conn.commit()


# adds entry to "data_entries_corrected_final" table (after phase 2 checking)
def add_to_final_corrected_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected_final " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db_conn.commit()


# add flag or edit made to particular value to "data_entries_phase_{}_errors" table (depending on chosen input parameter, can be for phase 1 or 2)
def add_error_edit_code(phase, error_code, original_value, corrected_value, entry_list, add_info=''):
    entry_id = entry_list[0]
    user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = [None for i in range(8)]
    if phase == 1:
        user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_list[2:]  # deal with 10 rows
    elif phase == 2:
        user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_list[2:len(entry_list) - 1]  # deal with 11 rows
    sql_command = "INSERT INTO data_entries_phase_{}_errors " \
                  "(id, ORIGINAL_VALUE, CORRECTED_VALUE, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, additional_info) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(phase)
    cursor.execute(sql_command, (entry_id, original_value, corrected_value, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, add_info))
    db_conn.commit()


# add reconciled observation entry to duplicateless table (after phase 1)
def add_to_duplicateless_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected_duplicateless " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db_conn.commit()


# updates duplicateless table - used to update MySQL table during observation reconciliation, before continuing with phase 2
def update_duplicateless_table(value, entry_id):
    sql_command = "UPDATE data_entries_corrected_duplicateless " \
                  "SET value = %s " \
                  "WHERE id = %s;"
    cursor.execute(sql_command, (value, entry_id))
    db_conn.commit()


# deletes MySQL table at the very end of post-processing
def delete_table(name):
    sql_command = "DROP TABLE {};".format(name)
    cursor.execute(sql_command)
