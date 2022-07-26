import mysql.connector
import os

import time
import numpy as np
import f1_methods as f_methods
import r1_methods as r_methods
import config
import database_connection as db

db = db.db
cursor = db.cursor()

cursor.execute("SELECT * FROM data_entries_corrected "
               "WHERE field_id = 7 "
               "AND flagged = 0 "
               "LIMIT 10000;")

entries = cursor.fetchall()

test_list = []

start = time.time()

counter = 0
for entry in entries:
    equation_value = 0
    value = entry[1]
    if value is not None:
        if config.possible_pressure_formats(value):
            equation_value = r_methods.equation_resultant_value(entry, 1)
            if equation_value is not None:
                test_list.append([float(entry[1]), equation_value])
            else:
                pass
    counter += 1
    print(counter)
print(test_list)
print("Amount of equated entries: " + str(len(test_list)))
print(time.time() - start)

corr_eq_diff = []
for i in test_list:
    corr_eq_diff.append(i[1] - i[0])

corr_eq_diff_arr = np.array(corr_eq_diff)
print("Average difference between calculated value and actual value: " + str(np.average(corr_eq_diff_arr)))
print("Standard deviation: " + str(np.std(corr_eq_diff_arr)))
