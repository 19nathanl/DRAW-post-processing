# file where all MySQL commands are kept
import datetime

test_raw_data_sql = "SELECT " \
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
                  "annotations.observation_date " \
                  \
                  "FROM pressure_entries " \
                  "LEFT JOIN fields " \
                  "ON fields.id = pressure_entries.field_id " \
                  "LEFT JOIN annotations " \
                  "ON pressure_entries.annotation_id = annotations.id " \
                  "WHERE value LIKE '___';"

raw_data_sql = "SELECT " \
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
                  "annotations.observation_date " \
                  \
                  "FROM pressure_entries " \
                  "LEFT JOIN fields " \
                  "ON fields.id = pressure_entries.field_id " \
                  "LEFT JOIN annotations " \
                  "ON pressure_entries.annotation_id = annotations.id;"

phase_1_corrected_data_sql = "SELECT * FROM pressure_entries_corrected;"


# MySQL commands used in workflow method "reference_previous_values":

# retrieve entries from same annotation
def check_1_command(entry):
    annotation_id = entry[6]
    return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE annotation_id = {};".format(annotation_id)


# retrieve entries from same/previous day in same relevant field group
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


# MySQL command to find value for same field_id and up one row in the ledger sheet (i.e. in the previous timestamp)
def ref_prev_value(entry):
    user_id = entry[2]
    field_id = entry[4]
    observation_date = entry[9]
    return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id = {} " \
                                                  "AND observation_date LIKE '%{}%' " \
                                                  "AND user_id = {};".format(field_id, str(observation_date)[:10], user_id)
