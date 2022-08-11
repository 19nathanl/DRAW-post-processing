# This file is used to determine the average fluctuation of pressure over short periods of time
import config
import database_connection as db
import statistics as stats
import calendar

db = db.db
cursor = db.cursor()


def num_to_month(num):
    num_list = [i for i in range(1, 13)]
    name_list = [calendar.month_name[i] for i in range(1, 13)]
    index = num_list.index(num)
    return name_list[index]


def pressure_fluctuations_1879():
    monthly_fluctuation_stats = {}
    for i in range(1, 13):
        month = str(i)
        if i < 10:
            month = '0{}'.format(i)
        sql_command = "SELECT value, observation_date FROM data_entries_corrected_duplicateless " \
                      "WHERE observation_date LIKE '%1879-{}%' " \
                      "AND field_id = 4 " \
                      "AND flagged = 0 " \
                      "ORDER BY observation_date;".format(month)
        cursor.execute(sql_command)
        entries_same_month = cursor.fetchall()
        same_month_scalar = []
        for j in range(1, len(entries_same_month)):
            if str(entries_same_month[j][0]).lower() not in [*config.disregarded_values, 'none']:
                try:
                    delta_pressure = abs(float(entries_same_month[j][0]) - float(entries_same_month[j - 1][0]))
                    delta_time = abs(entries_same_month[j][1].timestamp() - entries_same_month[j - 1][1].timestamp()) / 3600
                    if delta_time > 12:
                        continue
                    if delta_pressure/delta_time > 12 and i == 11:
                        print(j)
                    same_month_scalar.append(delta_pressure / delta_time)
                except ValueError:
                    pass
        print(max(same_month_scalar))
        monthly_fluctuation_stats[i] = "Pressure, on average, changes by an amount of {} inHg every hour in {}. " \
                                       "Standard deviation = {}".format(stats.mean(same_month_scalar), num_to_month(i), stats.stdev(same_month_scalar))
        print("Month {} done.".format(i))

    for stat in monthly_fluctuation_stats:
        print(monthly_fluctuation_stats[stat])


pressure_fluctuations_1879()
