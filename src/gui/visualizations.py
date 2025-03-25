# import matplotlib.pyplot as plt
#
# def plot_expenses_by_category(expenses):
#     """Create a pie chart of expenses by category."""
#     categories = {}
#     for expense in expenses:
#         category = expense['category']
#         amount = expense['amount']
#         if category in categories:
#             categories[category] += amount
#         else:
#             categories[category] = amount
#
#     labels = categories.keys()
#     values = categories.values()
#
#     plt.pie(values, labels=labels, autopct='%1.1f%%')
#     plt.title('Expenses by Category')
#     plt.show()
#
# def plot_expenses_over_time(expenses):
#     """Create a line chart of expenses over time."""
#     dates = [expense['date'] for expense in expenses]
#     amounts = [expense['amount'] for expense in expenses]
#
#     plt.plot(dates, amounts)
#     plt.title('Expenses Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Amount')
#     plt.xticks(rotation=45)
#     plt.show()
