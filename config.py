# File for configuring variables/attributes that are addressed in the workflow

import workflow_methods_master as methods

# unexpected characters in a data entry (when not surrounded on either side by digits)
unexpected_characters = ['?', '.', '*', '&', '#', '^', '$', '(', ')', '[', ']', '{', '}', '"', '/']


# characters that could potentially have replaced decimal point in a numerical data entry
decimal_point_alternates = [';', '-', '/', ',']


# values that can be disregarded automatically; method converts all data entries to lowercase to catch cases where term appears capitalized and uncapitalized
disregarded_values = ['empty', 'blank', 'retracted', 'empty / blank', 'vide', 'none existant', 'illegible']


# possible leading digits for a pressure value:
possible_lead_digits = ['28', '29', '30', '31']


# possible correct formats that a value can be in, for the case where we want to retrieve leading digits from it:
def possible_pressure_formats(value):
    if methods.desired_pressure_format(value):
        return True
    elif len(value) in [5, 6, 7, 8] and methods.float_decimal_index(value) == 2:
        return True
    elif len(value) == 5 and value.isnumeric():
        return True


# pressure config values
pressure_min = 28.000
pressure_max = 31.500
