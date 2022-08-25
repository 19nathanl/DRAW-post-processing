# File for configuring variables/attributes that are addressed in the workflow

import id1p1_methods as methods


# assigning post-process ID's to field ID's
ppid_to_field_id = {1: (4, 6, 7, 8, 67, 69),
                    2: 14,
                    3: (9, 10, 11, 12)
                    }


# unexpected characters in a data entry (when not surrounded on either side by digits)  TODO : determine if any alterations necessary for non-pressure values
unexpected_characters = {'?', '.', '*', '&', '#', '^', '$', '(', ')', '[', ']', '{', '}', '"', '/', '@', "\\"}


# characters that could potentially have replaced decimal point in a numerical data entry
decimal_point_alternates = {';', '-', '/', ','}


# values that can be disregarded automatically; method converts all data entries to lowercase to catch edge cases where term is capitalized or uncapitalized irregularly
disregarded_values = {'empty', 'blank', 'retracted', 'empty / blank', 'vide', 'none existant', 'illegible', ''}


# possible leading digits for a pressure value:
possible_lead_digits_pressure = {'28', '29', '30', '31'}


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
scalar_fluctuation_thresholds = {'01': 0.00, '02': 0.00, '03': 0.00, '04': 0.00, '05': 0.00, '06': 0.00,  # TODO : fill w/ pressure_fluctuation_stats results
                                 '07': 0.00, '08': 0.00, '09': 0.00, '10': 0.00, '11': 0.00, '12': 0.00}

# amount of time (in hours) between timestamps, for which a pressure fluctuation isn't granular enough
time_delta_limit = 12

# threshold value for which difference between transcribed and equation value requires further investigation (phase 2)
pressure_diff_threshold = 0.300


# intervals of interest for difference between transcribed and equation value - used for discerning values whose leading digits have (likely) been added incorrectly,
# hence the intervals occurring at +/- 1 range; configure the floats in the conditional statements according to your own statistical results (see stat_test_equations.py)
def possible_wrong_lead_digs_id_4(difference_value):  # TODO : fill in with same interval stats as other field id's below
    try:
        difference_value = float(difference_value)
        if -999999999 <= difference_value <= -999999999:
            return 'is_left'
        elif -999999999 <= difference_value <= 999999999:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_6(difference_value):
    try:
        difference_value = float(difference_value)
        if -1.015 <= difference_value <= -0.997:
            return 'is_left'
        elif 0.997 <= difference_value <= 1.015:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_7(difference_value):
    try:
        difference_value = float(difference_value)
        if -1.005 <= difference_value <= -0.995:
            return 'is_left'
        elif 0.995 <= difference_value <= 1.005:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_8(difference_value):
    try:
        difference_value = float(difference_value)
        if -1.200 <= difference_value <= -0.900:
            return 'is_left'
        elif 0.900 <= difference_value <= 1.200:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False
