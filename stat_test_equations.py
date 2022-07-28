import database_connection as db
import r1_methods
import statistics as stats
import config
import matplotlib.pyplot as plt
import time
import numpy as np

db = db.db
cursor = db.cursor()


# pulls all id's of values that had leading digits artificially added to them in phase 1
cursor.execute("SELECT id FROM pressure_entries_phase1_errors WHERE error_code = 110 AND field_id IN (7,8);")
excluded_ids = [item[0] for item in cursor.fetchall()]

# pulls all entries of values that didn't have leading digits added to them in phase 1, but are cleaned up appropriately
cursor.execute("SELECT * FROM pressure_entries_corrected WHERE field_id IN (7,8) AND id NOT IN {} AND flagged = 0;".format(tuple(excluded_ids)))
corr_vals_excl_lead_dig = cursor.fetchall()

field_ids_7 = []
field_ids_8 = []

for entry in corr_vals_excl_lead_dig:
    if entry[4] == 7:
        field_ids_7.append(entry)
    elif entry[4] == 8:
        field_ids_8.append(entry)

field_id_7_comparison = []
field_id_8_comparison = []


def stat_boundary(boundary, mean_diff_list, arr):
    return "Number of differences between -{} and {}: ".format(boundary, boundary) + str(np.sum(np.logical_and(-boundary < arr, arr < boundary))) + " ({}%)".format(round(100 * (np.sum(np.logical_and(-boundary < arr, arr < boundary)) / len(mean_diff_list)), 3))


def generated_stats_field_id_7():
    start = time.time()
    counter = 0
    ### finding mean and standard deviation of field_id's 7 (between transcribed and equation values)
    for entry in field_ids_7:
        value = entry[1]
        if value is not None:
            if config.possible_pressure_formats(value):
                equation_value = r1_methods.equation_resultant_value(entry)
                if equation_value is not None:
                    field_id_7_comparison.append([float(entry[1]), equation_value])
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
    print(stat_boundary(0.01, mean_diff_id_7, arr))
    print(stat_boundary(0.1, mean_diff_id_7, arr))
    print(stat_boundary(0.2, mean_diff_id_7, arr))
    print(stat_boundary(0.5, mean_diff_id_7, arr))
    print(stat_boundary(1, mean_diff_id_7, arr))
    print(stat_boundary(1.001, mean_diff_id_7, arr))
    print(stat_boundary(1.005, mean_diff_id_7, arr))
    print(stat_boundary(2, mean_diff_id_7, arr))

    plt.hist(mean_diff_id_7, bins=[-1.005, -1.001, -1, -0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1, 1, 1.001, 1.005])
    plt.show()


def generated_stats_field_id_8():
    start = time.time()
    counter = 0
    ### finding mean and standard deviation of field_id's 8 (between transcribed and equation values)
    for entry in field_ids_8:
        value = entry[1]
        if counter == 4091:
            print("stop here")
        if value is not None:
            if config.possible_pressure_formats(value):
                equation_value = r1_methods.equation_resultant_value(entry)
                if equation_value is not None:
                    field_id_8_comparison.append([float(entry[1]), equation_value])
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

    print(stat_boundary(0.0001, mean_diff_id_8, arr))
    print(stat_boundary(0.001, mean_diff_id_8, arr))
    print(stat_boundary(0.01, mean_diff_id_8, arr))
    print(stat_boundary(0.05, mean_diff_id_8, arr))
    print(stat_boundary(0.1, mean_diff_id_8, arr))
    print(stat_boundary(0.12, mean_diff_id_8, arr))
    print(stat_boundary(0.2, mean_diff_id_8, arr))
    print(stat_boundary(0.5, mean_diff_id_8, arr))
    print(stat_boundary(1, mean_diff_id_8, arr))
    print(stat_boundary(10, mean_diff_id_8, arr))
    print(stat_boundary(20, mean_diff_id_8, arr))
    print(stat_boundary(30, mean_diff_id_8, arr))
    print(stat_boundary(50, mean_diff_id_8, arr))
    print(stat_boundary(70, mean_diff_id_8, arr))

    plt.hist(mean_diff_id_8, bins=[-20, -10, -5, -1, -0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1, 1, 5, 10, 20])
    plt.show()


generated_stats_field_id_8()
