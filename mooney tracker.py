import tkinter as tk
from tkinter import messagebox

import os
import pickle

class MoneyTracker:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []
        self.filename = "money_tracker_data.pkl"
        self.load_data()

    def add_income(self, amount, description="Income"):
        self.balance += amount
        self.transactions.append((amount, description, 'income'))
        self.save_data()

    def add_expense(self, amount, description="Expense"):
        self.balance -= amount
        self.transactions.append((amount, description, 'expense'))
        self.save_data()

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions

    def print_transactions(self):
        for transaction in self.transactions:
            print(f"{transaction[2].capitalize()} of ₹{transaction[0]:,.2f} for '{transaction[1]}'")

    def save_data(self):
        with open(self.filename, 'wb') as f:
            pickle.dump((self.balance, self.transactions), f)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.balance, self.transactions = pickle.load(f)

class MoneyTrackerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Tracker")

        self.tracker = MoneyTracker()

        self.balance_label = tk.Label(root, text="Current Balance:", font=("Helvetica", 16))
        self.balance_label.pack(pady=10)

        self.balance_value = tk.Label(root, text=f"₹{self.tracker.get_balance():,.2f}", font=("Helvetica", 24, "bold"))
        self.balance_value.pack()

        self.amount_label = tk.Label(root, text="Enter Amount (₹):", font=("Helvetica", 12))
        self.amount_label.pack(pady=5)

        self.amount_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
        self.amount_entry.pack()

        self.description_label = tk.Label(root, text="Enter Description (optional):", font=("Helvetica", 12))
        self.description_label.pack(pady=5)

        self.description_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
        self.description_entry.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.income_button = tk.Button(self.button_frame, text="Add Income", font=("Helvetica", 12), bg="green", fg="white", width=12, command=self.add_income)
        self.income_button.grid(row=0, column=0, padx=5)

        self.expense_button = tk.Button(self.button_frame, text="Add Expense", font=("Helvetica", 12), bg="red", fg="white", width=12, command=self.add_expense)
        self.expense_button.grid(row=0, column=1, padx=5)

        self.transactions_button = tk.Button(root, text="View Transactions", font=("Helvetica", 12), width=30, command=self.view_transactions)
        self.transactions_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), width=30, command=root.quit)
        self.exit_button.pack(pady=5)

    def add_income(self):
        amount_str = self.amount_entry.get()
        description = self.description_entry.get()
        if amount_str and amount_str.replace('.', '', 1).isdigit():
            amount = float(amount_str)
            if amount > 0:
                self.tracker.add_income(amount, description)
                self.update_balance()
                messagebox.showinfo("Success", "Income added successfully.")
            else:
                messagebox.showerror("Error", "Amount must be greater than zero.")
        else:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def add_expense(self):
        amount_str = self.amount_entry.get()
        description = self.description_entry.get()
        if amount_str and amount_str.replace('.', '', 1).isdigit():
            amount = float(amount_str)
            if amount > 0:
                self.tracker.add_expense(amount, description)
                self.update_balance()
                messagebox.showinfo("Success", "Expense added successfully.")
            else:
                messagebox.showerror("Error", "Amount must be greater than zero.")
        else:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def view_transactions(self):
        transactions = self.tracker.get_transactions()
        if transactions:
            transaction_text = "\n".join(f"{t[2].capitalize()} of ₹{t[0]:,.2f} for '{t[1]}'" for t in transactions)
            messagebox.showinfo("Transactions", transaction_text)
        else:
            messagebox.showinfo("Transactions", "No transactions yet.")

    def update_balance(self):
        self.balance_value.config(text=f"₹{self.tracker.get_balance():,.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoneyTrackerUI(root)
    root.mainloop()
