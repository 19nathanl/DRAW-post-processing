import database_connection as db

import time

# Importing post_process_id = 1:
import post_process_ids.id1.f1 as f1
import post_process_ids.id1.r1 as r1


entries = db.raw_data()


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


start = time.time()
counter = 0
for row in entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 1)

    counter += 1
    print(counter)
print(time.time() - start)

# phase_1_corrected_entries = db.phase_1_corrected_data()
#
# for row in entries:
#     post_process_id = row[8]
#     filter_id(post_process_id, row, 2)
