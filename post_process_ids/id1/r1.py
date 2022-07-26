# post-processing range/consistency check algorithm for post_process_id = 1

import r1_methods as methods
import f1_methods as f_methods


def r1(entry):
    return_list = [entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8], entry[9], entry[10]]

    value = return_list[1]
    flagged = return_list[10]
    field_id = return_list[4]

    ############### Pull from flagged values ###############

    if flagged == 1:
        # checking if field_id = 7 and if value is like '.XXX' or 'XXX', for possibility of retrieving leading digits from equations
        if field_id == 7 and ((f_methods.float_decimal_index(value) == 0 and len(value) == 4) or (value.isnumeric() and len(entry[1]) == 3)):
            leading_digits = methods.equation_1_leading_digits(return_list)
            if leading_digits is not None:
                new_value = list(value)  # change to value
                new_value.insert(0, leading_digits)  # change to value
                return_list[1] = ''.join(new_value)  # change to value
                return return_list[1]
            else:
                pass

    ############### Pull from corrected, non-flagged values ###############

    elif flagged == 0:
        if methods.out_of_range(value, return_list[8]):
            return False  # TODO : flag
