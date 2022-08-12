# This file is used to direct each entry to its own outlier-fixing algorithm (if applicable), based on its post_process_id

import post_process_ids.id1.id_1_outliers as id_1_outliers


def patch_outlier(entry):
    match entry[8]:
        case 1:
            return id_1_outliers.patch_outlier(entry)
        case 2:
            pass
        case 3:
            pass
