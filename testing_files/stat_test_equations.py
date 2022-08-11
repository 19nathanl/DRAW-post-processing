import database_connection as db
import id1p2_methods
import statistics as stats
import config
import matplotlib.pyplot as plt
import time
import numpy as np

db = db.db
cursor = db.cursor()


# pulls all id's of values that had leading digits artificially added to them in phase 1
cursor.execute("SELECT id FROM pressure_entries_phase1_errors WHERE error_code IN (110,115) AND field_id IN (6,7,8);")
excluded_ids = [item[0] for item in cursor.fetchall()]

# pulls all entries of values from phase 1 - can remove or add 'NOT' condition before IN, based on whether you want to analyze values with leading digits added (or not)
cursor.execute("SELECT * FROM pressure_entries_corrected WHERE field_id IN (6,7,8) AND id IN {} AND flagged = 0;".format(tuple(excluded_ids)))
corr_vals_excl_lead_dig = cursor.fetchall()

field_ids_6 = []
field_ids_7 = []
field_ids_8 = []

for entry in corr_vals_excl_lead_dig:
    if entry[4] == 6:
        field_ids_6.append(entry)
    elif entry[4] == 7:
        field_ids_7.append(entry)
    elif entry[4] == 8:
        field_ids_8.append(entry)

field_id_6_comparison = []
field_id_7_comparison = []
field_id_8_comparison = []


def stat_boundary(boundary, mean_diff_list, arr):
    return "Number of differences between -{} and {}: ".format(boundary, boundary) + str(np.sum(np.logical_and(-boundary < arr, arr < boundary))) + " ({}%)".format(round(100 * (np.sum(np.logical_and(-boundary < arr, arr < boundary)) / len(mean_diff_list)), 3))


def generated_stats_field_id_6():
    start = time.time()
    counter = 0
    ### finding mean and standard deviation of field_id's 6 (between transcribed and equation values)
    for transcribed_entry in field_ids_6:
        value = transcribed_entry[1]
        if value is not None:
            if config.possible_pressure_formats(value, False):
                equation_value = r1_methods.equation_resultant_value(transcribed_entry)
                if equation_value is not None:
                    field_id_6_comparison.append([float(transcribed_entry[1]), equation_value])
                else:
                    pass
        counter += 1
        print(counter)

    mean_diff_id_6 = []
    for value_pair in field_id_6_comparison:
        mean_diff_id_6.append(value_pair[1] - value_pair[0])
    print("Took " + str(round(time.time() - start, 2)) + " seconds to run:")
    print("Number of differences: " + str(len(mean_diff_id_6)))
    print("Mean difference between transcribed and equation value (Baro_instr_corr): " + str(stats.mean(mean_diff_id_6)))
    print("Standard deviation: " + str(stats.stdev(mean_diff_id_6)))
    arr = np.array(mean_diff_id_6)

    print(stat_boundary(0.00001, mean_diff_id_6, arr))
    print(stat_boundary(0.0001, mean_diff_id_6, arr))
    print(stat_boundary(0.001, mean_diff_id_6, arr))
    print(stat_boundary(0.005, mean_diff_id_6, arr))
    print(stat_boundary(0.01, mean_diff_id_6, arr))
    print(stat_boundary(0.1, mean_diff_id_6, arr))
    print(stat_boundary(0.2, mean_diff_id_6, arr))
    print(stat_boundary(0.5, mean_diff_id_6, arr))
    print(stat_boundary(0.997, mean_diff_id_6, arr))
    print(stat_boundary(1, mean_diff_id_6, arr))
    print(stat_boundary(1.001, mean_diff_id_6, arr))
    print(stat_boundary(1.005, mean_diff_id_6, arr))
    print(stat_boundary(1.015, mean_diff_id_6, arr))

    # plt.hist(arr, bins=100, log=True)
    # plt.show()


def generated_stats_field_id_7():
    start = time.time()
    counter = 0
    ### finding mean and standard deviation of field_id's 7 (between transcribed and equation values)
    for transcribed_entry in field_ids_7:
        value = transcribed_entry[1]
        if value is not None:
            if config.possible_pressure_formats(value, False):
                equation_value = r1_methods.equation_resultant_value(transcribed_entry)
                if equation_value is not None:
                    field_id_7_comparison.append([float(transcribed_entry[1]), equation_value])
                else:
                    pass
        counter += 1
        print(counter)

    mean_diff_id_7 = []
    for value_pair in field_id_7_comparison:
        mean_diff_id_7.append(value_pair[1] - value_pair[0])
    print("Took " + str(round(time.time() - start, 2)) + " seconds to run:")
    print("Number of differences: " + str(len(mean_diff_id_7)))
    print("Mean difference between transcribed and equation value (T_(0)): " + str(stats.mean(mean_diff_id_7)))
    print("Standard deviation: " + str(stats.stdev(mean_diff_id_7)))
    arr = np.array(mean_diff_id_7)

    print(stat_boundary(0.0001, mean_diff_id_7, arr))
    print(stat_boundary(0.001, mean_diff_id_7, arr))
    print(stat_boundary(0.005, mean_diff_id_7, arr))
    print(stat_boundary(0.01, mean_diff_id_7, arr))
    print(stat_boundary(0.1, mean_diff_id_7, arr))
    print(stat_boundary(0.2, mean_diff_id_7, arr))
    print(stat_boundary(0.5, mean_diff_id_7, arr))
    print(stat_boundary(0.995, mean_diff_id_7, arr))  # min. bound
    print(stat_boundary(1, mean_diff_id_7, arr))
    print(stat_boundary(1.001, mean_diff_id_7, arr))
    print(stat_boundary(1.005, mean_diff_id_7, arr))  # max. bound
    print(stat_boundary(2, mean_diff_id_7, arr))

    plt.hist(arr, bins=100, log=True)
    plt.show()


def generated_stats_field_id_8():
    start = time.time()
    counter = 0
    ### finding mean and standard deviation of field_id's 8 (between transcribed and equation values)
    for transcribed_entry in field_ids_8:
        value = transcribed_entry[1]
        if value is not None:
            if config.possible_pressure_formats(value, False):
                equation_value = r1_methods.equation_resultant_value(transcribed_entry)
                if equation_value is not None:
                    field_id_8_comparison.append([float(transcribed_entry[1]), equation_value])
                else:
                    pass
        counter += 1
        print(counter)
    mean_diff_id_8 = []
    for value_pair in field_id_8_comparison:
        mean_diff_id_8.append(value_pair[1] - value_pair[0])
    print("Took " + str(round(time.time() - start, 2)) + " seconds to run:")
    print("Number of differences: " + str(len(mean_diff_id_8)))
    print("Mean difference between transcribed and equation value (SLP): " + str(stats.mean(mean_diff_id_8)))
    print("Standard deviation: " + str(stats.stdev(mean_diff_id_8)))
    arr = np.array(mean_diff_id_8)

    print(stat_boundary(0.01, mean_diff_id_8, arr))
    print(stat_boundary(0.05, mean_diff_id_8, arr))
    print(stat_boundary(0.1, mean_diff_id_8, arr))
    print(stat_boundary(0.12, mean_diff_id_8, arr))
    print(stat_boundary(0.2, mean_diff_id_8, arr))
    print(stat_boundary(0.5, mean_diff_id_8, arr))
    print(stat_boundary(0.75, mean_diff_id_8, arr))
    print(stat_boundary(0.875, mean_diff_id_8, arr))
    print(stat_boundary(0.900, mean_diff_id_8, arr))  # min. bound
    print(stat_boundary(0.990, mean_diff_id_8, arr))
    print(stat_boundary(1, mean_diff_id_8, arr))
    print(stat_boundary(1.05, mean_diff_id_8, arr))
    print(stat_boundary(1.1, mean_diff_id_8, arr))
    print(stat_boundary(1.125, mean_diff_id_8, arr))
    print(stat_boundary(1.15, mean_diff_id_8, arr))
    print(stat_boundary(1.2, mean_diff_id_8, arr))  # max. bound
    print(stat_boundary(1.25, mean_diff_id_8, arr))
    print(stat_boundary(1.5, mean_diff_id_8, arr))

    plt.hist(arr, bins=100, log=True)
    plt.show()


generated_stats_field_id_6()
