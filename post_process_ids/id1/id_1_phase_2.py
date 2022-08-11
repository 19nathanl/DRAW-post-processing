# post-processing range/consistency check algorithm for post_process_id = 1 (phase 2)

import id1p2_methods as methods


def phase_2(entry):
    return_list = [entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8], entry[9], entry[10]]

    value = return_list[1]
    flagged = return_list[10]  # TODO : Need?
    field_id = return_list[4]  # TODO : Need?

    if flagged == 0:
        if methods.out_of_range(value, return_list[8]):
            return False  # TODO : flag
