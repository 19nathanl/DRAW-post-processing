# File for configuring variables/attributes that are addressed in the workflow


# unexpected characters in a data entry (when not surrounded on either side by digits)
unexpected_characters = ['?', '.', '*', '&', '#', '^', '$', '(', ')', '[', ']', '{', '}', '"', '/']


# characters that could potentially have replaced decimal point in a numerical data entry
decimal_point_alternates = [';', '-', '/', ',']


# values that can be disregarded automatically; all lower case, method will convert all data entries to lowercase to catch max. edge cases
disregarded_values = ['empty', 'blank', 'retracted', 'empty/blank', 'vide']


# pressure config values
pressure_min = 28.000
pressure_max = 31.500
