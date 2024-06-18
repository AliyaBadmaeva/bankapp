import tkinter as tk  # импортируем встроенную библиотеку tkinter
import os.path  # для работы с файлами
from tkinter.scrolledtext import ScrolledText  # для работы с текстовым полем - текст с прокруткой по вертикали


class BankModel:  # модель банка
    def __init__(self, root, clients):  # инициализация объекта
        self.clients = clients  # инициализация клиентов
        self.root = root  # инициализация окна

    def get_clients(self, name):  # получение баланса клиента
        return self.clients[name]  # возвращает баланс клиента

    def add_client(self, name, summa):  # добавление нового клиента
        self.clients[name] = summa  # добавляет нового клиента с балансом

    def set_clients(self, fun, name, summa):  # изменение баланса клиента
        if fun == "DEPOSIT":  # если функция DEPOSIT
            self.clients[name] = self.clients.setdefault(name, 0) + int(summa)  # то увеличиваем баланс
        elif fun == "WITHDRAW":  # если функция WITHDRAW
            self.clients[name] = self.clients.setdefault(name, 0) - int(summa)  # то уменьшаем баланс

    def error(self, fun):  # обработка ошибок
        return f'ОШИБКА: {fun}\n    ВВЕДИТЕ ИМЯ КЛИЕНТА ИЛИ СУММУ\n>>>'  # возвращает сообщение об ошибке

    def get_result(self, fun, name, summa):  # получение результата
        return f'{fun} {name} {summa}\n    {name} {self.get_clients(name)}\n>>>'  # возвращает результат

    def deposit(self, name="", summa=0, fun="DEPOSIT"):  # функция внесения денег - депозита
        if name == '':  # если имя пустое
            return self.error(fun)  # то возвращает сообщение об ошибке
        else:  # иначе
            self.set_clients(fun, name, summa)  # то изменяем баланс
            return self.get_result(fun, name, summa)  # возвращает результат

    def withdraw(self, name="", summa=0, fun="WITHDRAW"):  # функция снятия денег
        if name == '':  # если имя пустое
            return self.error(fun)  # то возвращает сообщение об ошибке
        else:  # иначе
            self.set_clients(fun, name, summa)  # то изменяем баланс
            return self.get_result(fun, name, summa)  # возвращает результат

    def balance(self, name="", fun="BALANCE", s=""):  # функция баланса
        if name == '':  # если имя пустое
            a = s
            i = 0  # счётчик
            for key, value in self.clients.items():  # цикл по всем клиентам
                if i > 0:  # если счётчик больше нуля
                    a += '\n'  # то переход на новую строку
                a += f'{fun} {key} {value}\n>>>'  # выводим имя и баланс клиента
                i += 1  # увеличиваем счётчик
            return a  # возвращаем результат - всех клиентов с балансом
        elif name in self.clients:  # если такой клиент есть
            return f'{fun} {name}\n    {name} {self.get_clients(name)}\n>>>'  # то выводим имя и баланс
        else:  # иначе если такого клиента нет
            return f'{fun} {name}\n    NO CLIENT\n>>>'  # то выводим сообщение об ошибке

    def transfer(self, name_from, name_to, summa):  # функция перевода денег
        s = ""
        s += self.withdraw(name_from, summa)  # снимаем деньги с первого клиента
        s += self.deposit(name_to, summa)  # зачисляем деньги второму клиенту
        return s

    def income(self, percent, fun="INCOME"):  # функция начисления процентов
        if percent == 0:  # если процент равен нулю
            return f'ОШИБКА: {fun}\n    ВВЕДИТЕ ПРОЦЕНТ\n>>>'  # то возвращает сообщение об ошибке
        for name, summa in self.clients.items():  # цикл по всем клиентам
            if summa > 0:  # если баланс больше нуля
                # начисляем проценты
                self.clients[name] = int(self.clients.get(name) + int(summa) * float(percent) // 100)
        s = f'{fun} {percent}\n>>>\n'  # выводим команду
        for key, value in self.clients.items():  # цикл по всем клиентам
            return self.balance(name="", fun="BALANCE", s=s)  # возвращаем результат - всех клиентов с балансом


class BankView:  # Класс представления
    def __init__(self, model, root):  # инициализация
        self.model = model  # инициализация модели
        self.root = root  # инициализация окна
        self.canvas = tk.Canvas(root, width=850, height=800)  # инициализация холста
        self.canvas.grid(row=0, columnspan=10)  # расположение холста

    def create_labels(self):  # функция создания меток
        self.canvas.delete("all")  # очистка холста
        label_1 = tk.Label(self.canvas, text='Введите команду', font='Arial 10')  # создадим текстовую метку
        label_1.place(y=10, x=10)  # местоположение
        label_result = tk.Label(self.canvas, text='Результат', font='Arial 10')  # этикетка перед полем с результатом
        label_result.place(y=300, x=10)  # местоположение
        # этикетка для загрузки данных из файла
        label_2 = tk.Label(self.canvas, text='Введите название текстового файла для загрузки, например, "source.txt"',
                           font='Arial 10')
        label_2.place(y=600, x=10)  # местоположение


class BankController:  # контроллер
    def __init__(self, model, view):  # инициализация объекта
        self.model = model  # модель
        self.view = view  # визуальное представление

    def load(self):  # загрузка программы
        self.view.create_labels()  # отрисовка начального состояния
        self.create_buttons_and_inputs()  # создание кнопок и полей ввода

    def get_length_result(self, result, s):  # функция подсчета длины строки
        ln = len(result.get("1.0", "end"))  # считаем длину строки
        if ln > 1:  # если строка не пустая
            # добавляем строку в конец текстового файла со знаком переноса перед строкой
            result.insert(tk.END, f'\n{s}')
        else:
            result.insert("1.0", s)  # вставляем строку в начало

    def start(self, words, result):  # функция запуска программы
        inputs = words.get("1.0", tk.END)  # считываем введенные данные
        lines = inputs.splitlines()  # разделяем на строки
        functions = ['DEPOSIT', 'WITHDRAW', 'BALANCE', 'TRANSFER', 'INCOME']  # список команд
        for line in lines:  # цикл по всем строкам
            if line:  # если не пустая строка
                line = line.split()  # разделяем на слова
                if line[0] in functions:  # если первое слово - команда из списка
                    index = functions.index(line[0])    # находим индекс команды
                    if index == 0:  # если команда DEPOSIT
                        try:  # обработка исключений
                            s = self.model.deposit(line[1], line[2])  # вызываем функцию депозит
                        except IndexError:  # если не хватает аргументов
                            s = self.model.deposit("")  # вызываем функцию депозит с пустым аргументом
                    elif index == 1:  # если команда WITHDRAW
                        try:  # обработка исключений
                            s = self.model.withdraw(line[1], line[2])  # вызываем функцию вывода
                        except IndexError:  # если не хватает аргументов
                            s = self.model.withdraw("")  # вызываем функцию вывода с пустым аргументом
                    elif index == 2:  # если команда BALANCE
                        try:  # обработка исключений
                            s = self.model.balance(line[1])  # вызываем функцию баланс
                        except IndexError:  # если не хватает аргументов
                            s = self.model.balance("")  # вызываем функцию баланс с пустым аргументом
                    elif index == 3:  # если команда TRANSFER
                        try:  # обработка исключений
                            s = self.model.transfer(line[1], line[2], line[3])  # вызываем функцию перевода
                        except IndexError:  # если не хватает аргументов
                            s = self.model.transfer("", "", 0)  # вызываем функцию перевода с пустыми аргументами
                    elif index == 4:  # если команда INCOME
                        try:  # обработка исключений
                            s = self.model.income(line[1])  # вызываем функцию начисления процентов
                        except IndexError:  # если не хватает аргументов
                            s = self.model.income(0)  # вызываем функцию начисления процентов с пустым аргументом
                    self.get_length_result(result, s)  # вызываем функцию подсчета длины
                else:  # если команда не найдена
                    # печатаем этикетку
                    label_s = tk.Label(self.view.root, text=f'Проверьте правильность ввода. Такая команда {line[0]} '
                                                            f'не найдена', font="times 12")
                    label_s.place(x=100, y=300)  # местоположение
                    label_s.after(1000, label_s.destroy)  # удалить этикетку через секунду
            else:  # если строка пустая
                label_s = tk.Label(self.view.root, text='Поле ввода не может быть пустым', font="times 12")
                label_s.place(x=100, y=300)  # местоположение
                label_s.after(1000, label_s.destroy)  # удалить этикетку через секунду

    def read_text(self, name, words):  # функция для чтения файла
        if os.path.exists(name):  # если файл существует
            with open(name, 'r') as source:  # открываем его
                source_lines = source.readlines()  # считываем все строки
                if len(source_lines) >= 1:  # если в файле есть строки
                    for line in source_lines:  # перебираем все строки
                        words.insert(tk.END, line)  # вставляем строку в поле ввода
                else:  # если в файле нет строк
                    # печатаем этикетку
                    label_check_txt = tk.Label(self.view.root, text='Файл пуст', font="times 12")
                    label_check_txt.place(x=10, y=690)  # местоположение
                    label_check_txt.after(1000, label_check_txt.destroy)  # удалить этикетку через секунду
        else:  # если файл не существует
            label_check_txt = tk.Label(self.view.root, text='Файл не существует, проверьте название', font="times 12")
            label_check_txt.place(x=10, y=690)  # местоположение
            label_check_txt.after(1000, label_check_txt.destroy)  # удалить этикетку через секунду

    def get_text(self, entryv, words):  # функция для получения названия
        e = entryv.get()  # получаем название из поля ввода
        if e.endswith(".txt"):  # если название оканчивается на расширение .txt
            self.read_text(e, words)  # вызываем функцию для чтения файла
        else:  # если название не оканчивается на расширение .txt
            # печатаем этикетку
            label_check = tk.Label(self.view.root, text='Проверьте название текстового документа', font="times 12")
            label_check.place(x=10, y=690)  # местоположение
            label_check.after(1000, label_check.destroy)  # удалить этикетку через секунду

    def create_buttons_and_inputs(self):
        # многострочное текстовое поле для ввода команд пользователя
        words = ScrolledText(self.view.root, width=50, height=7, wrap='word', font='arial 20')
        words.place(x=10, y=30)  # местоположение
        # многострочное текстовое поле для вывода результата
        result = ScrolledText(self.view.root, width=50, height=7, wrap='word', font='arial 20')
        result.place(x=10, y=330)  # местоположение
        # Кнопка для расчёта
        calculate = tk.Button(self.view.root, width=10, height=1, bg='green', fg='white', text='Расчёт',
                              font='arial 10', command=lambda: self.start(words, result))
        calculate.place(y=270, x=350)  # местоположение
        # Кнопка для очистки поля ввода команд
        clear_btn = tk.Button(self.view.root, width=10, height=1, bg='red', fg='white', text='Очистить',
                              font='arial 10', command=lambda: words.delete('1.0', tk.END))
        clear_btn.place(y=270, x=250)  # местоположение
        # Кнопка для очистки многострочного текстового поля с результатом
        clear_result = tk.Button(self.view.root, width=10, height=1, bg='red', fg='white', text='Очистить',
                                 font='arial 10', command=lambda: result.delete('1.0', tk.END))
        clear_result.place(y=570, x=300)  # местоположение
        # однострочное поле для ввода названия файла
        entry = tk.StringVar()  # строка
        entryv = tk.Entry(self.view.root, width=125, textvariable=entry)  # однострочное поле
        entryv.place(y=630, x=10)  # местоположение
        # Кнопка для загрузки
        btn_dwnld = tk.Button(self.view.root, width=10, height=1, bg='purple', fg='white', text="Загрузить",
                              command=lambda: self.get_text(entryv, words))
        btn_dwnld.place(y=660, x=250)  # местоположение
        # Кнопка для очистки поля от названия файла
        btn_clear = tk.Button(self.view.root, width=10, height=1, bg='red', fg='white', text="Очистить",
                              command=lambda: entry.set(""))
        btn_clear.place(y=660, x=350)  # местоположение


def main():  # основная функция
    root = tk.Tk()  # создаем окно - корневой объект
    root.title("Задание 2 - Система управления банковскими счетами клиентов")  # озаглавим окно
    model = BankModel(root, {'Badmaeva': 70196629})  # инициализация модели
    view = BankView(model, root)  # инициализация представления
    controller = BankController(model, view)  # инициализация контроллера
    controller.load()  # запуск программы
    root.mainloop()  # запуск основного цикла


if __name__ == "__main__":  # основная функция
    main()  # запуск основной функции
