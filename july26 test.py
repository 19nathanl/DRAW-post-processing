import database_connection as db
import r1_methods
import statistics as stats
import config

db = db.db
cursor = db.cursor()

# pulls all id's of values that had leading digits artificially added to them in phase 1
cursor.execute("SELECT id FROM pressure_entries_phase1_errors WHERE error_code = 110 AND field_id in (7,8);")
excluded_ids = cursor.fetchall()

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


### finding mean and standard deviation of field_id's 7 (between transcribed and equation values)  TODO : add field_id 10 to r1_methods "equation_resultant_value" method ***
for entry in field_ids_7:
    value = entry[1]
    if value is not None:
        if config.possible_pressure_formats(value):
            equation_value = r1_methods.equation_resultant_value(entry, 2)
            if equation_value is not None:
                field_id_7_comparison.append([float(entry[1]), equation_value])
            else:
                pass
mean_diff_id_8 = []
for value_pair in field_id_7_comparison:
    mean_diff_id_8.append(value_pair[1] - value_pair[0])
print("Mean difference between transcribed and equation value (T_(0)): " + str(stats.mean(mean_diff_id_8)))




### finding mean and standard deviation of field_id's 8 (between transcribed and equation values)
for entry in field_ids_8:
    value = entry[1]
    if value is not None:
        if config.possible_pressure_formats(value):
            equation_value = r1_methods.equation_resultant_value(entry, 1)
            if equation_value is not None:
                field_id_8_comparison.append([float(entry[1]), equation_value])
            else:
                pass
mean_diff_id_8 = []
for value_pair in field_id_8_comparison:
    mean_diff_id_8.append(value_pair[1] - value_pair[0])
print("Mean difference between transcribed and equation value (SLP): " + str(stats.mean(mean_diff_id_8)))
