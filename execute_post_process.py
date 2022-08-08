import database_connection as db
import create_raw_data_table as raw_data
import observation_reconciliation as reconcile


# Importing post_process_id = 1:
import post_process_ids.id1.f1 as f1
import post_process_ids.id1.r1 as r1

db = db.db
cursor = db.cursor()


# point data entry to particular post_processing algorithm for phase 1 depending on its post_process_id
def filter_id(post_process_id, entry, phase):
    match phase:
        # phase 1
        case 1:
            match post_process_id:
                case 1:
                    f1.f1(entry)
                case 2:
                    pass
        # phase 2
        case 2:
            match post_process_id:
                case 1:
                    r1.r1(entry)
                case 2:
                    pass


#####################       TAKE IN RAW DATA AND CREATE "raw_data_entries" TABLE;       ######################################
raw_data.create_raw_data_entries()
# TODO : write code to create indexes IF not already existent (as listed in 'Documentation' doc) for 'raw_data_entries' for faster querying in section below


#####################       REMOVE ENTRIES FROM USERS WITH LESS THAN 100 TOTAL TRANSCRIBED ENTRIES       #####################
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()

threshold = 100
less_than_threshold_users = []
for i in users:
    user_id = i[0]
    sql_command = "SELECT COUNT(*) from data_entries_raw " \
                  "WHERE user_id = {};".format(user_id)
    cursor.execute(sql_command)
    num = cursor.fetchall()[0][0]
    if num < threshold:
        less_than_threshold_users.append(user_id)

delete_transcriptions_sql = "DELETE FROM data_entries_raw WHERE user_id IN {};".format(tuple(less_than_threshold_users))


#####################       EXECUTE PHASE 1 (FORMAT CHECKING/CLEANING)       #################################################
raw_entries = db.raw_data()

for row in raw_entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 1)


#####################       RECONCILE VALUES FOR SAME OBSERVATION (FIELD + DATETIME)       ###################################
reconcile.remove_duplicates()


#####################       EXECUTE PHASE 2 (STATISTICAL/VALIDATION CHECKING)       ##########################################
# TODO : finish designing and writing code for phase 2

phase_1_entries = db.phase_1_data()

for row in phase_1_entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 2)
