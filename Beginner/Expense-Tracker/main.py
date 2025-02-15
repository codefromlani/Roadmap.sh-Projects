import argparse
from expense_tracker import ExpenseTracker


def main():
    parser = argparse.ArgumentParser(
        description="A CLI application to manage your finances."
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser('add', help="Add a new expense")
    add_parser.add_argument('description', help="The Description of the expense") 
    add_parser.add_argument('amount', help="Amount of the expense")
    add_parser.add_argument('category', choices=["Rent", "Car", "Food", "Family", "Miscellaneous"])    

    update_parser = subparsers.add_parser('update', help="Update an existing expense")
    update_parser.add_argument('expense_id', help="ID of the expense to update")
    update_parser.add_argument('--new_description', help="New description of the expense")
    update_parser.add_argument('--new_amount', help="New amount of the expense")
    update_parser.add_argument('--new_category', choices=["Rent", "Car", "Food", "Family", "Miscellaneous"], help="New category of the expense")

    delete_parser = subparsers.add_parser('delete', help="Delete an existing expense")
    delete_parser.add_argument('expense_id', help="The ID of the expense to delete")

    subparsers.add_parser('view', help="View all expenses")

    subparsers.add_parser('summary', help="Summary of all expenses")

    summary_by_month = subparsers.add_parser('summary_by_month', help="View a summary of expenses by month")
    summary_by_month.add_argument('month',  type=int, help="Month (as an integer) to view the expense summary")

    view_by_category = subparsers.add_parser('view_by_category', help="View expenses by category")
    view_by_category.add_argument('category', choices=["Rent", "Car", "Food", "Family", "Miscellaneous"], help="The category of the expense")

    view_summary_by_category = subparsers.add_parser('view_summary_by_category', help="View expenses summary by category")
    view_summary_by_category.add_argument('category', choices=["Rent", "Car", "Food", "Family", "Miscellaneous"], help="The category of the expense summary")

    set_budgets = subparsers.add_parser('budgets', help="Set a monthly budget for expenses")
    set_budgets.add_argument('month', type=int, help="Month of the budget")
    set_budgets.add_argument('budgets', type=float, help="Budget for the month")

    view_budget_summary_by_month = subparsers.add_parser('budgets_summary', help="View a summary of budgets per month")
    view_budget_summary_by_month.add_argument('month', type=int, help="Month for the budget summary")

    args = parser.parse_args()

    my_expense = ExpenseTracker()

    if args.command == 'add':
        my_expense.add_expense(args.description, args.amount, args.category)

    elif args.command == 'update':
        new_amount = float(args.new_amount) if args.new_amount else None
        my_expense.update_expense(args.expense_id, args.new_description, new_amount, args.new_category)

    elif args.command == 'delete':
        my_expense.delete_expense(args.expense_id)

    elif args.command == 'view':
        my_expense.view_all_expenses()

    elif args.command == 'summary':
        my_expense.view_expenses_summary()

    elif args.command == 'summary_by_month':
        my_expense.view_expenses_summary_by_month(args.month)

    elif args.command == 'view_by_category':
        my_expense.view_expense_by_category(args.category)

    elif args.command == 'view_summary_by_category':
        my_expense.view_expenses_summary_by_category(args.category)

    elif args.command == 'budgets':
        my_expense.set_monthly_budget(args.month, args.budgets)

    elif args.command == 'budgets_summary':
        my_expense.view_expenses_summary_by_month_with_budget(args.month)

    else:
        print("Invalid command. Use --help for usage.")

if __name__ == "__main__":
    main()