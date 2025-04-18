import datetime
from utils.file_utils import get_data_file_path
from db.db_interface import load_data, save_data

BILL_DATA_FILE = get_data_file_path('bills.json')

def list_bills():
    """List all bills."""
    bills = load_data(BILL_DATA_FILE)
    if not bills:
        print("\nNo bills found.")
        return

    print("\nList of bills:")
    for bill in bills:
        print(f"id: {bill['id']} / description: {bill['description']} / price: {bill['price']} / date: {bill['date']}")


def make_bill(description, price, date):
    """Create a new bill."""
    if description is None:
        print("Error: Description is required.")
        return

    if price is None:
        print("Error: Price is required.")
        return

    if date is None:
        date = datetime.datetime.now().strftime('%d/%m/%Y')

    bills = load_data(BILL_DATA_FILE)

    new_id = 1 if not bills else bills[-1]['id'] + 1

    bills.append({
        'id': new_id,
        'description': description,
        'price': price,
        'date': date,
    })

    save_data(BILL_DATA_FILE, bills)
    print(f"Bill '{description}' with price {price} added successfully with ID {new_id}.")


def change_bill(bill_id, description=None, price=None, date=None):
    """Update an existing bill."""
    bills = load_data(BILL_DATA_FILE)

    for bill in bills:
        if bill["id"] == bill_id:
            if description is not None:
                bill["description"] = description
            if price is not None:
                bill["price"] = price
            if date is not None:
                bill["date"] = date

            save_data(BILL_DATA_FILE, bills)
            print(f"Bill with ID {bill_id} updated successfully.")
            return

    print(f"Error: Bill with ID {bill_id} not found.")


def delete_bill(bill_id):
    """Delete a bill by ID."""
    bills = load_data(BILL_DATA_FILE)

    for bill in bills:
        if bill["id"] == bill_id:
            bills.remove(bill)
            save_data(BILL_DATA_FILE, bills)
            print(f"Bill with ID {bill_id} deleted successfully.")
            return

    print(f"Error: Bill with ID {bill_id} not found.")