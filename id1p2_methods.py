# File in which all methods that are called upon in pressure statistical workflow are stored, for repurposability and modularity of code

import config
import sql_commands as sql
import database_connection as db
import datetime

db = db.db
cursor = db.cursor()


def fluctuation_exceeds_normal(entry):
    # way to structure the above: go back previously first and iterate for each value to check if it's acceptable; THEN do the same for subsequent values
    # => ensure (FIRST) if there is a value before / after the one we're analyzing in the returned list, (SECOND) that it's of acceptable pressure format,
    # (THIRD) if it's not 12 hours away => if values stray further away from 12 hours at that point, ignore that side of the fluctuation and do not let it
    # influence outcome (i.e. just have outcome be based on the other side); if both sides are unsuitable, return result that does not influence outcome;
    # i.e. the program would assume that the fluctuation check confirmed that it was bad

    def step_through_adjacent_day(entry_list, which_side):
        sql_command = None
        match which_side:
            case 'previous':
                sql_command = sql.ref_adjacent_fluctuations(entry, entry[9] - datetime.timedelta(days=1))
            case 'subsequent':
                sql_command = sql.ref_adjacent_fluctuations(entry, entry[9] + datetime.timedelta(days=1))
        cursor.execute(sql_command)
        adjacent_day_entries = cursor.fetchall()
        iter_direction = None
        match which_side:
            case 'previous':
                iter_direction = range(len(adjacent_day_entries) - 1, -1, -1)
            case 'subsequent':
                iter_direction = range(len(adjacent_day_entries))
        for index in iter_direction:
            if adjacent_day_entries[index][9] is not None:
                time_delta_2 = abs(((entry[9].timestamp() - adjacent_day_entries[index][9].timestamp()) / 3600))
                if time_delta_2 < config.time_delta_limit:
                    try:
                        if config.possible_pressure_formats(adjacent_day_entries[index][1], False):
                            scalar_value = abs(float(entry_list[1]) - float(adjacent_day_entries[index][1])) / time_delta_2
                            if scalar_value > config.scalar_fluctuation_thresholds[str(entry_list[9])[5:7]]:
                                return True
                            else:
                                return False
                    except TypeError:
                        return None
                else:
                    return None
        return None

    def step_through_same_day(entry_list, bef_or_aft):
        counter = None
        index_limit_condition = None
        which_side = None
        match bef_or_aft:
            case 'before':
                counter = -1
                index_limit_condition = -1
                which_side = 'previous'
            case 'after':
                counter = +1
                index_limit_condition = len(entries)
                which_side = 'subsequent'

        while True:
            if entry_index + counter == index_limit_condition:
                return step_through_adjacent_day(entry_list, which_side)
            time_delta_1 = abs(((entry[9].timestamp() - entries[entry_index + counter][9].timestamp()) / 3600))
            if time_delta_1 > 12:
                return None
            try:
                if config.possible_pressure_formats(entries[entry_index + counter][1], False):
                    scalar = abs(float(entry[1]) - float(entries[entry_index + counter][1])) / time_delta_1
                    if scalar > config.scalar_fluctuation_thresholds[str(entry[9])[5:7]]:
                        return True
                    else:
                        return False
            except TypeError:
                counter += counter
                continue
            counter += counter

    if entry[9] is not None:
        sql_ref_same_day = sql.ref_adjacent_fluctuations(entry, entry[9])
        cursor.execute(sql_ref_same_day)
        entries = cursor.fetchall()
        entry_index = entries.index(entry)

        left_scalar_exceeds_limit = step_through_same_day(entry, 'before')
        right_scalar_exceeds_limit = step_through_same_day(entry, 'after')

        # "None" => couldn't conclude that fluctuation didn't exceed (non-influence)  TODO : figure out conditionals once each side is determined:
        if left_scalar_exceeds_limit and right_scalar_exceeds_limit:
            return True


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


# returns list of id's corresponding to values whose leading digits have been added artificially in phase 1
def pressure_artificial_lead_digs_list():
    cursor.execute("SELECT * FROM data_entries_phase1_errors "
                   "WHERE error_code IN (110,115);")
    return set([item[0] for item in cursor.fetchall()])
