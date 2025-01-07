import os 
import json
import random 
from datetime import datetime

class Account: 
    account_storage = "AccStorage.json"

    def setInit(self): 
        self.setName()
        self.setSurname()
        self.setAccNumber()
        self.setMobileNum()
        self.setPIN()
        self.setDeposit()
        self._transactions = []
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add creation date
        self.is_frozen = False 

    def setName(self):
        while True: 
            name = input("Please write your name: ")
            if name.isalpha(): 
                break
        self.Name = name

    def setSurname(self): 
        while True: 
            surname = input("Please write your surname: ")
            if surname.isalpha(): 
                break
        self.Surname = surname
      
    def setAccNumber(self):
        while True: 
            acc_num = self.generateAccNumber()
            if self.isAccountNumberUnique(acc_num):
                self.AccountNumber = acc_num
                break

    def isAccountNumberUnique(self, acc_num):
        if os.path.exists(self.account_storage):
            with open(self.account_storage, "r") as fl:
                try:
                    accounts = json.load(fl)
                    for account in accounts:
                        if account["AccountNumber"] == acc_num:
                            return False
                except json.JSONDecodeError:
                    return True
        return True

    def generateAccNumber(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])

    def setMobileNum(self):
        while True: 
            mob_num = input("Please enter your phone number: ")
            if mob_num.isdigit() and mob_num.startswith('0') and '-' not in mob_num: 
                self.mobile_num = mob_num
                break
            elif not mob_num.isdigit():
                print("Phone number must contain only digits!")
            elif not mob_num.startswith('0'):
                print("Phone number must start with 0!")
            elif '-' in mob_num:
                print("Phone number must not contain dashes!")

    def setPIN(self):
        while True: 
            _pin = input("Please enter your pin (must contain 6 digits): ")
            if _pin.isdigit() and len(_pin) == 6: 
                self.Pin = _pin
                break
            else: 
                print("PIN must contain 6 digits!")
    
    def setDeposit(self):
        self.balance = 0 
        while True: 
            balance = input("Please enter the amount of money you want to deposit: ")
            if balance.isdigit() and int(balance) >= 0: 
                break
            else: 
                print("The amount must be positive or 0!")
        self.balance = int(balance)
        self.initial_deposit = self.balance  
    
    def addTransaction(self, transaction_type, amount):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._transactions.append(transaction)

    def getDict(self):
        return {
            "Name": self.Name,
            "Surname": self.Surname,
            "PhoneNumber": self.mobile_num,
            "Balance": self.balance,
            "AccountNumber": self.AccountNumber,
            "Pin": self.Pin,
            "Transactions": self._transactions,
            "CreationDate": self.creation_date,
            "InitialDeposit": self.initial_deposit,
            "is_frozen": self.is_frozen  
        }
    
    def saveToJson(self):
        try:
            if os.path.exists(self.account_storage):
                with open(self.account_storage, "r") as fl:
                    try:
                        accounts = json.load(fl)
                    except json.JSONDecodeError:
                        accounts = []
            else:
                accounts = []

            accounts.append(self.getDict())

            with open(self.account_storage, "w") as fl:
                json.dump(accounts, fl, indent=3)
        except Exception as e:
            print(f"An error occurred: {e}")



