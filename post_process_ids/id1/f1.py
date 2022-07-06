# post-processing format check algorithm for post_process_id = 1

import workflow_methods_master as methods


def f1(entry):
    value = entry[1]

    # Checking to see if raw pressure value is already of form XX.XXX
    if methods.desired_pressure_format(value):
        return entry

    elif methods.disregarded_value(value):
        pass  # TODO : flag system/updating corrected table with disregarded value as is (?) add else statement if this block doesn't break loop

    # if not of the right form initially, corrects format and returns entry with corrected value
    else:
        value = methods.remove_spaces(value)
        value = methods.correct_double_decimals(value)
        value = methods.remove_alphabetical_char(value)
        value = methods.remove_unexpected_characters(value)

        # checking again if pressure value is of form XX.XXX after simple clean-up methods
        if methods.desired_pressure_format(value):
            entry[1] = value
            return entry

        # TODO : 'Illegible' entries
        # TODO : Add 'else' conditions to all code blocks below to make sure that all entries are accounted for
        # TODO : return all values as **floats** so they can be processed as necessary in phase 2

        if len(value) == 5:
            if value.isnumeric():
                entry[1] = float(value) / 1000  # TODO : return entry
            # checking and fixing accordingly if pressure value of form 0.XXX, 2.XXX, or 3.XXX
            elif methods.float_decimal_index(value) == 1:
                match int(value[0]):
                    case 2:
                        value = methods.insert_element_at_index(value, 1, '9')
                        pass  # TODO : return entry
                    case 3:
                        value = methods.insert_element_at_index(value, 1, '0')
                        pass  # TODO : return entry
                    case 0:
                        leading_digits = methods.reference_previous_values(entry, 'whole_value')
                        if leading_digits is not None:
                            value = list(value)
                            value.pop(0)
                            value.insert(0, leading_digits)
                            ''.join(value)  # TODO : return entry
                        else:
                            pass  # TODO : determine what to do if leading digits not found / FLAG

                        pass  # TODO : Remove zero, use reference_previous_value(), replace missing leading digits as necessary and move to phase 2
                    case _:
                        pass  # TODO : flag
            # checking and fixing accordingly if value is of form XX.XX
            elif methods.float_decimal_index(value) == 2:
                pass  # TODO : (see post_process_id = 1 workflow doc)
            else:
                pass  # TODO : flag

        elif len(value) == 6:
            # value of form XXXXXX:
            if value.isnumeric():
                methods.replace_with_decimal(value, 2)  # TODO : return entry
            # value of form XXX.XX:
            elif methods.float_decimal_index(value) == 4:
                entry[1] = float(value) / 10  # TODO : return entry
            # value of form XXXX.X:
            elif methods.float_decimal_index(value) == 5:
                entry[1] = float(value) / 100  # TODO : return entry
            # value of form XX.XXX where decimal is instead one of ( '/'  ';'  ','  '-' )
            elif methods.pressure_decimal_alternate(value):
                entry[1] = methods.replace_with_decimal(value, 2)  # TODO : return entry
            else:
                pass  # TODO : flag

        elif len(value) == 4:
            # value of form XXXX
            if value.isnumeric():
                pass  # TODO : refer to document
            # value of form +XXX or -XXX:
            if methods.removable_plus_minus(value):
                pass  # TODO : Remove value
            # value of form .XXX:
            elif methods.float_decimal_index(value) == 0:
                leading_digits = methods.reference_previous_values(entry, 'leading_digits')
                if leading_digits is not None:
                    value = list(value)
                    value.insert(0, leading_digits)
                    ''.join(value)  # TODO : return entry
                else:
                    pass  # TODO : determine what to do if leading digits not found / FLAG
            # value of form XX.X:
            elif methods.float_decimal_index(value) == 2:
                pass  # TODO : refer to document
            # value of form X.XX:
            elif methods.float_decimal_index(value) == 1:
                if value[0] == '0':
                    pass  # TODO : refer to document
                else:
                    pass  # TODO : refer to document
            else:
                pass  # TODO : flag

        elif len(value) == 3:
            # value of form XXX:
            if value.isnumeric():
                leading_digits = methods.reference_previous_values(entry, 'leading_digits')
                if leading_digits is not None:
                    value = list(value)
                    value.insert(0, leading_digits)
                    value.insert(1, '.')
                    ''.join(value)  # TODO : return entry
                else:
                    pass  # TODO : determine what to do if leading digits not found / FLAG
            index = methods.float_decimal_index(value)
            match index:
                # value of form .XX:
                case 0:
                    pass  # TODO : refer to document
                # value of form X.X:
                case 1:
                    pass  # TODO : refer to document
                # value of form XX.:
                case 2:
                    pass  # TODO : refer to document
                case _:
                    pass
            pass  # TODO : flag

        elif len(value) == 2:
            # value of form XX:
            if value.isnumeric():
                pass  # TODO : refer to document
            # value of form .X:
            elif methods.float_decimal_index(value) == 0:
                leading_digits = methods.reference_previous_values(entry, 'leading_digits')
                if leading_digits is not None:
                    value = list(value)
                    value.insert(0, leading_digits)
                    value.append('00')
                    ''.join(value)  # TODO : return entry
                else:
                    pass  # TODO : determine what to do if leading digits not found / FLAG
            else:
                pass  # TODO : flag

        elif len(value) == 7:
            # value of form XX.XXXX:
            if methods.float_decimal_index(value) == 2 and (value[:2] in ['29', '30']):
                value = methods.remove_elements_at_indices(value, [5])
                pass  # TODO : return entry
            # value of form XXX.XXX:
            elif methods.float_decimal_index(value) == 3:
                value = methods.remove_elements_at_indices(value, 1)
                pass  # TODO : return entry
            else:
                pass  # TODO : flag

        elif len(value) == 8:
            # value of form XX.XXXXX:
            if methods.float_decimal_index(value) == 2:
                value = methods.remove_trailing_digits(value, 2)
                pass  # TODO : return entry
            else:
                pass  # TODO : flag

        elif len(value) == 9:
            # single data entry comprises 2+ entries, entered in the same cell by transcriber
            if ',.' in value:
                pass  # TODO : parse values and create new entries as necessary for additional values
            else:
                pass  # TODO : flag

        else:
            pass  # TODO : flag
