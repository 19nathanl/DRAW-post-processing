# post-processing range/consistency check algorithm for post_process_id = 1 (phase 2)

import id1p2_methods as methods
import config
import tables


# check for possible transcription / observation errors, other than wrong leading digits added
def check_other_transcription_errors(value):  # TODO : add to id1p2_methods (?)
    pass


def phase_2(entry, lead_digs_added):
    return_list = [entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8], entry[9], entry[10]]
    value = return_list[1]

    if value in config.disregarded_values:
        tables.add_to_corrected_table(*return_list, 1)  # TODO : debug to see if unpacking + '1' works for updating to final table

    elif value is None:
        tables.add_to_corrected_table(*return_list, 1)  # TODO : debug to see if unpacking + '1' works for updating to final table

    if return_list[4] in {6, 7, 8}:
        diff_equation_transcribed = abs(float(value) - methods.equation_resultant_value(entry))
        if diff_equation_transcribed > config.pressure_diff_threshold:
            if lead_digs_added:
                match return_list[4]:

                    case 6:
                        try:
                            match config.possible_wrong_lead_digs_id_6(value):
                                case 'is_left':
                                    pass  # TODO : check fluctuation, don't move leading digits in right direction ONLY if fluctuation is fine
                                case 'is_right':
                                    pass  # TODO : check fluctuation, don't move leading digits in right direction ONLY if fluctuation is fine
                                case False:
                                    pass  # TODO : PASS THROUGH check_other_transcription_errors()
                        except TypeError:
                            pass  # TODO : flag ?

                    case 7:
                        try:
                            match config.possible_wrong_lead_digs_id_7(value):
                                case 'is_left':
                                    pass  # TODO : check fluctuation, don't move leading digits in right direction ONLY if fluctuation is fine
                                case 'is_right':
                                    pass  # TODO : check fluctuation, don't move leading digits in right direction ONLY if fluctuation is fine
                                case False:
                                    pass  # TODO : PASS THROUGH check_other_transcription_errors()
                        except TypeError:
                            pass  # TODO : flag ?

                    case 8:
                        try:
                            match config.possible_wrong_lead_digs_id_8(value):
                                case 'is_left':
                                    pass  # TODO : check fluctuation, don't move leading digits in right direction ONLY if fluctuation is fine
                                case 'is_right':
                                    pass  # TODO : check fluctuation, don't move leading digits in right direction ONLY if fluctuation is fine
                                case False:
                                    pass  # TODO : PASS THROUGH check_other_transcription_errors()
                        except TypeError:
                            pass  # TODO : flag ?

                    case _:
                        pass  # TODO : other field id's => (4, 67, 69)

            elif not lead_digs_added:
                pass  # TODO : add fluctuation check
                pass  # TODO : PASS THROUGH check_other_transcription_errors()
