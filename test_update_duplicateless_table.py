import config
import database_connection as db
import post_process_ids.id1.id_1_outliers as id1outliers

db = db.db
cursor = db.cursor()

cursor.execute("SELECT * FROM data_entries_corrected_duplicateless "
               "WHERE flagged = 0 "
               "AND field_id IN (4,6,7,8,67,69);")
entries = cursor.fetchall()

outliers = []
for entry in entries:
    if str(entry[1]).lower() not in [*config.disregarded_values, 'none'] and (float(entry[1]) < 27 or float(entry[1]) > 33):
        outliers.append(entry)

for outlier in outliers:
    print(outlier)
