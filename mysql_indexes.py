import database_connection as db

db = db.db
cursor = db.cursor()


def data_entries_raw(index_type, action):
    match index_type:

        case 'annotation':
            match action:
                case 'create':
                    cursor.execute("CREATE INDEX data_entries_raw_annotation_index ON data_entries_raw (annotation_id);")
                case 'delete':
                    cursor.execute("DROP INDEX data_entries_raw_annotation_index ON data_entries_raw;")

        case 'field_date':
            match action:
                case 'create':
                    cursor.execute("CREATE INDEX data_entries_raw_field_date_index ON data_entries_raw (field_id, observation_date);")
                case 'delete':
                    cursor.execute("DROP INDEX data_entries_raw_field_date_index ON data_entries_raw;")

        case 'user':
            match action:
                case 'create':
                    cursor.execute("CREATE INDEX data_entries_raw_user_index ON data_entries_raw (user_id);")
                case 'delete':
                    cursor.execute("DROP INDEX data_entries_raw_user_index ON data_entries_raw;")


def data_entries_corrected(index_type, action):
    match index_type:
        case 'field_date_user':
            match action:
                case 'create':
                    cursor.execute("CREATE INDEX data_entries_corrected_field_date_user_index ON data_entries_corrected (field_id, observation_date, user_id);")
                case 'delete':
                    cursor.execute("DROP INDEX data_entries_corrected_field_date_user_index ON data_entries_corrected;")


def data_entries_corrected_duplicateless(index_type, action):
    match index_type:
        case 'field_date':
            match action:
                case 'create':
                    cursor.execute("CREATE INDEX data_entries_corrected_duplicateless_field_date_index ON data_entries_corrected_duplicateless (field_id, observation_date);")
                case 'delete':
                    cursor.execute("DROP INDEX data_entries_corrected_duplicateless_field_date_index ON data_entries_corrected_duplicateless;")
