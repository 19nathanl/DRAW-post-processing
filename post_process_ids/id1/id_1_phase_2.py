# post-processing range/consistency check algorithm for post_process_id = 1 (phase 2)

import id1p2_methods as methods
import config
import tables


def phase_2(entry, lead_digs_added):
    return_list = list(entry)
    value = return_list[1]

    if value in config.disregarded_values:
        tables.add_to_final_corrected_table(*return_list)

    elif value is None:
        tables.add_to_final_corrected_table(*return_list)

    if return_list[4] in {4, 6, 7, 8}:
        diff_equation_transcribed = abs(float(value) - methods.equation_resultant_value(entry))
        if diff_equation_transcribed >= config.pressure_diff_threshold:

            if lead_digs_added:
                methods.check_lead_digs_with_equation(diff_equation_transcribed, return_list, lead_digs_added)

            elif not lead_digs_added:
                if methods.fluctuation_exceeds_normal(return_list):
                    pass # TODO : PASS THROUGH check_other_transcription_errors()
                pass  # TODO : PASS THROUGH check_other_transcription_errors()

        elif diff_equation_transcribed < config.pressure_diff_threshold:
            pass  # TODO : for when difference is not great, but can try to pick out possible smaller errors
