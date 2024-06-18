import tkinter as tk  # import tkinter
import os.path  # for working with files
from tkinter.scrolledtext import ScrolledText  # for working with a text field - text with vertical scrolling


class BankModel:  # Model
    def __init__(self, root, clients):  # object initialization
        self.clients = clients  # client initialization
        self.root = root  # window initialization

    def get_clients(self, name):  # get client balance
        return self.clients[name]  # returns the client's balance

    def add_client(self, name, summa):  # adding a new client
        self.clients[name] = summa  # adds a new client with balance

    def set_clients(self, fun, name, summa):  # client balance change
        if fun == "DEPOSIT":  # if DEPOSIT function
            self.clients[name] = self.clients.setdefault(name, 0) + int(summa)  # increase the balance
        elif fun == "WITHDRAW":  # if WITHDRAW function
            self.clients[name] = self.clients.setdefault(name, 0) - int(summa)  # decrease the balance

    def error(self, fun):  # error processing
        return f'ERROR: {fun}\n    ENTER CUSTOMER NAME OR AMOUNT\n>>>'  # returns an error message

    def get_result(self, fun, name, summa):  # getting the result
        return f'{fun} {name} {summa}\n    {name} {self.get_clients(name)}\n>>>'  # returns the result

    def deposit(self, name="", summa=0, fun="DEPOSIT"):  # money deposit function
        if name == '':  # if the name is empty
            return self.error(fun)  # then returns an error message
        else: 
            self.set_clients(fun, name, summa)  # then changing the balance
            return self.get_result(fun, name, summa)  # returns the result

    def withdraw(self, name="", summa=0, fun="WITHDRAW"):  # money withdrawal function
        if name == '':  # if the name is empty
            return self.error(fun)  # then returns an error message
        else:  # иначе
            self.set_clients(fun, name, summa)  # then changing the balance
            return self.get_result(fun, name, summa)  # returns the result

    def balance(self, name="", fun="BALANCE", s=""):  # BALANCE function
        if name == '':  # if the name is empty
            a = s
            i = 0  # counter
            for key, value in self.clients.items():  # cycle for all clients
                if i > 0:  # if the counter is greater than zero
                    a += '\n'  # then go to new line
                a += f'{fun} {key} {value}\n>>>'  # display the client's name and balance
                i += 1  # increase the counter
            return a  # return the result - all clients with a balance
        elif name in self.clients:  # if such client exists
            return f'{fun} {name}\n    {name} {self.get_clients(name)}\n>>>'  # then displaying the name and balance
        else:  # otherwise if there is no such client
            return f'{fun} {name}\n    NO CLIENT\n>>>'  # display an error message

    def transfer(self, name_from, name_to, summa):  # money transfer function
        s = ""
        s += self.withdraw(name_from, summa)  # withdraw money from the first client
        s += self.deposit(name_to, summa)  # transfer money to the second client
        return s

    def income(self, percent, fun="INCOME"):  # INCOME (interest) function
        if percent == 0:  # if the percentage is zero
            return f'ERROR: {fun}\n    ENTER PERCENTAGE\n>>>'  # then returns an error message
        for name, summa in self.clients.items():  # cycle for all clients
            if summa > 0:  # if the balance is greater than zero
                # charge interest
                self.clients[name] = int(self.clients.get(name) + int(summa) * float(percent) // 100)
        s = f'{fun} {percent}\n>>>\n'  # print the command
        for key, value in self.clients.items():  # cycle for all clients
            return self.balance(name="", fun="BALANCE", s=s)  # return the result - all clients with a balance


class BankView:  # View Class
    def __init__(self, model, root):  # inizialisation
        self.model = model  # model initialization
        self.root = root  # window initialization
        self.canvas = tk.Canvas(root, width=850, height=800)  # canvas initialization
        self.canvas.grid(row=0, columnspan=10)  # canvas layout

    def create_labels(self):  # label creation function
        self.canvas.delete("all")  # clearing canvas
        label_1 = tk.Label(self.canvas, text='Enter the command', font='Arial 10')  # create a text label
        label_1.place(y=10, x=10)  # location
        label_result = tk.Label(self.canvas, text='Result', font='Arial 10')  # label in front of the result field
        label_result.place(y=300, x=10)  # location
        # label for loading data from file
        label_2 = tk.Label(self.canvas, text='Enter the name of the text file to upload, for instance: "source.txt"',
                           font='Arial 10')
        label_2.place(y=600, x=10)  # location


class BankController:  # Controller Class
    def __init__(self, model, view):  # objext inizialisation
        self.model = model  # model inizialisation
        self.view = view  # view inizialisation

    def load(self):  # loading
        self.view.create_labels()  # drawing the initial state
        self.create_buttons_and_inputs()  # creating buttons and input fields

    def get_length_result(self, result, s):  # string length counting function
        ln = len(result.get("1.0", "end"))  # count the length of the string
        if ln > 1:  # if the string is not empty
            # add a line to the end of the text file with a hyphen before the line
            result.insert(tk.END, f'\n{s}')
        else:
            result.insert("1.0", s)  # insert the line at the beginning

    def start(self, words, result):  # program launch function
        inputs = words.get("1.0", tk.END)  # read the entered data
        lines = inputs.splitlines()  # split into lines
        functions = ['DEPOSIT', 'WITHDRAW', 'BALANCE', 'TRANSFER', 'INCOME']  # list of commands
        for line in lines:  # loop through all lines
            if line:  # if not empty string
                line = line.split()  # split into words
                if line[0] in functions:  # if the first word is a command from the list
                    index = functions.index(line[0])  # find the command index
                    if index == 0:  # if DEPOSIT command
                        try:  # Exception Handling
                            s = self.model.deposit(line[1], line[2])  # call the DEPOSIT function
                        except IndexError:  # if there are not enough arguments
                            s = self.model.deposit("")  # call the deposit function with an empty argument
                    elif index == 1:  # if WITHDRAW command
                        try:  # Exception Handling
                            s = self.model.withdraw(line[1], line[2])  # call the WITHDRAW function
                        except IndexError:  # if there are not enough arguments
                            s = self.model.withdraw("")  # call the function with an empty argument
                    elif index == 2:  # if BALANCE command
                        try:  # Exception Handling
                            s = self.model.balance(line[1])  # call the BALANCE
                        except IndexError:  # if there are not enough arguments
                            s = self.model.balance("")  # call the function with an empty argument
                    elif index == 3:  # if TRANSFER command
                        try:  # Exception Handling
                            s = self.model.transfer(line[1], line[2], line[3])  # call the TRANSFER function
                        except IndexError:  # if there are not enough arguments
                            s = self.model.transfer("", "", 0)  # call the function with an empty argument
                    elif index == 4:  # if INCOME command
                        try:  # Exception Handling
                            s = self.model.income(line[1])  # call the INCOME function
                        except IndexError:  # if there are not enough arguments
                            s = self.model.income(0)  # call the function with an empty argument
                    self.get_length_result(result, s)  # call the length calculation function
                else:  # if the command is not found
                    # print label
                    label_s = tk.Label(self.view.root, text=f'Please check if your entry is correct. Such a command {line[0]} '
                                                            f'was not found', font="times 12")
                    label_s.place(x=100, y=300)  # location
                    label_s.after(1000, label_s.destroy)  # remove the label after a second
            else:  # if the line is empty
                label_s = tk.Label(self.view.root, text='The input field cannot be empty', font="times 12")
                label_s.place(x=100, y=300)  # location
                label_s.after(1000, label_s.destroy)  # remove the label after a second

    def read_text(self, name, words):  # function to read a file
        if os.path.exists(name):  # if the file exists
            with open(name, 'r') as source:  # open it
                source_lines = source.readlines()  # read all lines
                if len(source_lines) >= 1:  # if there are lines in the file
                    for line in source_lines:  # iterate over all lines
                        words.insert(tk.END, line)  # insert a string into the input field
                else:  # if there are no lines in the file
                    # print label
                    label_check_txt = tk.Label(self.view.root, text='The file is empty', font="times 12")
                    label_check_txt.place(x=10, y=690)  # location
                    label_check_txt.after(1000, label_check_txt.destroy)  # remove the label after a second
        else:  # if the file does not exist
            label_check_txt = tk.Label(self.view.root, text='File does not exist, check the name', font="times 12")
            label_check_txt.place(x=10, y=690)  # location
            label_check_txt.after(1000, label_check_txt.destroy)  # remove the label after a second

    def get_text(self, entryv, words):  # function to get the name
        e = entryv.get()  # get the name from the input field
        if e.endswith(".txt"):  # if the name ends with .txt
            self.read_text(e, words)  # call the function to read the file
        else:  # if the name does not end with .txt
            # print the label
            label_check = tk.Label(self.view.root, text='Check the title of the text document', font="times 12")
            label_check.place(x=10, y=690)  # location
            label_check.after(1000, label_check.destroy)  # remove the label after a second

    def create_buttons_and_inputs(self):
        # multi-line text field for entering user commands
        words = ScrolledText(self.view.root, width=50, height=7, wrap='word', font='arial 20')
        words.place(x=10, y=30)  # location
        # multiline text field to display the result
        result = ScrolledText(self.view.root, width=50, height=7, wrap='word', font='arial 20')
        result.place(x=10, y=330)  # location
        # Button for calculation
        calculate = tk.Button(self.view.root, width=10, height=1, bg='green', fg='white', text='Result',
                              font='arial 10', command=lambda: self.start(words, result))
        calculate.place(y=270, x=350)  # location
        # Button to clear the command input field
        clear_btn = tk.Button(self.view.root, width=10, height=1, bg='red', fg='white', text='Clear',
                              font='arial 10', command=lambda: words.delete('1.0', tk.END))
        clear_btn.place(y=270, x=250)  # location
        # Button to clear a multi-line text field with the result
        clear_result = tk.Button(self.view.root, width=10, height=1, bg='red', fg='white', text='Clear',
                                 font='arial 10', command=lambda: result.delete('1.0', tk.END))
        clear_result.place(y=570, x=300)  # location
        # entry field for entering the file name
        entry = tk.StringVar()  # string
        entryv = tk.Entry(self.view.root, width=125, textvariable=entry)  # entry field
        entryv.place(y=630, x=10)  # location
        # Download button
        btn_dwnld = tk.Button(self.view.root, width=10, height=1, bg='purple', fg='white', text="Download",
                              command=lambda: self.get_text(entryv, words))
        btn_dwnld.place(y=660, x=250)  # location
        # Button to clear the field from the file name
        btn_clear = tk.Button(self.view.root, width=10, height=1, bg='red', fg='white', text="Clear",
                              command=lambda: entry.set(""))
        btn_clear.place(y=660, x=350)  # location


def main():  # main function
    root = tk.Tk()  # create a window - root object
    root.title("Client bank account management system")  # let's title the window
    model = BankModel(root, {'Alisa': 59302859})  # model initialization
    view = BankView(model, root)  # view initialization
    controller = BankController(model, view)  # controller initialization
    controller.load()  # program launch
    root.mainloop()  # starting the main loop


if __name__ == "__main__":  # main function
    main()  # running the main function
