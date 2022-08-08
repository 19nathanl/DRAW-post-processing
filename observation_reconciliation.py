import time

import database_connection as db
import statistics as stats

db = db.db
cursor = db.cursor()


def update_temp_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    sql_command = "INSERT INTO data_entries_corrected_duplicateless " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql_command, (entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged))
    db.commit()


def create_temp_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS data_entries_corrected_duplicateless AS SELECT * FROM data_entries_corrected LIMIT 0;")
    cursor.execute("SELECT COUNT(*) FROM data_entries_corrected_duplicateless;")
    count = cursor.fetchall()[0][0]
    if count != 0:
        cursor.execute("DELETE FROM data_entries_corrected_duplicateless;")
        db.commit()
    # TODO : add indexes 'data_entries_corrected_duplicateless_field_date' on field_id, observation_date to speed up code


def remove_duplicates():
    create_temp_table()
    cursor.execute("SELECT * FROM data_entries_corrected;")
    data_entries = cursor.fetchall()

    counter = 0
    checked_entries = {}
    for entry in data_entries:
        if entry[9] is not None and entry[0] not in checked_entries.keys():
            cursor.execute("SELECT * FROM data_entries_corrected WHERE field_id = {} AND observation_date = '{}';".format(entry[4], str(entry[9])))
            duplicates = cursor.fetchall()
            # if there is only one transcription for this observation, add it to the new table
            if len(duplicates) == 1:
                update_temp_table(*entry)
            # if observation has a mode transcription, choose the mode transcription and add it to the temp table
            else:
                try:
                    chosen_value = stats.mode([item[1] for item in duplicates])
                    for i in range(len(duplicates)):
                        if duplicates[i][1] == chosen_value:
                            update_temp_table(*duplicates[i])
                            break
                    for item in duplicates:
                        checked_entries[item[0]] = None
                # if the observation does not have a mode value, choose transcription from user with most entries in the database and add to the temp table
                except stats.StatisticsError:
                    user_entries_list = []
                    for duplicate in duplicates:
                        cursor.execute("SELECT COUNT(*) FROM data_entries_corrected "
                                       "WHERE user_id = {};".format(duplicate[2]))
                        user_entries_list.append([duplicate[2], cursor.fetchall()[0][0]])
                    sorted_user_entries_list = sorted(user_entries_list, key=lambda x: x[1])
                    chosen_user = sorted_user_entries_list[len(sorted_user_entries_list) - 1][0]
                    chosen_entry = tuple([duplicate for duplicate in duplicates if duplicate[2] == chosen_user])
                    update_temp_table(*chosen_entry)
                    for item in duplicates:
                        checked_entries[item[0]] = item[0]
        elif entry[9] is None and entry not in checked_entries:
            update_temp_table(*entry)
        counter += 1
        print(counter)
    # TODO : rename duplicateless table to regular 'data_entries_corrected' table, and delete old table with duplicates


start = time.time()
remove_duplicates()
print("Took {} seconds to run.".format(str(time.time() - start)))
