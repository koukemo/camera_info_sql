from sql_operations.sql_operation import SqlShow


def main():
    table_name = 'json_tables'
    SqlShow.show_table_data(table_name)


if __name__ == "__main__":
    main()
