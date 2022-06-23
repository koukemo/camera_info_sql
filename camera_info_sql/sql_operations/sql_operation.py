import mysql.connector
import json
import os
import rosidl_runtime_py

from camera_info_sql.sql_operations.config import config


class SqlGetdata:
    @staticmethod
    def get_all_tables():
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        cursor.execute("SHOW TABLES")

        all_tables = ()
        for table in cursor:
            all_tables = all_tables + table
        cursor.close()
        return all_tables

    @staticmethod
    def get_json_data(table_name: str, column: str = "*"):
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        sql = "SELECT {} FROM {};"
        cursor.execute(sql.format(column, table_name))

        json_datas = {}
        for data in cursor:
            json_datas[data[0]] = json.loads(data[1])
        cursor.close()
        return json_datas


class SqlInsert:
    @staticmethod
    def insert_json_tables(data):
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        json_data = JsonOperation.ros_msg_to_json(data)

        sql = "INSERT INTO json_tables(json_datas) VALUES (%s)"
        cursor.execute(sql, (json_data,))
        ctx.commit()
        ctx.close()


class SqlShow:
    @staticmethod
    def show_all_tables():
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        cursor.execute("SHOW TABLES")

        for table in cursor:
            print(table[0])
        cursor.close()

    @staticmethod
    def show_table_data(table_name: str, column: str = "*"):
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        sql = "SELECT {} FROM {};"
        cursor.execute(sql.format(column, table_name))

        print("table :", table_name)
        for data in cursor:
            print(data)
        cursor.close()


class SqlDelete:
    @staticmethod
    def delete_all_table():
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        tables = SqlGetdata.get_all_tables()

        for table in tables:
            if table == "schema_migrations":
                continue
            sql = "TRUNCATE TABLE {};"
            cursor.execute(sql.format(table))
            ctx.commit()
        print("All data in the created table has been deleted!")
        cursor.close()


class JsonOperation:
    @staticmethod
    def ros_msg_to_json(msg_data):
        dict_data = rosidl_runtime_py.message_to_ordereddict(msg_data)
        json_data = json.dumps(dict_data, indent=2)

        return json_data

    @staticmethod
    def write_json_from_ros_msg(msg_data, save_dir_path: str, save_file_name: str = "camera_info_from_msg"):
        dict_data = rosidl_runtime_py.message_to_ordereddict(msg_data)
        with open(os.path.join(save_dir_path, save_file_name) + '.json', 'w') as f:
            json.dump(dict_data, f, indent=2)

    @staticmethod
    def create_json_from_sql(save_dir_path: str):
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        json_data = SqlGetdata.get_json_data("json_tables")

        for key, value in json_data.items():
            save_file_name = "camera_info_from_sql_" + str(key)
            with open(os.path.join(save_dir_path, save_file_name) + '.json', 'w') as f:
                json.dump(value, f, indent=2)
