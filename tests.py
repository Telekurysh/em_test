import unittest
import datetime

from main import Account, Record


class TestAccount(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый файл с данными
        with open('test_data.txt', 'w') as file:
            file.write("Дата: 2024-05-02\n")
            file.write("Категория: Расход\n")
            file.write("Сумма: 1500\n")
            file.write("Описание: Покупка продуктов\n\n")
            file.write("Дата: 2024-05-03\n")
            file.write("Категория: Доход\n")
            file.write("Сумма: 30000\n")
            file.write("Описание: Зарплата\n\n")

    def test_load_records(self):
        # Проверяем загрузку записей из файла
        account = Account('test_data.txt')
        account.load_records()
        self.assertEqual(len(account.records), 2)

    def test_add_record(self):
        # Проверяем добавление новой записи
        account = Account('test_data.txt')
        account.load_records()
        initial_count = len(account.records)
        account.add_record(datetime.datetime(2024, 5, 4), 'Расход', 500, 'Покупка книг')
        self.assertEqual(len(account.records), initial_count + 1)

    def test_edit_record(self):
        # Проверяем редактирование существующей записи
        account = Account('test_data.txt')
        account.load_records()
        old_description = account.records[0].description
        account.edit_record(0, account.records[0].date, account.records[0].category, 2000, 'Новое описание')
        self.assertNotEqual(account.records[0].description, old_description)

    def test_search_records(self):
        # Проверяем поиск записей по категории
        account = Account('test_data.txt')
        account.load_records()
        search_results = account.search_records(category='Расход')
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].category, 'Расход')

    def test_calculate_balance(self):
        # Проверяем расчет баланса
        account = Account('test_data.txt')
        account.load_records()
        balance = account.calculate_balance()
        self.assertEqual(balance, 30000 - 1500)

    def tearDown(self):
        # Удаляем тестовый файл с данными после завершения тестов
        import os
        os.remove('test_data.txt')


if __name__ == '__main__':
    unittest.main()
