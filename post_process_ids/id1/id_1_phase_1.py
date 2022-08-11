# post-processing format check algorithm for post_process_id = 1

import id1p1_methods as methods
import tables


def phase_1(entry):
    return_list = [entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8], entry[9]]
    value = entry[1]

    # Checking to see if raw pressure value is already of form XX.XXX
    if methods.desired_pressure_format(value):
        tables.update_corrected_table(*return_list, 0)

    elif methods.disregarded_value(value):
        tables.update_corrected_table(*return_list, 0)

    elif value is None:
        tables.update_corrected_table(*return_list, 0)

    # if not of the right form initially, corrects format and returns entry with corrected value
    else:
        value = methods.remove_spaces(value, return_list)
        value = methods.correct_double_decimals(value, return_list)
        value = methods.remove_alphabetical_char(value, return_list)
        value = methods.remove_unexpected_characters(value, return_list)

        return_list[1] = value

        # checking again if pressure value is of form XX.XXX after simple clean-up methods
        if methods.desired_pressure_format(value):
            tables.update_corrected_table(*return_list, 0)

        # TODO : 'Illegible' entries (currently disregarded)
        # TODO : append error_code in corrected table to any value being passed to said table with value '1'

        elif value == '':
            tables.update_corrected_table(*return_list, 0)

        elif len(value) == 5:
            if value.isnumeric():
                original_value = value
                value, return_list[1] = float(value) / 1000, float(value) / 1000
                tables.add_error_edit_code('105', original_value, value, return_list)
                tables.update_corrected_table(*return_list, 0)

            # checking and fixing accordingly if pressure value of form 0.XXX, 2.XXX, 3.XXX, or 9.XXX
            elif methods.float_decimal_index(value) == 1:
                match int(value[0]):
                    case 2:
                        return_list[1] = methods.insert_element_at_index(value, 1, '9', return_list)
                        tables.update_corrected_table(*return_list, 0)
                    case 3:
                        return_list[1] = methods.insert_element_at_index(value, 1, '0', return_list)
                        tables.update_corrected_table(*return_list, 0)
                    case 0:
                        leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                        if leading_digits is not None:
                            original_value = value
                            value = list(value)
                            value[0] = leading_digits
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('110', original_value, return_list[1], return_list, 'Ref. entry ID: {}, '
                                                                                                           'Value: {}, '
                                                                                                           'Datetime of reference: {}'.format(*ref_info))
                            tables.update_corrected_table(*return_list, 0)
                        else:
                            original_value = value
                            value = list(value)
                            value[0] = '29'
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                            tables.update_corrected_table(*return_list, 0)
                    case 9:
                        original_value = value
                        value = list(value)
                        value.insert(0, '2')
                        value, return_list[1] = ''.join(value), ''.join(value)
                        tables.add_error_edit_code('106', original_value, value, return_list)
                        tables.update_corrected_table(*return_list, 0)
                    case _:
                        tables.add_error_edit_code('000', value, '', return_list)
                        tables.update_corrected_table(*return_list, 1)
            # checking and fixing accordingly if value is of form XX.XX
            elif methods.float_decimal_index(value) == 2:
                if entry[4] == 8:
                    tables.update_corrected_table(*return_list, 0)
                else:
                    original_value = value
                    value = list(value)
                    value.append('0')
                    value, return_list[1] = ''.join(value), ''.join(value)
                    tables.add_error_edit_code('107', original_value, value, return_list)
                    tables.update_corrected_table(*return_list, 0)
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        elif len(value) == 6:
            # value of form XXXXXX:
            if value.isnumeric():
                return_list[1] = methods.replace_with_decimal(value, 2, return_list)
                tables.update_corrected_table(*return_list, 0)
            # value of form XXX.XX:
            elif methods.float_decimal_index(value) == 3:
                original_value = value
                value, return_list[1] = round(float(value) / 10, 3), round(float(value) / 10, 3)
                tables.add_error_edit_code('105', original_value, value, return_list)
                tables.update_corrected_table(*return_list, 0)
            # value of form XXXX.X:
            elif methods.float_decimal_index(value) == 4:
                original_value = value
                value, return_list[1] = float(value) / 100, float(value) / 100
                tables.add_error_edit_code('105', original_value, value, return_list)
                tables.update_corrected_table(*return_list, 0)
            # value of form XX.XXX where decimal is instead one of ( '/'  ';'  ','  '-' )
            elif methods.pressure_decimal_alternate(value):
                return_list[1] = methods.replace_with_decimal(value, 2, return_list)
                tables.update_corrected_table(*return_list, 0)
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        elif len(value) == 4:
            # value of form XXXX
            if value.isnumeric():
                original_value = value
                value = list(value)
                value.append('0')
                value.insert(2, '.')
                value, return_list[1] = ''.join(value), ''.join(value)
                tables.add_error_edit_code('107', original_value, value, return_list)
                tables.update_corrected_table(*return_list, 0)
            # value of form +XXX or -XXX:
            elif methods.removable_plus_minus(value):
                original_value = value
                return_list[1] = ''
                tables.add_error_edit_code('113', original_value, return_list[1], return_list)
                tables.update_corrected_table(*return_list, 0)
            # value of form .XXX:
            elif methods.float_decimal_index(value) == 0:
                leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                if leading_digits is not None:
                    original_value = value
                    value = list(value)
                    value.insert(0, leading_digits)
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('110', original_value, return_list[1], return_list, 'Ref. entry ID: {}, '
                                                                                                   'Value: {}, '
                                                                                                   'Datetime of reference: {}'.format(*ref_info))
                    tables.update_corrected_table(*return_list, 0)
                else:
                    original_value = value
                    value = list(value)
                    value.insert(0, '29')
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                    tables.update_corrected_table(*return_list, 0)
            # value of form XX.X:
            elif methods.float_decimal_index(value) == 2:
                if value[:2] in ['29', '30']:
                    original_value = value
                    value = list(value)
                    value.append('00')
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('107', original_value, return_list[1], return_list)
                    tables.update_corrected_table(*return_list, 0)
                else:
                    return_list[1] = methods.remove_elements_at_indices(value, 2, return_list)  # convert to form XXX
                    leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                    if leading_digits is not None:
                        original_value = return_list[1]
                        value = list(return_list[1])
                        value.insert(0, leading_digits)
                        value.insert(1, '.')
                        value, return_list[1] = ''.join(value), ''.join(value)
                        tables.add_error_edit_code('110', original_value, value, return_list,
                                                   'Ref. entry ID: {}, '
                                                   'Value: {}, '
                                                   'Datetime of reference: {}'.format(*ref_info))
                        tables.update_corrected_table(*return_list, 0)
                    else:
                        original_value = return_list[1]
                        value = list(return_list[1])
                        value.insert(0, '29.')
                        return_list[1] = ''.join(value)
                        tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                        tables.update_corrected_table(*return_list, 0)
            # value of form X.XX:
            elif methods.float_decimal_index(value) == 1:
                if value[0] != '0':
                    return_list[1] = methods.remove_elements_at_indices(value, 1, return_list)
                    leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                    if leading_digits is not None:
                        original_value = return_list[1]
                        value = list(return_list[1])
                        value.insert(0, leading_digits)
                        value.insert(1, '.')
                        return_list[1] = ''.join(value)
                        tables.add_error_edit_code('110', original_value, return_list[1], return_list,
                                                   'Ref. entry ID: {}, '
                                                   'Value: {}, '
                                                   'Datetime of reference: {}'.format(*ref_info))
                        tables.update_corrected_table(*return_list, 0)
                    else:
                        original_value = return_list[1]
                        value = list(return_list[1])
                        value.insert(0, '29.')
                        return_list[1] = ''.join(value)
                        tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                        tables.update_corrected_table(*return_list, 0)
                else:  # if value is of form '0.XX':
                    if entry[4] == 8:
                        leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                        if leading_digits is not None:
                            original_value = value
                            value = list(value)
                            value[0] = leading_digits
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('110', original_value, return_list[1], return_list,
                                                       'Ref. entry ID: {}, '
                                                       'Value: {}, '
                                                       'Datetime of reference: {}'.format(*ref_info))
                            tables.update_corrected_table(*return_list, 0)
                        else:
                            original_value = value
                            value = list(value)
                            value[0] = '29.'
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                            tables.update_corrected_table(*return_list, 0)
                    else:
                        leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                        if leading_digits is not None:
                            original_value = value
                            value = list(value)
                            value.remove('.')
                            value.insert(0, '.')
                            value.insert(0, leading_digits)
                            value, return_list[1] = ''.join(value), ''.join(value)
                            tables.add_error_edit_code('110', original_value, value, return_list,
                                                       'Ref. entry ID: {}, '
                                                       'Value: {}, '
                                                       'Datetime of reference: {}'.format(*ref_info))
                            tables.update_corrected_table(*return_list, 0)
                        else:
                            original_value = value
                            value = list(value)
                            value.remove('.')
                            value.insert(0, '29.')
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                            tables.update_corrected_table(*return_list, 0)
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        elif len(value) == 3:
            # value of form XXX:
            if value.isnumeric():
                leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                if leading_digits is not None:
                    original_value = value
                    value = list(value)
                    value.insert(0, leading_digits)
                    value.insert(1, '.')
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('110', original_value, return_list[1], return_list, 'Ref. entry ID: {}, '
                                                                                                   'Value: {}, '
                                                                                                   'Datetime of reference: {}'.format(*ref_info))
                    tables.update_corrected_table(*return_list, 0)
                else:
                    original_value = value
                    value = list(value)
                    value.insert(0, '29.')
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                    tables.update_corrected_table(*return_list, 0)
            elif not value.isnumeric():
                index = methods.float_decimal_index(value)
                match index:
                    # value of form .XX:
                    case 0:
                        leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                        if leading_digits is not None:
                            original_value = value
                            value = list(value)
                            value.insert(0, leading_digits)
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('110', original_value, return_list[1], return_list,
                                                       'Ref. entry ID: {}, '
                                                       'Value: {}, '
                                                       'Datetime of reference: {}'.format(*ref_info))
                            tables.update_corrected_table(*return_list, 0)
                        else:
                            original_value = value
                            value = list(value)
                            value.insert(0, '29')
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                            tables.update_corrected_table(*return_list, 0)
                    # value of form X.X:
                    case 1:
                        tables.add_error_edit_code('000', value, '', return_list)
                        tables.update_corrected_table(*return_list, 1)
                    # value of form XX.:
                    case 2:
                        tables.add_error_edit_code('000', value, '', return_list)
                        tables.update_corrected_table(*return_list, 1)
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        elif len(value) == 2:
            # value of form XX:
            if value.isnumeric():
                if value in ('29', '30'):
                    original_value = value
                    value = list(value)
                    value.append('.000')
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('107', original_value, return_list[1], return_list)
                    tables.update_corrected_table(*return_list, 0)
                elif (float(value) < 28) or (float(value) >= 33):
                    if entry[4] == 8:
                        leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                        if leading_digits is not None:
                            original_value = value
                            value = list(value)
                            value.insert(0, leading_digits)
                            value.insert(1, '.')
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('110', original_value, return_list[1], return_list,
                                                       'Ref. entry ID: {}, '
                                                       'Value: {}, '
                                                       'Datetime of reference: {}'.format(*ref_info))
                            tables.update_corrected_table(*return_list, 0)
                        else:
                            original_value = value
                            value = list(value)
                            value.insert(0, '29.')
                            return_list[1] = ''.join(value)
                            tables.add_error_edit_code('115', original_value, return_list[1], return_list)
                            tables.update_corrected_table(*return_list, 0)
                    elif entry[4] in [67, 69]:
                        return_list[4], return_list[5] = 68, 'City Hall Attached Thermometer'
                        tables.add_error_edit_code('111', value, '', return_list, 'Previous field_id: {}'.format(entry[4]))
                        tables.update_corrected_table(*return_list, 0)
                    else:
                        tables.add_error_edit_code('000', value, '', return_list)
                        tables.update_corrected_table(*return_list, 1)
            # value of form .X:
            elif methods.float_decimal_index(value) == 0:
                leading_digits, ref_info = methods.reference_previous_values(tuple(return_list), 'leading_digits')
                if leading_digits is not None:
                    original_value = value
                    value = list(value)
                    value.insert(0, leading_digits)
                    tables.add_error_edit_code('110', original_value, ''.join(value), return_list,
                                               'Ref. entry ID: {}, '
                                               'Value: {}, '
                                               'Datetime of reference: {}'.format(*ref_info))
                    original_value = ''.join(value)
                    value.append('00')
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('107', original_value, return_list[1], return_list)
                    tables.update_corrected_table(*return_list, 0)
                else:
                    original_value = value
                    value = list(value)
                    value.insert(0, '29')
                    tables.add_error_edit_code('115', original_value, ''.join(value), return_list)
                    original_value = ''.join(value)
                    value.append('00')
                    return_list[1] = ''.join(value)
                    tables.add_error_edit_code('107', original_value, return_list[1], return_list)
                    tables.update_corrected_table(*return_list, 0)
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        elif len(value) == 7:
            # value of form XX.XXXX:
            if methods.float_decimal_index(value) == 2 and (value[:2] in ['29', '30']):
                return_list[1] = methods.remove_elements_at_indices(value, 5, return_list)
                tables.update_corrected_table(*return_list, 0)
            # value of form XXX.XXX:
            elif methods.float_decimal_index(value) == 3:
                return_list[1] = methods.remove_elements_at_indices(value, 1, return_list)
                tables.update_corrected_table(*return_list, 0)
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        elif len(value) == 8:
            # value of form XX.XXXXX:
            if methods.float_decimal_index(value) == 2:
                return_list[1] = methods.remove_trailing_digits(value, 2, return_list)
                tables.update_corrected_table(*return_list, 0)
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        elif len(value) >= 9:
            # single data entry comprises 2+ entries, entered in the same cell by transcriber
            if ',' in value:
                original_value = value
                index = value.index(',')
                value = value[:index]
                return_list[1] = value
                tables.add_error_edit_code('112', original_value, return_list[1], return_list)
                phase_1(tuple(return_list))  # once we've parsed the entry and reduced it to a single observation, put it back through same algorithm again
            else:
                tables.add_error_edit_code('000', value, '', return_list)
                tables.update_corrected_table(*return_list, 1)


        else:
            tables.add_error_edit_code('000', value, '', return_list)
            tables.update_corrected_table(*return_list, 1)
