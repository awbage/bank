import sqlite3
import random
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''create table if not exists card(
id INTEGER PRIMARY KEY,
number TEXT,
pin TEXT, 
balance INTEGER DEFAULT 0)
''')
conn.commit()
from random import randint
import re

class card:
    def __init__(self, log_number=0, transfer_num=0, num_pin={}, num=None, pin=None, bal=0):
        self.bal=bal
        self.num = num
        self.pin=pin
        self.num_pin=num_pin

    def checksum(self):
        self.num = list(str(f'{400000}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}\
{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}'))
        luhn = (self.num)
        for i in range(0, 15):
            luhn[i] = int(luhn[i])
        i = 0
        s0 = 0
        s1 = 0
        while i < 15:
            if i % 2 == 0:
                l = luhn[i] * 2
                if l > 9:
                    s0 = s0 + (l - 9)
                else:
                    s0 += l
                i += 1
            else:
                s1 += luhn[i]
                i += 1
        s = s0 + s1
        if s % 10 == 0:
            last_digit = 0
        else:
            last_digit = (10 - s % 10)
        luhn.append(last_digit)
        luhn = list(map(str, luhn))
        luhn = (''.join(luhn))
        self.num = (luhn)

    def gen(self, num_pin={}):
        c.checksum()
        self.pin = (f'{randint(1,9)}{randint(1,9)}{randint(1,9)}{randint(1,9)}')
        c.pin = (int(c.pin))
        print('Your card has been created \nYour card number:')
        print(c.num)
        cur.execute(f'''insert into card(number, pin) values({self.num}, {self.pin})''')
        conn.commit()
        print('Your card PIN:')
        print((c.pin))
        c.mainmenu()

    def tnum(self, transfer_num):
        t_num = transfer_num
        ttuple_num = []
        for i in range(len(t_num)):
            ttuple_num.append(t_num[i])
        for i in range(0, 15):
            ttuple_num[i] = int(ttuple_num[i])
            i = 0
            s0 = 0
            s1 = 0
            while i < 16:
                if i % 2 == 0:
                    l = int(ttuple_num[i] * 2)
                    if l > 9:
                        s0 = s0 + (l - 9)
                    else:
                        s0 += l
                    i += 1
                else:
                    s1 += int(ttuple_num[i])
                    i += 1
            s = s0 + s1
        if s % 10 == 0:
            return 1
        else:
            return 0

    def transfer(self):
        print('\nTransfer\nEnter card number:')
        transfer_num = input()
        transfer_num_exist = cur.execute(f'select * from card where number = {transfer_num}')
        transfer_num_exist = transfer_num_exist.fetchall()
        if transfer_num == self.log_number:
            print("You can't transfer money to the same account!")
            c.logged_in()
        elif not c.tnum(transfer_num):
            print('Probably you made a mistake in the card number. Please try again!')
            c.logged_in()
        elif not transfer_num_exist:
            print('Such a card does not exist.')
            c.logged_in()
        else:
            print('Enter how much money you want to transfer:')
            money_to_transfer=int(input())
            current_balance=cur.execute(f'select balance from card where number = {self.log_number}').fetchone()
            current_balance=(current_balance[0])
            if current_balance < money_to_transfer:
                print('\nNot enough money!')
                c.logged_in()
            else:
                cur.execute(f'UPDATE card SET balance = {current_balance-money_to_transfer} where number = {self.log_number}')
                cur.execute(f'UPDATE card SET balance = (balance + {money_to_transfer}) where number = {transfer_num}')
                print('Success!')
                conn.commit()
                c.logged_in()
        conn.commit()

    def logged_in(self):
        print('\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
        a=int(input())
        if a == 1:
            c.check()
            c.logged_in()
        elif a == 2:
            print('\nEnter income:')
            cur.execute(f'UPDATE card SET balance = (balance+{input()}) WHERE number = {self.log_number}')
            print('Income was added!')
            conn.commit()
            c.logged_in()
        elif a == 3:
            c.transfer()
        elif a == 4:
            cur.execute(f'delete from card where number={self.log_number}')
            print('\nThe account has been closed!')
            conn.commit()
            c.mainmenu()
        elif a == 5:
            print('\nYou have successfully logged out!')
            c.mainmenu()
        elif a == 0:
            c.exit()
        conn.commit()

    def enter(self):
        print('Enter your card number:')
        a=str(input())
        if a == '0':
            c.exit()
        else:
            if a in c.num_pin.keys():
                self.log_number = a
                print('Enter your PIN:')
                b=(input())
                if self.num_pin[a] == b:
                    print('\nYou have successfully logged in!\n')
                    c.logged_in()
                else:
                    print('Wrong card number or PIN!')
                    c.enter()
            else:
                print('Wrong card number or PIN!')
                c.enter()

    def check(self):
        cur.execute('select number, balance from card')
        bal = dict(cur.fetchall())
        balance=(bal[self.log_number])
        print(f'\nYour balance is {balance}')
        conn.commit()

    def exit(self):
        print('\nBye!')

    def mainmenu(self):
        cur.execute('select number, pin from card')
        self.num_pin = cur.fetchall()
        self.num_pin = dict(self.num_pin)
        print(f'\n1. Create an account\n2. Log into account\n0. Exit')
        a = (input())
        if   a == '1':
            c.gen()
        elif a == '2':
            c.enter()
        elif a == '0':
            c.exit()
        else:
            print('Please use following options')
            c.mainmenu()

c = card()
c.mainmenu()
conn.commit()
conn.close()
