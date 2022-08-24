import database_connection as db
import tables
import observation_reconciliation as reconcile
import remove_low_transcription_users as remove_ltu
import mysql_indexes
import setup_raw_data_table as setup

# Importing post_process_id = 1:
import post_process_ids.id1.id_1_phase_1 as id1p1
import post_process_ids.id1.id_1_phase_2 as id1p2
import post_process_ids.id1.id_1_outliers as id1outliers
import id1p2_methods

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
                    if entry[0] in pressure_lead_digs_added:
                        id1p2.phase_2(entry, True)
                    else:
                        id1p2.phase_2(entry, False)
                case 2:
                    pass
        # outlier removal
        case 'outlier_removal':
            match pp_id:
                case 1:
                    return id1outliers.patch_outlier(entry)
                case 2:
                    pass


#####################       TAKE IN RAW DATA AND CREATE "raw_data_entries" TABLE       ########################################
setup.set_up_raw_data_table()
mysql_indexes.data_entries_raw('user', 'create')


#####################       REMOVE ENTRIES FROM USERS WITH LESS THAN 100 TOTAL TRANSCRIBED ENTRIES       ######################
remove_ltu.delete_transcriptions()
mysql_indexes.data_entries_raw('user', 'delete')

#####################       EXECUTE PHASE 1 (FORMAT CHECKING/CLEANING)       ##################################################
mysql_indexes.data_entries_raw('annotation', 'create')
mysql_indexes.data_entries_raw('field_date', 'create')
raw_entries = db.raw_data()
tables.create_corrected_data_table()
tables.create_error_edit_table(1)

counter = 0
for row in raw_entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 1)
    counter += 1
    print('Phase 1 :', counter)


#####################       RECONCILE VALUES FOR SAME OBSERVATION (FIELD + DATETIME)       ####################################
mysql_indexes.data_entries_corrected('field_date_user', 'create')
tables.create_duplicateless_table()
reconcile.remove_duplicates()
mysql_indexes.data_entries_corrected_duplicateless('field_date', 'create')


#####################       EXECUTE PHASE 2 (REMOVE OUTLIERS + STATISTICAL/VALIDATION CHECKING)       #########################
entries = db.phase_1_data()
tables.create_final_corrected_table()
tables.create_error_edit_table(2)

for index in range(len(entries)):
    row_list = list(entries[index])
    post_process_id = row_list[8]
    outlier_fixed = filter_id(post_process_id, row_list, 'outlier_removal')
    if outlier_fixed is not None:
        row_list[1] = outlier_fixed
    row = tuple(row_list)
    entries[index] = row


pressure_lead_digs_added = id1p2_methods.pressure_artificial_lead_digs_list()

for row in entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 2)


#####################       DELETE ALL DISPENSABLE TABLES (KEEP FINAL + ERRORS/EDITS TABLES)       ############################
tables.delete_table('data_entries_raw')
tables.delete_table('data_entries_corrected')
tables.delete_table('data_entries_corrected_duplicateless')
