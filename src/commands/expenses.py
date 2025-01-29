import datetime
import json
import os
import pandas as pd


EXPENSES_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'expenses.json')


def load_expenses():
    """Load expenses data from the JSON file."""
    if os.path.exists(EXPENSES_DATA_FILE):
        with open(EXPENSES_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_expenses(data):
    """Save expenses data to the JSON file."""
    with open(EXPENSES_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def list_expenses():
    """List all expenses with date, description, and amount."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\nList of Expenses:")
    for expense in expenses:
        id = expense.get('id', 'No id available')
        date = expense.get('date', 'No date available')
        description = expense.get('description', 'No description available')
        amount = expense.get('amount', 'No amount available')
        category = expense.get('category', 'No category available')
        print(f"{id} / {date} / {description} / {amount} / {category}")


def make_expense(description=None, amount=None, date=None, category=None):
    """Create a new expense."""
    if description is None or amount is None or category is None:
        print("Error: Description, amount and category are required.")
        return

    if date is None:
        date = datetime.datetime.now().strftime('%d/%m/%Y')

    expenses = load_expenses()

    new_id = 1 if not expenses else expenses[-1]['id'] + 1

    expenses.append({
        'id': new_id,
        'date': date,
        'description': description,
        'amount': amount,
        'category': category
    })

    save_expenses(expenses)

    print(f"Expense '{description}' with amount {amount} in category {category} was added successfully with ID {new_id}.")


def change_expense(expense_id=None, description=None, amount=None, date=None, category=None):
    """Modify an existing expense by ID."""
    if expense_id is None:
        print("Error: Expense ID is required.")
        return

    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            if description is not None:
                expense["description"] = description
            if amount is not None:
                expense["amount"] = amount
            if date:
                expense["date"] = date
            if category:
                expense["category"] = category

            save_expenses(expenses)

            print(f"Expense with ID {expense_id} updated successfully.")
            return

    print(f"Error: Expense with ID {expense_id} not found.")


def delete_expense(expense_id):
    """Delete an expense by ID."""
    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print(f"Expense with ID {expense_id} deleted successfully.")
            return

    print(f"Error: Expense with ID {expense_id} not found.")


def expense_log(start_date=None, end_date=None, category=None, download=False):
    """Generate an expense log based on filters and optionally export to CSV."""
    expenses = load_expenses()

    if not start_date and not end_date and not category:
        print("Error: At least one filter (start_date, end_date, or category) must be provided.")
        return

    filtered_expenses = []

    for expense in expenses:
        expense_date = datetime.datetime.strptime(expense["date"], '%d/%m/%Y')

        if start_date:
            start_date_obj = datetime.datetime.strptime(start_date, '%d/%m/%Y')
            if expense_date < start_date_obj:
                continue

        if end_date:
            end_date_obj = datetime.datetime.strptime(end_date, '%d/%m/%Y')
            if expense_date > end_date_obj:
                continue

        if category and expense["category"].lower() != category.lower():
            continue

        filtered_expenses.append(expense)

    if not filtered_expenses:
        print("No expenses found for the given criteria.")
        return

    print("\nFiltered Expenses:")
    for expense in filtered_expenses:
        print(
            f"{expense['id']} / {expense['date']} / {expense['description']} / {expense['amount']} / {expense['category']}")

    if download:
        current_date = datetime.datetime.now().strftime('%d-%m-%Y')  # Fix filename issue
        csv_file = f"expense_report_{current_date}.csv"

        # Using Pandas to handle CSV writing
        df = pd.DataFrame(filtered_expenses)
        df.to_csv(csv_file, index=False)

        print(f"Expense report saved as {csv_file}.")