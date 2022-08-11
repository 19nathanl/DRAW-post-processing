import database_connection as db
import sql_commands as sql


###     RUN THIS FILE TO CREATE COMPOSITE RAW DATA TABLE FROM DATA ENTRIES, FIELDS AND ANNOTATIONS TABLES.        ###
###     CREATING THIS RAW DATA TABLE IS NECESSARY BECAUSE IT ALLOWS THE ADDITION OF MYSQL INDEXES, WHICH          ###
###     SPEEDS UP CODE CONSIDERABLY DURING POST-PROCESSING RUNTIME.                                               ###

db = db.db
cursor = db.cursor()


def create_raw_data_entries():
    cursor.execute(sql.composite_raw_data_entries)
    # TODO : add indexes here
