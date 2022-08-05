import database_connection as db


# update value to "data_entries_corrected" table
def update_corrected_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    db.cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db.db.commit()


# add flag or edit made to particular value to "data_entries_phase1_errors" table
def add_error_edit_code(error_code, original_value, corrected_value, entry_info, add_info=''):
    entry_id = entry_info[0]
    user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_info[2:]
    sql_command = "INSERT INTO data_entries_phase1_errors " \
                  "(id, ORIGINAL_VALUE, CORRECTED_VALUE, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, additional_info) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    db.cursor.execute(sql_command, (entry_id, original_value, corrected_value, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, add_info))
    db.db.commit()
