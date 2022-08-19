import tables


def set_up_raw_data_table():
    tables.add_ppid_column_fields_table()
    tables.update_fields_ppid(1, (4, 6, 7, 8, 67, 69))
    # TODO : update other field id's with their respective pp_id

    tables.create_raw_data_table()


set_up_raw_data_table()
