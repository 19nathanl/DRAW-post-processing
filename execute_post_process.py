import database_connection as db

# Importing post_process_id = 1:
import post_process_ids.id1.f1 as f1
import post_process_ids.id1.r1 as r1


entries = db.db_data()


# point data entry to particular post_processing algorithm depending on its post_process_ids
def filter_by_id(post_process_id, entry):

    # filter each data_entry by its post_process_id to its own algorithm
    match post_process_id:
        case 1:
            f1.f1(entry)
            # range_consistency_checked_value = r1.r1(entry)
            # then update corrected table with this new value above

        case 2:
            pass
        case 3:
            pass
        case 4:
            pass


for row in entries:
    post_process_id = row[8]
    filter_by_id(post_process_id, row)
