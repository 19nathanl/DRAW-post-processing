# File for configuring variables/attributes that are addressed in the workflow

import id1p1_methods as methods

# unexpected characters in a data entry (when not surrounded on either side by digits)  TODO : determine if any alterations necessary for non-pressure values
unexpected_characters = ['?', '.', '*', '&', '#', '^', '$', '(', ')', '[', ']', '{', '}', '"', '/', '@', "\\"]


# characters that could potentially have replaced decimal point in a numerical data entry
decimal_point_alternates = [';', '-', '/', ',']


# values that can be disregarded automatically; method converts all data entries to lowercase to catch edge cases where term is capitalized or uncapitalized irregularly
disregarded_values = ['empty', 'blank', 'retracted', 'empty / blank', 'vide', 'none existant', 'illegible', '']


# possible leading digits for a pressure value:
possible_lead_digits_pressure = ['28', '29', '30', '31']


# possible correct formats that a value can be in, for cases where we want to retrieve leading digits from it (True) or use the whole value (False):
def possible_pressure_formats(value, for_leading_digits):
    if methods.desired_pressure_format(value):
        return True
    elif len(value) in [5, 6, 7, 8] and methods.float_decimal_index(value) == 2:
        return True
    elif for_leading_digits:
        if len(value) == 5 and value.isnumeric():
            return True


# outlier bounds for pressure values
pressure_min = 27.000
pressure_max = 33.000
