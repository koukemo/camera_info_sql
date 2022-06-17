import mysql
import json
import os

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
            json_datas[data[0]] = json.loads(data[2])
        cursor.close()
        return json_datas


class SqlInsert:
    @staticmethod
    def insert_json_tables(data):
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        json_data = json.dumps(data)

        sql = f"INSERT INTO json_tables(json_datas) VALUES ('{json_data}')"
        cursor.execute(sql)
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
    def camera_info_to_json(camera_info):
        camera_info_shaping = str(camera_info).replace('=', ':')
        camera_info_shaping = camera_info_shaping.replace('sensor_msgs.msg.CameraInfo(', '')
        camera_info_shaping = camera_info_shaping.rstrip()
        camera_info_shaping = camera_info_shaping.replace('std_msgs.msg.Header', '')
        camera_info_shaping = camera_info_shaping.replace('sensor_msgs.msg.RegionOfInterest', '')
        camera_info_shaping = camera_info_shaping.replace('builtin_interfaces.msg.Time', '')
        camera_info_shaping = camera_info_shaping.replace('array', '')
        camera_info_shaping = camera_info_shaping.replace('([', '[{')
        camera_info_shaping = camera_info_shaping.replace('])', '}]')
        camera_info_shaping = camera_info_shaping.replace('(', '{')
        camera_info_shaping = camera_info_shaping.replace(')', '}')
        camera_info_shaping = '{' + camera_info_shaping

        stud_obj = json.loads(camera_info_shaping)

        return json.dumps(stud_obj, indent=4)


    @staticmethod
    def create_json(save_dir_path: str):
        ctx = mysql.connector.connect(**config)
        cursor = ctx.cursor()

        json_data = SqlGetdata.get_json_data("json_tables")

        for key, value in json_data.items():
            save_file_name = "db_json_sample_" + str(key)
            with open(os.path.join(save_dir_path, save_file_name) + '.json', 'w') as f:
                json.dump(value, f, indent=4)