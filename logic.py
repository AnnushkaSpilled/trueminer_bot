import datetime
from datetime import timedelta
import db


class WrongMsgError(Exception):
    pass


class WrongProject(Exception):
    pass


class WrongCategory(Exception):
    pass


def parse_message(message):
    #Распознает сообщение
    data = message.text.split(" ")
    try:
        date_ind = int(data[0])
        project_id = int(data[1])
        operation = str(data[2])
        category_id = int(data[3])
        amount = int(data[4])
        parsed_data = (date_ind, project_id, operation, category_id, amount)
        print(data)
        return parsed_data
    except (ValueError, IndexError):
        raise WrongMsgError("Не могу понять сообщение.")


def date_rec(date_ind):
    # Определяет дату операции
    if date_ind == 0:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.now() + timedelta(days=date_ind)
    return str(date)[:-7]


def project_rec(project_id):
    # Определяет имя проекта
    try:
        projects = db.get_names('project_name', 'project')
        project_name = str(projects[int(project_id) - 1])
        pretty_project_name = project_name.replace("'", '').replace('(', '').replace(')', '').replace(',', '')
        print(pretty_project_name)
        return pretty_project_name
    except IndexError:
        raise WrongProject(f"Некорректный идентификатор проекта.\n"
                           f"Такого проекта не существует.\n"
                           f"Cписок проектов /projects")


def operation_rec(operation):
    # Определяет тип операции
    if operation == "+":
        table = "in"
        operation_type = "доход"
        return table, operation_type
    elif operation == "-":
        table = "out"
        operation_type = "расход"
        return table, operation_type


def category_rec(category_id, operation_type):
    # Определяет имя категории
    try:
        categories = db.get_names(f"{operation_type}_cat_name", f"{operation_type}come_cat")
        category_name = str(categories[int(category_id) - 1])
        pretty_category_name = category_name.replace("'", '').replace('(', '').replace(')', '').replace(',', '')
        return pretty_category_name
    except IndexError:
        raise WrongCategory(f"Некорректный идентификатор категории.\n"
                            f"Такой категории дохода/расхода не существует.\n"
                            f"Список статей доходов /in, статей расходов /out")


def rec_message(parsed_data):
    # Делает в БД запись об операции
        date = date_rec(parsed_data[0])
        project_name = project_rec(parsed_data[1])
        operation_table = operation_rec(parsed_data[2])[0]
        operation_type = operation_rec(parsed_data[2])[1]
        category_name = str(category_rec(parsed_data[3], operation_table))
        amount = parsed_data[4]
        db.insert(f"{operation_table}come", {
            "date": date,
            "project_id": parsed_data[1],
            f"{operation_table}come_cat_id": parsed_data[3],
            "value": amount})
        return (f"Добавлена запись о {operation_type}е от {date} на сумму {amount} рублей\n"
                f"Проект: {str(project_name)}\n"
                f"Категория: {str(category_name)}")


def delete_row(table, row_id):
    #Удаляет запись из БД
    db.delete(table, row_id)


def call_lists(table):
    #Вызывает списки данных
    called_list = db.get_lists(table)
    return called_list


def call_last_ten(table):
    #Вызывает 10 последних записей
    called_last_ten = db.get_last_ten(table)
    return called_last_ten




