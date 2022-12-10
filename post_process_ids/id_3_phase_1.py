# post-processing format check algorithm for post_process_id = 3

import tables


def phase_1(entry):
    return_list = list(entry)
    value = entry[1]

