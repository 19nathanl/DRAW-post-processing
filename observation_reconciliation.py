# This file is used to remove all duplicate transcription entries for the same observation in the database

import database_connection as db
import statistics as stats
import tables

db = db.db
cursor = db.cursor()


def remove_duplicates():
    cursor.execute("SELECT * FROM data_entries_corrected;")
    data_entries = cursor.fetchall()

    counter = 0
    checked_entries = {}
    for entry in data_entries:
        if entry[9] is not None and entry[0] not in checked_entries.keys():
            cursor.execute("SELECT * FROM data_entries_corrected "
                           "WHERE field_id = {} "
                           "AND observation_date = '{}';".format(entry[4], str(entry[9])))
            duplicates = cursor.fetchall()
            # if there is only one transcription for this observation, add it to the new table
            if len(duplicates) == 1:
                tables.add_to_duplicateless_table(*entry)
            # if observation has a mode transcription, choose the mode transcription and add it to the temp table
            else:
                try:
                    chosen_value = stats.mode([item[1] for item in duplicates])
                    for i in range(len(duplicates)):
                        if duplicates[i][1] == chosen_value:
                            tables.add_to_duplicateless_table(*duplicates[i])
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
                    tables.add_to_duplicateless_table(*chosen_entry)
                    for item in duplicates:
                        checked_entries[item[0]] = item[0]
        elif entry[9] is None and entry not in checked_entries:
            tables.add_to_duplicateless_table(*entry)
        counter += 1
        print('Reconciliation:', counter)
