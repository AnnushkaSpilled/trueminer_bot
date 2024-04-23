import os
from typing import Dict, List, Tuple

import sqlite3

connection = sqlite3.connect('E:/sqllite/databases/test.db', check_same_thread=False)
cursor = connection.cursor()


def get_names(what, where):
    cursor.execute(f"SELECT {what} FROM {where}")
    data = cursor.fetchall()
    return data


def get_lists(table):
    cursor.execute(f"SELECT * FROM {table}")
    items_list = cursor.fetchall()
    return items_list


def get_last_ten(table):
    cursor.execute(f"SELECT {table}come.{table}come_id, {table}come.date, project.project_name, {table}come_cat.{table}_cat_name, {table}come.value\n"
                   f"FROM {table}come, project, {table}come_cat\n"
                   f"WHERE {table}come.project_id = project.project_id AND {table}come.{table}come_cat_id = {table}come_cat.{table}_cat_id\n"
                   f"ORDER BY {table}come.{table}come_id DESC LIMIT 10")
    last_ten = cursor.fetchall()
    return last_ten


def delete(table, operation_id):
    cursor.execute(f"DELETE FROM {table}come WHERE {table}come_id={operation_id}")
    connection.commit()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    connection.commit()

