# file where all important MySQL commands are kept

import datetime

composite_raw_data_entries = "CREATE TABLE data_entries_raw AS SELECT " \
                             \
                             "data_entries.id, " \
                             "data_entries.value, " \
                             "data_entries.user_id, " \
                             "data_entries.page_id, " \
                             "data_entries.field_id, " \
                             "fields.field_key, " \
                             "data_entries.annotation_id, " \
                             "annotations.transcription_id, " \
                             "fields.post_process_id, " \
                             "annotations.observation_date " \
                             \
                             "FROM data_entries " \
                             "LEFT JOIN fields " \
                             "ON fields.id = data_entries.field_id " \
                             "LEFT JOIN annotations " \
                             "ON data_entries.annotation_id = annotations.id;"

raw_data_sql = "SELECT * FROM data_entries_raw;"

create_duplicate_table_sql = "CREATE TABLE IF NOT EXISTS data_entries_corrected_duplicateless AS SELECT * FROM data_entries_corrected LIMIT 0;"

phase_1_data_sql = "SELECT * FROM data_entries_corrected ORDER BY post_process_id;"


# MySQL commands used in workflow method "reference_previous_values":

# retrieves entries from same annotation in method "reference_previous_values"
def check_1_command(entry):
    annotation_id = entry[6]
    return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE annotation_id = {};".format(annotation_id)


# retrieves entries from same/previous day in same relevant field group in method "reference_previous_values"
def check_2_command(entry, counter):
    try:
        observation_date = entry[9] - datetime.timedelta(days=counter)
    except TypeError:
        return -1
    field_id = entry[4]
    if field_id in [4, 6, 7]:
        return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id IN (4,6,7) " \
                                                      "AND observation_date LIKE '%{}%';".format(str(observation_date)[:10])
    if field_id == 8:
        return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id IN (4,6,7,8) " \
                                                      "AND observation_date LIKE '%{}%';".format(str(observation_date)[:10])
    if field_id in [67, 69]:
        return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id IN (67,69) " \
                                                      "AND observation_date LIKE '%{}%' ".format(str(observation_date)[:10])


# finds value for same field_id and up one row in the ledger sheet (i.e. in the previous timestamp)
def ref_prev_value(entry):
    field_id = entry[4]
    observation_date = entry[9]
    return phase_1_data_sql[:len(phase_1_data_sql) - 1] + "_duplicateless " \
                                                          "WHERE field_id = {} " \
                                                          "AND observation_date LIKE '%{}%';".format(field_id, str(observation_date)[:10])


# retrieves relevant field_id's in ledger sheet, to calculate particular field_id based on other two elements, using equation 1, 2 oe 3
def equation_retrieve_row(entry, equation_num):
    field_ids = None
    match equation_num:
        case 1:
            field_ids = (4, 5, 6)  # to find field_id = 7
        case 2:
            field_ids = (4, 6, 7, 9, 10)  # to find field_id = 8
        case 3:
            field_ids = (5, 7)  # to find field_id = 6
    user_id = entry[2]
    observation_date = str(entry[9])
    return "SELECT * FROM data_entries_corrected " \
           "WHERE observation_date = '{}' " \
           "AND field_id IN {} " \
           "AND user_id = {};".format(observation_date, field_ids, user_id)
