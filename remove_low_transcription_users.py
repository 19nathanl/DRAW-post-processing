# This file removes all transcriptions from users in the database that come from users with less than the desired threshold amount of transcriptions
# This is done under the assumption that users that didn't have many transcriptions were much less likely to transcribe correctly.

import database_connection as db

db_conn = db.conn
cursor = db.cursor


def delete_transcriptions():
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()

    threshold = 100
    less_than_threshold_users = []
    for i in users:
        user_id = i[0]
        sql_command = "SELECT COUNT(*) from data_entries_raw " \
                      "WHERE user_id = {};".format(user_id)
        cursor.execute(sql_command)
        num = cursor.fetchall()[0][0]
        if num < threshold:
            less_than_threshold_users.append(user_id)

    delete_transcriptions_sql = "DELETE FROM data_entries_raw WHERE user_id IN {};".format(tuple(less_than_threshold_users))
    cursor.execute(delete_transcriptions_sql)
    db_conn.commit()
