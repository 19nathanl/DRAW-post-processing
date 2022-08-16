import database_connection as db
import sql_commands as sql

db = db.db
cursor = db.cursor()


#  command to create composite raw data table from data entries, fields and annotations tables; creating this table is necessary as it enables the
# addition of indexes, which speeds up code considerably during runtime
def create_raw_data_table():
    cursor.execute(sql.composite_raw_data_entries)


# create 'data_entries_corrected' table to store values after cleaned in phase 1
def create_corrected_data_table():
    create_table = "CREATE TABLE data_entries_corrected AS SELECT * FROM data_entries_raw LIMIT 0;"
    cursor.execute(create_table)
    add_flagged_column = "ALTER TABLE data_entries_corrected ADD flagged INT NOT NULL;"
    cursor.execute(add_flagged_column)
    db.commit()
    # TODO : add indexes if necessary


# creates 'data_entries_corrected_final' table for post-phase 2 processed data
def create_final_corrected_table():
    # TODO : need to ensure that corrected / duplicateless table isn't deleted before we can use it as template in SQL command below (i.e. 'AS SELECT * FROM .......')
    create_table = "CREATE TABLE data_entries_corrected_final AS SELECT * FROM data_entries_corrected_duplicateless LIMIT 0;"
    cursor.execute(create_table)


# adds entry to "data_entries_corrected" or "data_entries_corrected_final" table
def add_to_corrected_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged, final=0):
    append_final = final
    if final == 1:
        append_final = '_final'
    sql_command = "INSERT INTO data_entries_corrected{} " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(append_final)
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db.commit()


# add flag or edit made to particular value to "data_entries_phase{}_errors" table (depending on chosen input parameter, can be for phase 1 or 2)
def add_error_edit_code(phase, error_code, original_value, corrected_value, entry_info, add_info=''):
    entry_id = entry_info[0]
    user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_info[2:]
    sql_command = "INSERT INTO pressure_entries_phase{}_errors " \
                  "(id, ORIGINAL_VALUE, CORRECTED_VALUE, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, additional_info) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(phase)
    cursor.execute(sql_command, (entry_id, original_value, corrected_value, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, add_info))
    db.commit()


# add reconciled observation entry to duplicateless table (after phase 1)
def add_to_duplicateless_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected_duplicateless " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db.commit()


# updates duplicateless table - used to update MySQL table during observation reconciliation, before continuing with phase 2
def update_duplicateless_table(value, entry_id):
    sql_command = "UPDATE data_entries_corrected_duplicateless " \
                  "SET value = %s " \
                  "WHERE id = %s;"
    cursor.execute(sql_command, (value, entry_id))
    db.commit()
