# File in which all methods that are called upon in pressure statistical workflow are stored, for repurposability and modularity of code

import config
import sql_commands as sql
import database_connection as db


##################### DIRECT EDITING / FIXING METHODS #####################

# returns the resultant value for field_id based on equation 1 or 2 (as indicated by equation_num), given presence of associated variables
def equation_resultant_value(entry, equation_num):
    if entry[9] is None:
        return None
    sql_command = sql.equation_retrieve_row(entry, equation_num)
    db.cursor.execute(sql_command)
    row = db.cursor.fetchall()
    if len(row) == 3:
        if any(str(item[1]).lower() in [*config.disregarded_values, 'none'] for item in row):
            return None
        row_values = []
        for transcription in row:
            row_values.append([transcription[1], transcription[4]])
        match equation_num:

            case 1:
                baro_slp = None
                atb = None
                for i in row_values:
                    if i[1] == 8:
                        baro_slp = i[0]
                    elif i[1] == 9:
                        atb = i[0]
                try:
                    bar_32 = round(float(baro_slp) * (1 - (((0.00010001*(float(atb) - 32)) - (0.000010141*(float(atb) - 62))) / (1 + 0.00010001*(float(atb) - 32)))), 3)
                    return bar_32
                except ValueError:
                    return None

            case 2:
                baro_temp_cor = None
                atb = None
                for i in row_values:
                    if i[1] == 7:
                        baro_temp_cor = i[0]
                    elif i[1] == 5:
                        atb = i[0]
                try:
                    baro_inst_cor = round(float(baro_temp_cor) / (1 - ((0.00010001*(float(atb) - 32) - 0.000010141*(float(atb) - 62)) / (1 + 0.00010001*(float(atb) - 32)))), 3)
                    return baro_inst_cor
                except ValueError:
                    return None
    else:
        return None


# in the case that a value of field_id=7 is missing leading digits, this method attempts to find them using equation 1
def equation_1_leading_digits(entry):
    resultant_value = equation_resultant_value(entry, 1)
    if resultant_value is not None:
        return str(resultant_value)[:2]
    else:
        return None


# in the case that a value of field_id=6 is missing leading digits, this method attempts to find them using equation 2
def equation_2_leading_digits(entry):
    resultant_value = equation_resultant_value(entry, 2)
    if resultant_value is not None:
        return str(resultant_value)[:2]
    else:
        return None


##################### CONDITIONAL STATEMENT CHECKS BELOW #####################

# local sanity (range) check
def out_of_range(value, post_process_id):
    minimum, maximum = None, None
    match post_process_id:
        case 1:
            minimum = config.pressure_min
            maximum = config.pressure_max
        case _:
            pass

    try:
        if (float(value) < minimum) or (float(value) > maximum):
            return True
    except ValueError:
        print("Format-checked value couldn't be treated as a number: " + str(value))
