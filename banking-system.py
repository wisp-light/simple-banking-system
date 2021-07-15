import enquiries
import colorama
import random
import sys
import sqlite3
import getpass

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class Bank:
    banking_data = None
    def __init__(self):
        self.user_balance = 0
        self.user_card_number = 0
        self.user_card_pin = 0
        self.user_luhn_checksum = 0
        self.id_in_system = 0

    def main_greeting(self):
        options = ['Create an account', 'Log Into account', 'Quit']
        choice = enquiries.choose('', options)

        if choice == 'Create an account':
            self.create_user()
        elif choice == 'Log Into account':
            self.login_user()
        else:
            if enquiries.confirm('Do you really want to exit the program?'):
                self.exit_the_program()
            else:
                self.greeting()

    def user_greeting(self):
        options = ['Balance',
                   'Add income',
                   'Do Transfer',
                   'Close account',
                   'Log Out',
                   'Quit']

        choice = enquiries.choose('', options)

    def balance(self):
        pass

    def add_income(self):
        pass

    def do_transfer(self):
        pass

    def delete_account(self):
        pass

    def create_user(self):
        random.seed()
        self.user_card_number = "400000" + str(random.randint(100000000, 999999999))
        self.user_luhn_checksum = self.create_chksum_for_card(self.user_card_number)
        self.user_card_number += str(self.user_luhn_checksum)
        self.user_card_pin = str(random.randint(0000, 9999))
        self.create_bank_table()
        self.data_entry_card()

        print(colorama.Fore.GREEN + "Account has been created!")
        print(colorama.Style.RESET_ALL + "Your card number : " + colorama.Fore.YELLOW + self.user_card_number)
        print(colorama.Style.RESET_ALL + "Your card pin    : " + colorama.Fore.YELLOW +self.user_card_pin + colorama.Style.RESET_ALL + '\n')

    def login_user(self):
        self.data_read_card()
        Bank.banking_data = cur.fetchall()
        print("Enter your card number")
        card = input("> ")
        print("Enter your pin")
        pin = getpass.getpass('> ')
        if (any(card in i for i in Bank.banking_data)) and (any(pin in i for i in Bank.banking_data)):
            cur.execute("SELECT id FROM card WHERE number =(?)", (card,))
            self.id_in_system = cur.fetchone()

            print(colorama.Fore.GREEN + "You have successfully logged in!\n" + colorama.Style.RESET_ALL)
            self.user_greeting()
        else:
            print(colorama.Fore.RED + "Wrong card or PIN!\n" + colorama.Style.RESET_ALL)


    def create_chksum_for_card(self, card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_num)
        odd_digits = digits[0::2]
        even_digits = digits[1::2]

        odd_new_digits = [i * 2 for i in odd_digits]
        a = [i - 9 for i in odd_new_digits if i > 9]

        for i in odd_new_digits[:]:
            if i > 9:
                odd_new_digits.remove(i)
        sum_list = even_digits + odd_new_digits + a
        checksum = 0
        for i in sum_list:
            checksum += i
        for i in range(10):
            if (checksum + i) % 10 == 0:
                return i


    def create_bank_table(self):
        cur.execute("""CREATE TABLE IF NOT EXISTS card(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0);
        """)

    def data_entry_card(self):
        cur.execute("INSERT INTO card (number, pin) VALUES(?, ?)", (self.user_card_number, self.user_card_pin))
        conn.commit()

    def data_read_card(self):
        cur.execute("SELECT number, pin FROM card;")



    def exit_the_program(self):
        print(colorama.Fore.RED + "Good Luck! Bye")
        cur.close()
        sys.exit()


if __name__ == "__main__":
    start_sys = Bank()
    print(colorama.Fore.MAGENTA + "Welcome to the banking system! Choose one of these options:" + colorama.Style.RESET_ALL)
    while True:
        start_sys.main_greeting()
