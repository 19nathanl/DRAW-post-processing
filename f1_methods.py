# File in which all methods that are called upon in pressure format workflow are stored, for repurposability and modularity of code

import config
import sql_commands as sql
import database_connection as db
import tables


##################### DIRECT EDITING / FIXING METHODS #####################

# references previous values in the ledger sheet(s); depending on chosen option, finds and returns previous leading digits (to use),
# or returns entire value that contains necessary leading digits
def reference_previous_values(entry, option):
    def modular_code_block(entry, command, step):
        if command == -1:
            return -1, None
        db.cursor.execute(command)
        list_entries = db.cursor.fetchall()
        list_values = [item[1] for item in list_entries]
        if step == 2 and len(list_values) == 0:
            return -1, None

        start_index = 0
        if (step == 1) or (step == 2 and counter == 0):
            for i in list_entries:
                if i[0] == entry[0]:
                    break
                start_index += 1
        elif step == 2 and counter > 0:
            start_index = len(list_values)

        try:
            for i in range(start_index - 1, -1, -1):
                try:
                    if (list_values[i][0:2] in config.possible_lead_digits_pressure) and (config.possible_pressure_formats(list_values[i])):
                        match option:
                            case 'leading_digits':
                                ref_info = list_entries[i]
                                return list_values[i][0:2], [ref_info[0], ref_info[1], ref_info[9]]  # ref. value , information about ref. value
                            case 'whole_value':
                                return list_values[i]
                except TypeError:
                    return None, None
            return None, None
        except ValueError:
            return None, None

    result, info = modular_code_block(entry, sql.check_1_command(entry), 1)
    if result is not None:
        if result == -1:
            return None, None
        return result, info
    else:
        counter = 0
        while True:
            result, info = modular_code_block(entry, sql.check_2_command(entry, counter), 2)
            if result is not None:
                if result == -1:
                    return None, None
                return result, info
            else:
                counter += 1
                if counter > 25:
                    print('verify if loop is infinite!')
                    return None, None


# remove any spaces present in the data entry
def remove_spaces(value, entry):
    if ' ' in value:
        original_value = value
        value = list(value)
        while ' ' in value:
            value.remove(' ')
        value = ''.join(value)
        tables.add_error_edit_code('101', original_value, value, entry)
    return value


# remove double decimals '..' in the data entry if instance is surrounded by a digit on both sides
def correct_double_decimals(value, entry):
    while '..' in value:
        original_value = value
        index = value.index('..')
        if (index - 1) < 0:
            return value
        try:
            if isinstance(int(value[index - 1]), int) and isinstance(int(value[index + 2]), int):
                value = list(value)
                value.pop(index)
                value = ''.join(value)
                tables.add_error_edit_code('102', original_value, value, entry)
        except ValueError:
            return value
        except IndexError:
            return value
    return value


# remove any alphabetical character in the data entry
def remove_alphabetical_char(value, entry):
    if any(char.isalpha() for char in value):
        original_value = value
        value = list(value)
        for i in value:
            if i.isalpha():
                while i in value:
                    value.remove(i)
        value = ''.join(value)
        tables.add_error_edit_code('103', original_value, value, entry)
    return value


# remove any unexpected characters if they aren't surrounded by a digit on either side (adjacent or otherwise)
def remove_unexpected_characters(value, entry):
    try:
        if (len(value) >= 9 and ',' in value) or (value[0] == '.' and isinstance(int(value[1:]), int)) or (value[len(value) - 1] == '.' and isinstance(int(value[:len(value) - 1]), int)):
            return value
    except ValueError:
        pass
    original_value = value
    value = list(value)
    digit_present_right = False
    digit_present_left = False
    for i in range(len(value) - 1, -1, -1):
        if not digit_present_right:
            if any(char.isdigit() for char in value[i + 1:]):
                digit_present_right = True

        digit_present_left = any(char.isdigit() for char in value[:i])

        if value[i] in config.unexpected_characters:
            if digit_present_left and digit_present_right:
                digit_present_left = False
                continue
            elif (digit_present_left and not digit_present_right) or (not digit_present_left and digit_present_right) or (not digit_present_left and not digit_present_right):
                value.pop(i)

        digit_present_left = False

    value = ''.join(value)
    if value != original_value:
        tables.add_error_edit_code('104', original_value, value, entry)
    return value


# replacing any character in the string (index) with a decimal point
def replace_with_decimal(value, index, entry):
    original_value = value
    value = list(value)
    value[index] = '.'
    value = ''.join(value)
    tables.add_error_edit_code('108', original_value, value, entry)
    return value


# removes a set amount of trailing digits from a number (specified by 'number' parameter)
def remove_trailing_digits(value, number, entry):
    original_value = value
    value = value[:len(value) - number]
    tables.add_error_edit_code('114', original_value, value, entry)
    return value


# removes character(s) at given indices; adaptable to single index input, or a list of indices ('indices' parameter)
def remove_elements_at_indices(value, indices, entry):
    original_value = value
    value = list(value)
    if type(indices) == int:
        value.pop(indices)
        value = ''.join(value)
        tables.add_error_edit_code('109', original_value, value, entry)
        return value
    elif type(indices) == list:
        for i in range(len(indices)):
            j = max(indices)
            value.pop(j)
            indices.remove(j)
        value = ''.join(value)
        tables.add_error_edit_code('109', original_value, value, entry)
        return ''.join(value)


# inserts element (string character) at given index and returns new string
def insert_element_at_index(value, index, element, entry):
    original_value = value
    value = list(value)
    value.insert(index, element)
    value = ''.join(value)
    tables.add_error_edit_code('106', original_value, value, entry)
    return value


##################### CONDITIONAL STATEMENT CHECKS BELOW #####################

# Checking to see if raw pressure value is of form XX.XXX
def desired_pressure_format(value):
    try:
        float(value)
        if len(value) == 6 and float_decimal_index(value) == 2:
            return True
    except ValueError:
        return False
    except TypeError:
        return False
    return False


# returns True if value is of form XX XXX where the space is one of ( '/'  ';'  ','  '-' )
def pressure_decimal_alternate(value):
    try:
        if isinstance(int(value[:2]), int) and isinstance(int(value[3:]), int) and (value[2] in config.decimal_point_alternates):
            return True
    except ValueError:
        return False
    return False


# identifying values that can be disregarded (e.g. 'blank', 'retracted')
def disregarded_value(value):
    try:
        if value.lower() in config.disregarded_values:
            return True
    except AttributeError:
        return False
    return False


# returns index at which decimal point is placed if value is a float (composed of n-1 digits + one decimal point), otherwise returns False
def float_decimal_index(value):
    try:
        float(value)
        if '.' in value:
            return value.index('.')
    except ValueError:
        return False
    return False


# return True if value of form +XXX or -XXX (pressure values)
def removable_plus_minus(value):
    try:
        if isinstance(int(value[1:]), int) and value[0] in ['-', '+']:
            return True
        return False
    except ValueError:
        return False


# checks if value for particular field has fluctuated by more than 'amount' specified by parameter since previous timestamp on the same day
# TODO : repurpose this for phase 2 ******
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
        if index - 1 < 0:
            return False
        if abs(float(value) - float(values_same_day[index - 1])) > amount:
            ref_value = entries_same_day[index - 1]
            ref_info = [ref_value[0], ref_value[1], ref_value[9]]
            tables.add_error_edit_code('020', value, '', entry, 'Ref. entry ID: {}, '
                                                                'Value: {}, '
                                                                'Datetime of reference: {}'.format(*ref_info))
            return True
    except TypeError:
        return False
    except ValueError:
        return False
    except IndexError:
        return False
    return False
