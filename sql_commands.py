# file where all MySQL commands are kept
import datetime

main_command = "SELECT " \
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
                  "ON pressure_entries.annotation_id = annotations.id;"


# MySQL commands used in workflow method "reference_previous_values":

# retrieve entries from same annotation
def check_1_command(entry):
    annotation_id = entry[6]
    return main_command[:len(main_command) - 1] + " WHERE annotation_id = {};".format(annotation_id)


# retrieve entries from same/previous day in same relevant field group
def check_2_command(entry, counter):
    try:
        observation_date = entry[9] - datetime.timedelta(days=counter)
    except TypeError:
        return -1
    field_id = entry[4]
    if field_id in [4, 6, 7]:
        return main_command[:len(main_command) - 1] + " WHERE field_id IN (4,6,7) " \
                                                        "AND observation_date LIKE '%{}%';".format(str(observation_date)[:10])
    if field_id == 8:
        return main_command[:len(main_command) - 1] + " WHERE field_id IN (4,6,7,8) " \
                                                      "AND observation_date LIKE '%{}%';".format(str(observation_date)[:10])
    if field_id in [67, 69]:
        return main_command[:len(main_command) - 1] + " WHERE field_id IN (67,69) " \
                                                        "AND observation_date LIKE '%{}%' ".format(str(observation_date)[:10])
