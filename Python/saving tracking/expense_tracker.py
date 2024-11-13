import os
from expense import Expense 
import calendar
import datetime

def main():
    print(f"Running Expense Tracker!")
    expense_file_path = os.path.join(os.path.dirname(__file__), "expenses.csv")
    budget = 2000

    #get user to input expense
    expense = get_user_expense()

    #write it to file
    save_expense_to_file(expense, expense_file_path)

    #read file and summarise expenses
    summarize_expense(expense_file_path, budget)

def get_user_expense():
    print(f"Getting user expenses!")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category, please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"save expenses to file: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")

def summarize_expense(expense_file_path, budget):
    print(f"Summarize expenses!")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name, amount=float(expense_amount), category=expense_category
            )
            expenses.append(line_expense)

    amount_by_caetegory = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_caetegory:
            amount_by_caetegory[key] += expense.amount
        else: 
            amount_by_caetegory[key] = expense.amount

    print("Expenses by Category: ")
    for key, amount in amount_by_caetegory.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"You've spent ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Budget remaining ${remaining_budget:.2f}")

    now = datetime.datetime.now()

    days_in_month = calendar.monthrange(now.year, now.month)[1]

    remaining_days = days_in_month - now.day
    print("Remaining days in the current month: ", remaining_days)

    daily_budget = remaining_budget / remaining_days
    print(f"Budget per day ${daily_budget:.2f}")


if __name__ == "__main__":
    main()
