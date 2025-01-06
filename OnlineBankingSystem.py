

from AccountGeneration import Account
import json
import os
from datetime import datetime

currency = "BAM"

def save_acc(accounts):
    with open(Account.account_storage, "w") as fl:
        json.dump(accounts, fl, indent=4)
    return load_acc()

def load_acc():
    if os.path.exists(Account.account_storage):
        with open(Account.account_storage, "r") as fl:
            try:
                return json.load(fl)
            except json.JSONDecodeError:
                print("Error: Corrupted account storage file. Starting with an empty account list.")
                return []
    return []

def find_acc(phone_number, pin, accounts):
    phone_number = phone_number.strip()
    pin = pin.strip()
    for account in accounts:
        if account["PhoneNumber"] == phone_number and account["Pin"] == pin:
            return account
    return None

def account_menu(account_data, all_accounts):
    hold = True
    while hold:
        try:
            print("\nAccount Menu")
            print("1. View account details")
            print("2. Transaction history")
            print("3. Deposit money")
            print("4. Withdraw money")
            print("5. Transfer money")
            print("6. Log out")

            choice = int(input("\nEnter a valid choice: "))

            if choice == 1:
                print("\nAccount Details:")
                print(f"Name and Surname: {account_data['Name']} {account_data['Surname']}")
                print(f"Phone Number: {account_data['PhoneNumber']}")
                print(f"Balance: {account_data['Balance']} {currency}")
                print(f"Account Number: {account_data['AccountNumber']}")

            elif choice == 2:
                print("\nTransaction history:")
                if account_data["Transactions"]:
                    for tr in account_data["Transactions"]:
                        print(f"{tr['timestamp']}: {tr['type']} of {tr['amount']} {currency}")
                else:
                    print("No transactions yet.")

            elif choice == 3:
                try:
                    amount = int(input("Enter the amount to deposit in BAM: "))
                    if amount > 0:
                        account_data["Balance"] += amount
                        account_data["Transactions"].append({
                            "type": "Deposit",
                            "amount": amount,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        save_acc(all_accounts)
                        print(f"Successfully deposited {amount} {currency}. New balance: {account_data['Balance']} {currency}")
                    else:
                        print("Deposit amount must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")

            elif choice == 4:
                try:
                    amount = int(input("Enter the amount to withdraw in BAM: "))
                    if amount > 0 and amount <= account_data['Balance']:
                        account_data["Balance"] -= amount
                        account_data["Transactions"].append({
                            "type": "Withdrawal",
                            "amount": amount,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        save_acc(all_accounts)
                        print(f"Successfully withdrew {amount}. New balance: {account_data['Balance']} {currency}")
                    elif amount > account_data['Balance']:
                        print("Insufficient funds to withdraw.")
                    else:
                        print("The amount must be greater than zero.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")

            elif choice == 5:
                try:
                    recipient = input("Enter the recipient's account number: ")
                    recipient_acc = next((acc for acc in all_accounts if acc["AccountNumber"] == recipient), None)

                    if recipient_acc is None:
                        print("No account found.")
                        continue
                    if recipient_acc["AccountNumber"] == account_data["AccountNumber"]:
                        raise ValueError("You cannot transfer money to your own account.")

                    amount = int(input(f"Enter the amount to transfer to {recipient} in BAM: "))

                    if amount <= 0:
                        raise ValueError("Transfer amount must be greater than zero.")
                    if amount > account_data["Balance"]:
                        raise ValueError("Insufficient funds for the transfer.")

                    account_data["Balance"] -= amount
                    account_data["Transactions"].append({
                        "type": "Transfer Out",
                        "amount": amount,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "to": recipient_acc["AccountNumber"]
                    })

                    recipient_acc["Balance"] += amount
                    recipient_acc["Transactions"].append({
                        "type": "Transfer In",
                        "amount": amount,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "from": account_data["AccountNumber"]
                    })

                    print(f"Successfully transferred {amount} {currency} to {recipient_acc['AccountNumber']}.")
                    save_acc(all_accounts)

                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == 6:
                print("Logging out...")
                hold = False

            else:
                print("Invalid choice. Try again!")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def main():
    toggle = True
    while toggle:
        try:
            print("\n\nWelcome to The Bank of Ilidza\n\n")
            print("1. Create an account")
            print("2. Log in to an existing account")
            print("3. Exit the bank")

            choice = int(input("\nEnter a valid choice: "))

            if choice == 1:
                print("\nCreating a new account...")
                new_account = Account()
                new_account.setInit()
                new_account.saveToJson()
                accounts = load_acc()
                print("\nAccount successfully created!")

            elif choice == 2:
                accounts = load_acc()
                phone_number = input("\nEnter your phone number: ")
                pin = input("Enter your pin: ")
                account = find_acc(phone_number, pin, accounts)

                if account:
                    account_menu(account, accounts)
                else:
                    print("Invalid credentials. Please try again.")

            elif choice == 3:
                print("\nThank you for using the Bank of Ilidza\n")
                toggle = False

            else:
                print("Please only enter a number 1, 2, or 3!")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

if __name__ == "__main__":
    main()