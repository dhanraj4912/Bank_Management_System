import firebase_admin
from firebase_admin import credentials, db
import random

cred = credentials.Certificate(r"C:\Users\DHANRAJ SINGH\OneDrive\Desktop\python\ASSIGNMENT\bank-management-system-c5e95-firebase-adminsdk-fbsvc-f6476ad037.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bank-management-system-c5e95-default-rtdb.firebaseio.com/'
})

class bank_management:
    def make_an_account(self, Full_name, Age, Email_id, addhar_number, address):
        self.Full_name = Full_name
        self.Age = Age
        self.Email_id = Email_id
        self.addhar_number = addhar_number
        self.address = address
        self.details = [self.Full_name, self.Age, self.Email_id, self.addhar_number, self.address]

        if self.details:
            print("Thank you for choosing us")
            print(f"Your account has been created with name: {self.Full_name}")
            print("To find your account details please select account_details option")
        else:
            print("Please fill all the details correctly!")

    def account_formation(self, account_holder, account_number="", account_balance=0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.account_balance = account_balance
        self.account_holder = self.Full_name

        for _ in range(10):
            self.account_number += str(random.randint(1, 9))

        ref = db.reference("accounts")
        ref.child(self.account_holder).set({
            "account_number": self.account_number,
            "account_balance": self.account_balance
        })

# Deposit money
class deposit:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        ref = db.reference("accounts").child(self.name)

        if self.amount > 0:
            account_data = ref.get()
            if account_data:
                current_balance = int(account_data["account_balance"])
                current_balance += self.amount
                print(f"Your account with Account Number: {account_data['account_number']} has been credited with amount: {self.amount}. New balance: {current_balance}")
                self.current_balance = current_balance
            else:
                print(f"No account found with name {self.name}")
        else:
            print("Invalid deposit amount")

    def update_balance(self):
        ref = db.reference("accounts").child(self.name)
        ref.update({
            "account_balance": self.current_balance
        })

# Withdraw money
class withdraw:
    def __init__(self, account_holder, withdraw_amount):
        self.account_holder = account_holder
        self.withdraw = withdraw_amount
        ref = db.reference("accounts").child(self.account_holder)

        if self.withdraw > 0:
            account_data = ref.get()
            if account_data:
                current_balance = int(account_data["account_balance"])
                if self.withdraw <= current_balance:
                    current_balance -= self.withdraw
                    print(f"Your account with Account Number: {account_data['account_number']} has been debited with amount: {self.withdraw}. New balance: {current_balance}")
                    self.current_balance = current_balance
                else:
                    print("Insufficient balance!")
                    self.current_balance = current_balance
            else:
                print(f"No account found with name {self.account_holder}")
        else:
            print("Invalid withdraw amount")

    def update_balance(self):
        ref = db.reference("accounts").child(self.account_holder)
        ref.update({
            "account_balance": self.current_balance
        })

# Check account details
def account_details(account_holder):
    ref = db.reference("accounts").child(account_holder)
    account_data = ref.get()
    if account_data:
        print(f'''
        Account Holder: {account_holder}
        Account Number: {account_data["account_number"]}
        Account Balance: {account_data["account_balance"]}''')
    else:
        print(f"No account found for {account_holder}")

# Check balance
def check_balance(name):
    ref = db.reference("accounts").child(name)
    account_data = ref.get()
    if account_data:
        print("Current Balance of your account is:", account_data["account_balance"])
    else:
        print(f"No account found with name {name}")

# Main menu
account1 = bank_management()

print('''
1: Create an account
2: View account details
3: Deposit
4: Withdraw
5: Check balance
6: Exit
''')

while True:
    try:
        choice = int(input("Enter your choice (1/2/3/4/5/6): "))

        if choice == 1:
            full_name = input("Enter your full name: ")
            age = int(input("Enter your age: "))
            email = input("Enter your email: ")
            addhar = input("Enter your Aadhar number: ")
            address = input("Enter your address: ")
            account1.make_an_account(full_name, age, email, addhar, address)
            account1.account_formation(full_name)

        elif choice == 2:
            name = input("Enter account holder name: ")
            account_details(name)

        elif choice == 3:
            name = input("Enter account holder name: ")
            amount = int(input("Enter the amount you want to deposit: "))
            account2 = deposit(name, amount)
            account2.update_balance()

        elif choice == 4:
            name = input("Enter account holder name: ")
            amount = int(input("Enter the amount you want to withdraw: "))
            account3 = withdraw(name, amount)
            account3.update_balance()

        elif choice == 5:
            name = input("Enter account holder name: ")
            check_balance(name)

        elif choice == 6:
            print("Thank you for using our bank management system!")
            break

        else:
            print("Invalid choice. Please try again.")

    except Exception as e:
        print("Error:", e)
