import datetime


class Record:
    """
    Класс Record представляет отдельную запись о доходе или расходе.
    """

    def __init__(self, date, category, amount, description):
        """
        Инициализирует объект Record с заданной датой, категорией, суммой и описанием.

        :param date: Дата записи (datetime.datetime).
        :param category: Категория записи (строка).
        :param amount: Сумма записи (число).
        :param description: Описание записи (строка).
        """
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


class Account:
    """
    Класс Account представляет собой учетную запись, управляющую всеми записями доходов и расходов.
    """

    def __init__(self, filename):
        """
        Инициализирует объект Account с указанием имени файла для хранения данных.

        :param filename: Имя файла для хранения данных (строка).
        """
        self.filename = filename
        self.records = []

    def load_records(self):
        """
        Загружает записи из файла данных в список записей учетной записи.
        """
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            record_info = {}
            for line in lines:
                if line.strip():
                    key, value = line.split(': ')
                    record_info[key.strip()] = value.strip()
                else:
                    record = Record(datetime.datetime.strptime(record_info['Дата'], '%Y-%m-%d'),
                                    record_info['Категория'],
                                    float(record_info['Сумма']),
                                    record_info['Описание'])
                    self.records.append(record)
                    record_info = {}

    def save_records(self):
        """
        Сохраняет записи из списка записей учетной записи в файл данных.
        """
        with open(self.filename, 'w') as file:
            for record in self.records:
                file.write(f"Дата: {record.date.strftime('%Y-%m-%d')}\n")
                file.write(f"Категория: {record.category}\n")
                file.write(f"Сумма: {record.amount}\n")
                file.write(f"Описание: {record.description}\n\n")

    def add_record(self, date, category, amount, description):
        """
        Добавляет новую запись о доходе или расходе в список записей учетной записи.

        :param date: Дата записи (datetime.datetime).
        :param category: Категория записи (строка).
        :param amount: Сумма записи (число).
        :param description: Описание записи (строка).
        """

        record = Record(date, category, amount, description)
        self.records.append(record)

    def edit_record(self, index, date, category, amount, description):
        """
        Изменяет существующую запись о доходе или расходе в списке записей учетной записи.

        :param index: Индекс записи для редактирования (число).
        :param date: Новая дата записи (datetime.datetime).
        :param category: Новая категория записи (строка).
        :param amount: Новая сумма записи (число).
        :param description: Новое описание записи (строка).
        :return: True, если редактирование успешно, иначе False.
        """

        if 0 <= index < len(self.records):
            self.records[index].date = date
            self.records[index].category = category
            self.records[index].amount = amount
            self.records[index].description = description
            return True
        return False

    def search_records(self, category=None, start_date=None, end_date=None, min_amount=None, max_amount=None):
        """
        Ищет записи в списке записей учетной записи по заданным критериям.

        :param category: Категория для поиска (строка).
        :param start_date: Начальная дата для поиска (datetime.datetime).
        :param end_date: Конечная дата для поиска (datetime.datetime).
        :param min_amount: Минимальная сумма для поиска (число).
        :param max_amount: Максимальная сумма для поиска (число).
        :return: Список записей, удовлетворяющих заданным критериям.
        """
        results = []
        for record in self.records:
            if (category is None or record.category == category) and \
                    (start_date is None or record.date >= start_date) and \
                    (end_date is None or record.date <= end_date) and \
                    (min_amount is None or record.amount >= min_amount) and \
                    (max_amount is None or record.amount <= max_amount):
                results.append(record)
        return results

    def calculate_balance(self):
        """
        Вычисляет текущий баланс на основе записей о доходах и расходах.

        :return: Текущий баланс (число).
        """
        income = sum(record.amount for record in self.records if record.category == 'Доход')
        expenses = sum(record.amount for record in self.records if record.category == 'Расход')
        return income - expenses
