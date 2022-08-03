# post-processing range/consistency check algorithm for post_process_id = 1

import r1_methods as methods
import f1_methods as f_methods


def r1(entry):
    return_list = [entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8], entry[9], entry[10]]

    value = return_list[1]
    flagged = return_list[10]  # TODO : Need?
    field_id = return_list[4]  # TODO : Need?

    ############### Pull from flagged values ###############

    ############### Pull from corrected, non-flagged values ###############

    if flagged == 0:
        if methods.out_of_range(value, return_list[8]):
            return False  # TODO : flag
