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

# threshold value for which fluctuation between previous timestamp and current timestamp (for same field id) requires further investigation (phase 2)
fluctuation_threshold = None  # TODO : replace with sensible threshold based on month / field_id (?)

# threshold value for which difference between transcribed and equation value requires further investigation (phase 2)
pressure_diff_threshold = 0.300


# intervals of interest for difference between transcribed and equation value - used for discerning values whose leading digits have (likely) been added incorrectly;
# configure the floats in the conditional statements according to your own statistical results (see stat_test_equations.py)
def possible_wrong_lead_digs_id_7(value):
    try:
        value = float(value)
        if -1.005 <= value <= -0.995:
            return 'is_left'
        elif 0.995 <= value <= 1.005:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_8(value):
    try:
        value = float(value)
        if -1.200 <= value <= -0.900:
            return 'is_left'
        elif 0.900 <= value <= 1.200:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_6(value):
    try:
        value = float(value)
        if -1.015 <= value <= -0.997:
            return 'is_left'
        elif 0.997 <= value <= 1.015:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False
