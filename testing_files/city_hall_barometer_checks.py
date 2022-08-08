import database_connection as db
import statistics as stats
import time

db = db.db
cursor = db.cursor()

cursor.execute("SELECT * FROM data_entries_corrected_duplicateless WHERE field_id = 6;")
baro_inst_cor_list = cursor.fetchall()

start = time.time()
counter = 0
value_diff_list = []
for baro_cor_entry in baro_inst_cor_list:
    if baro_cor_entry[9] is not None:
        cursor.execute("SELECT * FROM data_entries_corrected_duplicateless WHERE field_id = 69 AND observation_date = '{}'".format(baro_cor_entry[9]))
        city_hall_baro_cor = cursor.fetchall()[0][0]
        value_diff_list.append(round(float(city_hall_baro_cor) - float(baro_cor_entry), 3))
    counter += 1
    print(counter)

    print("Took " + str(round(time.time() - start, 2)) + " seconds to run:")
    print("Number of differences: " + str(len(value_diff_list)))
    print("Mean difference between corrected city hall barometer, and corrected barometer: " + str(stats.mean(value_diff_list)))
    print("Standard deviation: " + str(stats.stdev(value_diff_list)))
