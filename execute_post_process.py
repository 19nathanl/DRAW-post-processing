import database_connection as db
import tables
import create_raw_data_table as raw_data
import observation_reconciliation as reconcile
import remove_low_transcription_users as remove_ltu
import outlier_remediation

# Importing post_process_id = 1:
import post_process_ids.id1.id_1_phase_1 as id1p1
import post_process_ids.id1.id_1_phase_2 as id1p2

db = db.db
cursor = db.cursor()


# point data entry to particular post_processing algorithm for phase 1 depending on its post_process_id
def filter_id(pp_id, entry, phase):
    match phase:
        # phase 1
        case 1:
            match pp_id:
                case 1:
                    id1p1.phase_1(entry)
                case 2:
                    pass
        # phase 2
        case 2:
            match pp_id:
                case 1:
                    id1p2.phase_2(entry)
                case 2:
                    pass


#####################       TAKE IN RAW DATA AND CREATE "raw_data_entries" TABLE       ########################################
raw_data.create_raw_data_entries()
# TODO : add relevant indexes in this file


#####################       REMOVE ENTRIES FROM USERS WITH LESS THAN 100 TOTAL TRANSCRIBED ENTRIES       ######################
remove_ltu.delete_transcriptions()


#####################       EXECUTE PHASE 1 (FORMAT CHECKING/CLEANING)       ##################################################
raw_entries = db.raw_data()
tables.create_corrected_data_table()
# TODO : create error / edit table for phase 1

for row in raw_entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 1)


#####################       RECONCILE VALUES FOR SAME OBSERVATION (FIELD + DATETIME)       ####################################
reconcile.remove_duplicates()


#####################       EXECUTE PHASE 2 (REMOVE OUTLIERS + STATISTICAL/VALIDATION CHECKING)       #########################
entries = db.phase_1_data()
tables.create_final_corrected_table()
# TODO : create error / edit table for phase 2

for row in entries:
    row_list = list(row)
    outlier_fixed = outlier_remediation.patch_outlier(row_list)
    if outlier_fixed is not None:
        row_list[1] = outlier_fixed
    row = tuple(row_list)


for row in entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 2)
