# File in which all methods that are called upon in pressure statistical workflow are stored, for repurposability and modularity of code

import config
import sql_commands as sql
import database_connection as db


##################### DIRECT EDITING / FIXING METHODS #####################

# checks if value for particular field has fluctuated by more than 'amount' specified by parameter since previous timestamp on the same day TODO : finalize for phase 2
def fluctuation_exceeds(value, entry, amount):
    sql_ref = sql.ref_prev_value(entry)
    db.cursor.execute(sql_ref)
    entries_same_day = db.cursor.fetchall()
    values_same_day = [item[1] for item in entries_same_day]
    index = 0
    for i in entries_same_day:
        if i[0] == entry[0]:
            break
        index += 1
    try:
        pass
        # if index - 1 < 0:
        #     return False
        # if abs(float(value) - float(values_same_day[index - 1])) > amount:
        #     ref_value = entries_same_day[index - 1]
        #     ref_info = [ref_value[0], ref_value[1], ref_value[9]]
        #     tables.add_error_edit_code('020', value, '', entry, 'Ref. entry ID: {}, '
        #                                                         'Value: {}, '
        #                                                         'Datetime of reference: {}'.format(*ref_info))
        #     return True
    except TypeError:
        return False
    except ValueError:
        return False
    except IndexError:
        return False
    return False



def pressure_change_temporal_scalar(entry):
    pass


# returns the resultant value for field_id based on equation 1 or 2 (as indicated by equation_num), given presence of associated variables
def equation_resultant_value(entry):
    if entry[9] is None:
        return None
    equation_num = 0
    match entry[4]:
        case 6:
            equation_num = 3
        case 7:
            equation_num = 1
        case 8:
            equation_num = 2
    sql_command = sql.equation_retrieve_row(entry, equation_num)
    db.cursor.execute(sql_command)
    row = db.cursor.fetchall()
    # remove any values in row that are in disregarded values are None:
    for i in range(len(row) - 1, -1, -1):
        if str(row[i][1]).lower() in [*config.disregarded_values, 'none']:
            row.pop(i)
    if len(row) < 2:
        return None
    row_values = []
    for transcription in row:
        row_values.append([transcription[1], transcription[4]])
    non_dupl_row_values = []
    for i in row_values:
        if i not in non_dupl_row_values:
            non_dupl_row_values.append(i)
    match equation_num:

        case 1:
            field_ids = [item[1] for item in non_dupl_row_values]
            field_ids_sorted = sorted(field_ids)

            match field_ids_sorted:
                case [5, 6]:
                    atb = [item[0] for item in non_dupl_row_values if item[1] == 5][0]
                    baro_inst_cor = [item[0] for item in non_dupl_row_values if item[1] == 6][0]
                case [4, 5]:
                    atb = [item[0] for item in non_dupl_row_values if item[1] == 5][0]
                    baro_inst_cor = [item[0] for item in non_dupl_row_values if item[1] == 4][0]
                case [4, 6]:
                    return None
                case [4, 5, 6]:
                    atb = [item[0] for item in non_dupl_row_values if item[1] == 5][0]
                    baro_inst_cor = [item[0] for item in non_dupl_row_values if item[1] == 6][0]
                case _:
                    return None
            try:
                baro_32 = round(float(baro_inst_cor) * (1 - ((0.000101*(float(atb) - 32) - 0.0000102*(float(atb) - 62)) / (1 + 0.000101*(float(atb) - 32)))), 3)
                return baro_32
            except ValueError:
                return None

        case 2:
            field_ids = [item[1] for item in non_dupl_row_values]
            field_ids_sorted = sorted(field_ids)

            baro_inst_cor_list = [True for item in field_ids_sorted if item in [4, 6]]
            if True in baro_inst_cor_list:
                if len(baro_inst_cor_list) == 2:
                    try:
                        baro_inst_cor = [item[0] for item in non_dupl_row_values if item[1] == 6][0]
                    except IndexError:
                        baro_inst_cor = [item[0] for item in non_dupl_row_values if item[1] == 4][0]
                else:
                    baro_inst_cor = [item[0] for item in non_dupl_row_values if (item[1] == 6 or item[1] == 4)][0]
            else:
                return None
            temp_air_list = [True for item in field_ids_sorted if item in [9, 10]]
            if True in temp_air_list:
                if len(temp_air_list) == 2:
                    try:
                        temp_air = [item[0] for item in non_dupl_row_values if item[1] == 10][0]
                    except IndexError:
                        temp_air = [item[0] for item in non_dupl_row_values if item[1] == 9][0]
                else:
                    temp_air = [item[0] for item in non_dupl_row_values if (item[1] == 10 or item[1] == 9)][0]
            else:
                return None
            baro_32_list = [True for item in field_ids_sorted if item == 7]
            if True in baro_32_list:
                baro_32 = [item[0] for item in non_dupl_row_values if item[1] == 7][0]
            else:
                return None
            try:
                m = 187 / (56573 + 123.1*float(temp_air) + 0.003*187)
                baro_slp = round(float(baro_32) + float(baro_inst_cor)*((10**m) - 1), 3)
                return baro_slp
            except ValueError:
                return None

        case 3:
            field_ids = [item[1] for item in non_dupl_row_values]
            field_ids_sorted = sorted(field_ids)

            match field_ids_sorted:
                case [5, 7]:
                    atb = [item[0] for item in non_dupl_row_values if item[1] == 5][0]
                    baro_32 = [item[0] for item in non_dupl_row_values if item[1] == 7][0]
                case _:
                    return None
            try:
                (1 - ((0.000101 * (float(atb) - 32) - 0.0000102 * (float(atb) - 62)) / (1 + 0.000101 * (float(atb) - 32))))
                baro_inst_cor = round(float(baro_32) / (1 - ((0.000101 * (float(atb) - 32) - 0.0000102 * (float(atb) - 62)) / (1 + 0.000101 * (float(atb) - 32)))), 3)
                return baro_inst_cor
            except ValueError:
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
