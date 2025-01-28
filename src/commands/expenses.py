import datetime
import json
import os

EXPENSES_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'expenses.json')


def load_data():
    """Load expenses data from the JSON file."""
    if os.path.exists(EXPENSES_DATA_FILE):
        with open(EXPENSES_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_data(data):
    """Save expenses data to the JSON file."""
    with open(EXPENSES_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def list_expenses():
    """List all expenses with date, description, and amount."""
    expenses = load_data()
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\nList of Expenses:")
    for expense in expenses:
        id = expense.get('id', 'No id available')
        date = expense.get('date', 'No date available')
        description = expense.get('description', 'No description available')
        amount = expense.get('amount', 'No amount available')
        print(f"{id} / {date} / {description} / {amount}")


def make_expense(description=None, amount=None, date=None, category=None):
    """Create a new expense."""
    if description is None or amount is None or category is None:
        print("Error: Description, amount and category are required.")
        return

    if date is None:
        date = datetime.datetime.now().strftime('%d/%m/%Y')

    expenses = load_data()

    new_id = 1 if not expenses else expenses[-1]['id'] + 1

    expenses.append({
        'id': new_id,
        'date': date,
        'description': description,
        'amount': amount,
        'category': category
    })

    save_data(expenses)

    print(f"Expense '{description}' with amount {amount} in category {category} was added successfully with ID {new_id}.")


def change_expense(expense_id=None, description=None, amount=None, date=None):
    """Modify an existing expense by ID."""
    if expense_id is None:
        print("Error: Expense ID is required.")
        return

    expenses = load_data()

    for expense in expenses:
        if expense["id"] == expense_id:
            if description is not None:
                expense["description"] = description
            if amount is not None:
                expense["amount"] = amount
            if date:
                expense["date"] = date

            save_data(expenses)

            print(f"Expense with ID {expense_id} updated successfully.")
            return

    print(f"Error: Expense with ID {expense_id} not found.")


def delete_expense(expense_id):
    """Delete an expense by ID."""
    expenses = load_data()

    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            save_data(expenses)
            print(f"Expense with ID {expense_id} deleted successfully.")
            return

    print(f"Error: Expense with ID {expense_id} not found.")