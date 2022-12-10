# This file fixes outliers for pressure values before moving on to next part of phase 2

import config
import tables


def patch_outlier(entry):
    value = entry[1]
    try:
        if str(value).lower() not in [*config.disregarded_values, 'none'] and (float(value) < config.pressure_min or float(value) > config.pressure_max) and entry[10] == 0:
            if value[1] == '9' and value[0] != '2':
                original_value = value
                value = list(value)
                value[0] = '2'
                value = ''.join(value)
                tables.update_duplicateless_table(value, entry[0])
                tables.add_error_edit_code(2, '121', original_value, value, entry)
                return value
            elif value[1] == '0' and value[0] != '3':
                original_value = value
                value = list(value)
                value[0] = '3'
                value = ''.join(value)
                tables.update_duplicateless_table(value, entry[0])
                tables.add_error_edit_code(2, '121', original_value, value, entry)
                return value
            elif value[:2] == '24':
                original_value = value
                value = list(value)
                value[1] = '9'
                value = ''.join(value)
                tables.update_duplicateless_table(value, entry[0])
                tables.add_error_edit_code(2, '121', original_value, value, entry)
                return value
            elif value[:2] == '34':
                original_value = value
                value = list(value)
                value.pop(1)
                value[0] = '29'
                value = ''.join(value)
                tables.update_duplicateless_table(value, entry[0])
                tables.add_error_edit_code(2, '121', original_value, value, entry)
                return value
            elif value[:2] == '74':
                original_value = value
                value = list(value)
                value.pop(1)
                value[0] = '29'
                value = ''.join(value)
                tables.update_duplicateless_table(value, entry[0])
                tables.add_error_edit_code(2, '121', original_value, value, entry)
                return value
            elif value[:2] == '26':
                original_value = value
                value = list(value)
                value[1] = '9'
                value = ''.join(value)
                tables.update_duplicateless_table(value, entry[0])
                tables.add_error_edit_code(2, '121', original_value, value, entry)
                return value

        else:
            return None
    except TypeError:
        pass
    except ValueError:
        pass
