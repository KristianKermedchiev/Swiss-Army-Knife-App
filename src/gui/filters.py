# from datetime import datetime
#
# def filter_expenses_by_category(expenses, category):
#     """Filter expenses by category."""
#     return [expense for expense in expenses if expense['category'].lower() == category.lower()]
#
# def filter_expenses_by_date(expenses, start_date, end_date):
#     """Filter expenses by date range."""
#     filtered = []
#     for expense in expenses:
#         expense_date = datetime.strptime(expense['date'], '%d/%m/%Y')
#         if start_date <= expense_date <= end_date:
#             filtered.append(expense)
#     return filtered
