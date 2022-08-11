import database_connection as db

db = db.db
cursor = db.cursor()


# create 'data_entries_corrected' table to store values after cleaned in phase 1
def create_corrected_data_table():
    create_table = "CREATE TABLE data_entries_corrected AS SELECT * FROM data_entries_raw LIMIT 0;"
    cursor.execute(create_table)
    add_flagged_column = "ALTER TABLE data_entries_corrected ADD flagged INT NOT NULL;"
    cursor.execute(add_flagged_column)
    db.commit()
    # TODO : add indexes if necessary


# update value to "data_entries_corrected" table
def update_corrected_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db.commit()


# add flag or edit made to particular value to "data_entries_phase1_errors" table
def add_error_edit_code(error_code, original_value, corrected_value, entry_info, add_info=''):
    entry_id = entry_info[0]
    user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_info[2:]
    sql_command = "INSERT INTO data_entries_phase1_errors " \
                  "(id, ORIGINAL_VALUE, CORRECTED_VALUE, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, additional_info) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, original_value, corrected_value, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, add_info))
    db.commit()


# add reconciled observation entry to duplicateless table (after phase 1)
def update_temp_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected_duplicateless " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db.commit()
