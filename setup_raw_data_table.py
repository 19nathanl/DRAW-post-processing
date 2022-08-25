import tables
import config


def set_up_raw_data_table():
    tables.add_ppid_column_fields_table()
    tables.update_fields_ppid(1, config.ppid_to_field_id[1])
    tables.update_fields_ppid(2, config.ppid_to_field_id[2])
    tables.update_fields_ppid(3, config.ppid_to_field_id[3])
    # TODO : update other field id's with their respective pp_id

    tables.create_raw_data_table()
