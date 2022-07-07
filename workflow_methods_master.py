# File in which all methods that are called upon in workflow are stored, for repurposability and modularity of code
# TODO : add error tags/codes to the value at each return statement if/when values are altered in any way

import config
import sql_commands as sql
import database_connection as db


##################### DIRECT EDITING / FIXING METHODS #####################

# references previous values in the ledger sheet(s); depending on chosen option, finds and returns previous leading digits (to use),
# or returns entire value that contains necessary leading digits
def reference_previous_values(entry, option):  # TODO : determine if 'option' is needed at all
    def modular_code_block(entry, command, step):
        if command == -1:
            return -1
        db.cursor.execute(command)
        list_entries = db.cursor.fetchall()
        list_values = [item[1] for item in list_entries]
        if step == 2 and len(list_values) == 0:
            return None

        start_index = 0
        if (step == 1) or (step == 2 and counter == 0):
            start_index = list_values.index(entry[1])
        elif step == 2 and counter > 0:
            start_index = len(list_values)

        try:
            for i in range(start_index - 1, -1, -1):
                try:
                    if (list_values[i][0:2] in config.possible_lead_digits) and (config.possible_pressure_formats(list_values[i])):
                        match option:
                            case 'leading_digits':
                                return list_values[i][0:2]
                            case 'whole_value':
                                return list_values[i]
                except TypeError:
                    pass
        except ValueError:
            pass

    result = modular_code_block(entry, sql.check_1_command(entry), 1)
    if result is not None:
        if result == -1:
            return None
        return result  # TODO : be able to return information about referenced value for pressure / phase 1 error table (using 'entry' indices)
    else:
        counter = 0
        while True:
            result = modular_code_block(entry, sql.check_2_command(entry, counter), 2)
            if result is not None:
                if result == -1:
                    return None
                return result  # TODO : be able to return information about referenced value for pressure / phase 1 error table (using 'entry' indices)
            else:
                counter += 1
                if counter > 100:
                    print('verify if loop is infinite!')


# remove any spaces present in the data entry
def remove_spaces(value):
    if ' ' in value:
        value = list(value)
        while ' ' in value:
            value.remove(' ')
        value = ''.join(value)
    return value


# remove double decimals '..' in the data entry if instance is surrounded by a digit on both sides
def correct_double_decimals(value):
    while '..' in value:
        index = value.index('..')
        if (index - 1) < 0:
            return value
        try:
            if isinstance(int(value[index - 1]), int) and isinstance(int(value[index + 2]), int):
                value = list(value)
                value.pop(index)
                value = ''.join(value)
        except ValueError:
            return value
        except IndexError:
            return value
    return value


# remove any alphabetical character in the data entry
def remove_alphabetical_char(value):
    value = list(value)
    for i in value:
        if i.isalpha():
            while i in value:
                value.remove(i)
    value = ''.join(value)
    return value


# remove any unexpected characters if they aren't surrounded by a digit on either side (adjacent or otherwise)
def remove_unexpected_characters(value):
    value = list(value)
    digit_present_right = False
    digit_present_left = False
    for i in range(len(value) - 1, -1, -1):
        if value[i] not in config.unexpected_characters:
            try:
                if (not digit_present_right) and isinstance(int(value[i]), int):
                    digit_present_right = True
                    continue
            except ValueError:
                pass
            continue
        if not digit_present_right:
            try:
                if isinstance(int(value[i]), int):
                    digit_present_right = True
            except ValueError:
                pass
        for k in value[:i]:
            try:
                if isinstance(int(k), int):
                    digit_present_left = True
                    break
            except ValueError:
                pass
        no_int_either_side = not (digit_present_left and digit_present_right)
        no_int_left_side = not digit_present_left and digit_present_right
        no_int_right_side = digit_present_left and not digit_present_right
        if no_int_either_side or no_int_left_side or no_int_right_side:
            value.pop(i)
        digit_present_left = False
    return ''.join(value)


# replacing any character in the string (index) with a decimal point
def replace_with_decimal(value, index):
    value = list(value)
    value[index] = '.'
    return ''.join(value)


# removes a set amount of trailing digits from a number (specified by 'number' parameter)
def remove_trailing_digits(value, number):
    return value[:len(value) - number]


# removes character(s) at given indices; adaptable to single index input, or a list of indices ('indices' parameter)
def remove_elements_at_indices(value, indices):
    value = list(value)
    if type(indices) == int:
        value.pop(indices)
    elif type(indices) == list:
        for i in range(len(indices)):
            j = max(indices)
            value.pop(j)
            indices.remove(j)
        return ''.join(value)


# inserts element (string character) at given index and returns new string
def insert_element_at_index(value, index, element):
    value = list(value)
    value.insert(index, element)
    return ''.join(value)


##################### CONDITIONAL STATEMENT CHECKS BELOW #####################

# local sanity check for pressure value  TODO : eventually replace this with universal method for local check, and match-case with field_id
def pressure_range(value):
    try:
        if (float(value) < config.pressure_min) or (float(value) > config.pressure_max):
            pass  # TODO : flag
    except ValueError:
        print("Format-checked value couldn't be treated as a number: " + str(value))


# Checking to see if raw pressure value is of form XX.XXX
def desired_pressure_format(value):
    try:
        float(value)
        if len(value) == 6 and float_decimal_index(value) == 2:
            return True
    except ValueError:
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
# TODO : determine later on if this needs to be coded as -999.9 ("missing value")
def disregarded_value(value):
    if value.lower() in config.disregarded_values:
        return True
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
def fluctuation_exceeds(value, entry, amount):
    sql_ref = sql.ref_prev_value(entry)
    db.cursor.execute(sql_ref)
    entries_same_day = db.cursor.fetchall()
    values_same_day = [item[1] for item in entries_same_day]
    index = values_same_day.index(value)
    try:
        if index - 1 < 0:
            return False
        if abs(float(values_same_day[index]) - float(values_same_day[index - 1])) > amount:
            return True
    except TypeError:
        return False
    except ValueError:
        return False
    except IndexError:
        return False
    return False
