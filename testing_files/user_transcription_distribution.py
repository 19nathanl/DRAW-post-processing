import database_connection as db
import time
import matplotlib.pyplot as plt

# Pulls all the users in the database, finds how many transcriptions are made by each user, and plots them accordingly.
# Will help find a sensible cut-off point for users that don't contribute much and therefore probably did not know what they were doing.

db = db.db
cursor = db.cursor()

cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()

users_transcription_list = []

counter = 0
start = time.time()
for i in users:
    id = i[0]
    sql_command = "SELECT COUNT(*) from data_entries_raw " \
                  "WHERE user_id = {};".format(id)
    cursor.execute(sql_command)
    num = cursor.fetchall()[0][0]
    users_transcription_list.append([id, num])
    counter += 1
    print(counter)

print("Took " + str(time.time() - start) + " seconds to run.")

list_sorted = sorted(users_transcription_list, key=lambda x: x[1])
for entry in list_sorted:
    print(entry)


print(len(list_sorted))
ignore_limit = 1000
values = [item for item in list_sorted if item[1] > ignore_limit]
for value in values:
    list_sorted.remove(value)
print(len(list_sorted))
plt.bar([str(item[0]) for item in list_sorted], [item[1] for item in list_sorted])
plt.xticks(rotation="vertical")
plt.title("Users vs. transcribed entries (excluding users with more than {} entries)".format(ignore_limit))
plt.show()

num_lost = sum([item[1] for item in list_sorted])
print("Amount of transcriptions made by users with less than {} transcriptions: ".format(ignore_limit) + str(num_lost))
