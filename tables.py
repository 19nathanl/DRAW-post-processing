import database_connection as db


# update value to "pressure_entries_phase1_corrected" table, adjusted for phase 1 checks
def update_corrected_table_phase1(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO pressure_entries_corrected " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    db.cursor.execute(sql_command, (id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db.db.commit()


# update "pressure_entries_phase1_errors" table with flag or edit made to particular value
def add_error_edit_code(error_code, original_value, corrected_value, entry_info, add_info=''):
    id = entry_info[0]
    user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_info[2:]
    sql_command = "INSERT INTO pressure_entries_phase1_errors " \
                  "(id, ORIGINAL_VALUE, CORRECTED_VALUE, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, additional_info) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    db.cursor.execute(sql_command, (id, original_value, corrected_value, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, add_info))
    db.db.commit()
