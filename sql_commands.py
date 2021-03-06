# file where all MySQL commands are kept
import datetime


raw_data_sql = "SELECT * FROM data_entries_raw;"

phase_1_data_sql = "SELECT * FROM data_entries_corrected;"


# MySQL commands used in workflow method "reference_previous_values":

# retrieves entries from same annotation
def check_1_command(entry):
    annotation_id = entry[6]
    return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE annotation_id = {};".format(annotation_id)


# retrieves entries from same/previous day in same relevant field group
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
    user_id = entry[2]
    field_id = entry[4]
    observation_date = entry[9]
    return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id = {} " \
                                                  "AND observation_date LIKE '%{}%' " \
                                                  "AND user_id = {};".format(field_id, str(observation_date)[:10], user_id)


# retrieves relevant field_id's in ledger sheet, to calculate particular field_id based on other two elements, using equation 1 (or) 2
def equation_retrieve_row(entry, equation_num):
    field_ids = None
    match equation_num:
        case 1:
            field_ids = (4, 5, 6)  # to find field_id = 7
        case 2:
            field_ids = (4, 5, 6, 9, 10)  # to find field_id = 8
    user_id = entry[2]
    observation_date = str(entry[9])
    return "SELECT * FROM data_entries_corrected " \
           "WHERE observation_date = '{}' " \
           "AND field_id IN {} " \
           "AND user_id = {};".format(observation_date, field_ids, user_id)
