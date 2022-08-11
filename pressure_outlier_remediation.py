# This file is used to direct each entry to its own outlier-fixing algorithm, based on its post_process_id

import config
import database_connection as db
import id1p2_methods as r1

# TODO : add this as a function in r1_methods for phase 2

db = db.db
cursor = db.cursor()

retrieve_outliers = "SELECT * FROM data_entries_corrected_duplicateless " \
                    "WHERE field_id IN (4,6,7,8,67,69);"
cursor.execute(retrieve_outliers)
results = cursor.fetchall()

counter = 0
outliers = []
for result in results:
    value = result[1]
    try:
        if str(value).lower() not in tuple(config.disregarded_values) and (float(value) < 27 or float(value) > 33) and result[10] == 0:
            outliers.append(result)
    except TypeError:
        pass
    except ValueError:
        pass
    counter += 1
    print(counter)

for outlier in outliers:
    print(list(outlier[:8]), str(outlier[9]))


def patch_outlier(entry):
    match entry[8]:
        case 1:
            pass
