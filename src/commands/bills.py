import json
import os

BILL_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bills.json')


def load_bills():
    """Load bills data from the JSON file."""
    if os.path.exists(BILL_DATA_FILE):
        with open(BILL_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_bills(bills):
    """Save bills data to the JSON file."""
    with open(BILL_DATA_FILE, 'w') as file:
        json.dump(bills, file, indent=4)


def list_bills():
    """List all bills."""
    bills = load_bills()
    if not bills:
        print("\nNo bills found.")
        return

    print("\nList of bills:")
    for bill in bills:
        print(f"{bill['id']} / {bill['description']} / {bill['price']}")


def make_bill(description, price):
    """Create a new bill."""
    if description is None:
        print("Error: Description is required.")
        return

    if price is None:
        print("Error: Price is required.")
        return

    bills = load_bills()

    new_id = 1 if not bills else bills[-1]['id'] + 1

    bills.append({
        'id': new_id,
        'description': description,
        'price': price
    })

    save_bills(bills)
    print(f"Bill '{description}' added successfully with ID {new_id}.")


def change_bill(bill_id, description=None, price=None):
    """Update an existing bill."""
    bills = load_bills()

    for bill in bills:
        if bill["id"] == bill_id:
            if description is not None:
                bill["description"] = description
            if price is not None:
                bill["price"] = price

            save_bills(bills)
            print(f"Bill with ID {bill_id} updated successfully.")
            return

    print(f"Error: Bill with ID {bill_id} not found.")


def delete_bill(bill_id):
    """Delete a bill by ID."""
    bills = load_bills()

    for bill in bills:
        if bill["id"] == bill_id:
            bills.remove(bill)
            save_bills(bills)
            print(f"Bill with ID {bill_id} deleted successfully.")
            return

    print(f"Error: Bill with ID {bill_id} not found.")