from datetime import datetime
import uuid
from collections import defaultdict
from utils import CSVHandler, BudgetsHandler
from expense_validator import ExpenseValidator


class ExpenseTracker:
    def __init__(self):
        self.utils = CSVHandler('expense.csv')
        self.validator = ExpenseValidator()
        self.monthly_budgets = BudgetsHandler('budgets.json')

    def add_expense(self, description: str, amount: float, category: str) -> None:

        try:
            amount = float(amount)  
        except ValueError:
            print("Amount must be a number.")
            return
    
        if not self.validator.validate_amount(amount):
            print("Invalid amount!")
            return
        
        date: str = datetime.now().isoformat()
        expense_id = str(uuid.uuid4())

        if not self.validator.validate_amount(amount):
            return

        if not self.validator.validate_category(category):
            return

        new_expense = {
            "id": expense_id,
            "description": description,
            "amount": amount,
            "category": category,
            "created_at": date,
            "updated_at": date
        }
        expenses = self.utils.read_expenses()
        expenses.append(new_expense)
        
        self.utils.write_expenses(expenses)
        print(f"Expense with ID {expense_id} created succefully!")

    def update_expense(self, expense_id: str, description: str = None, amount: float = None, category: str = None) -> None:
        if not expense_id:
            print("Expense ID cannot be empty.")
            return

        expenses = self.utils.read_expenses()
        expense_found = False

        for expense in expenses:
            if expense["id"] == expense_id:
                expense_found = True
               
                if description is not None:
                   expense["description"] = description

                if amount is not None:
                    try:
                        amount = float(amount)
                        if self.validator.validate_amount(amount):
                            expense["amount"] = amount
                    except ValueError:
                        print("Invalid amount format.")
                        return

                if category is not None:
                    if self.validator.validate_category(category):
                        expense["category"] = category

                expense["updated_at"] = datetime.now().isoformat()

                self.utils.write_expenses(expenses)
                print(f"Expense with ID {expense_id} has been updated.")
                break
        
        if not expense_found:
            print(f"No expense found with ID {expense_id}.")

    def delete_expense(self, expense_id: str) -> None:
        if not expense_id:
            print("Expense ID cannot be empty.")
            return

        expenses = self.utils.read_expenses()

        updated_expenses = [expense for expense in expenses if expense["id"] != expense_id]
        if len(updated_expenses) == len(expenses):
            print(f"No expense found with ID {expense_id}.")
        
        else:
            self.utils.write_expenses(updated_expenses)
            print(f"Expense with ID {expense_id} has been deleted.")

    def view_all_expenses(self) -> None:
        expenses = self.utils.read_expenses()

        if not expenses:
            print("No expenses available.")

        else:
            print("All Expenses: ")
            for expense in expenses:
                print(
                    f"ID: {expense['id']}, "
                    f"Description: {expense['description']}, "
                    f"Amount: {expense['amount']}, "
                    f"Category: {expense['category']}, "
                    f"Created At: {expense['created_at']}, "
                    f"Updated At: {expense['updated_at']}"
                )

    def view_expenses_summary(self) -> None:
        expenses = self.utils.read_expenses()

        if not expenses:
            print("No expenses available.")
            return

        total_amount = 0
        category_totals = defaultdict(float)
        count = len(expenses)

        for expense in expenses:
            total_amount += float(expense["amount"])
            category_totals[expense["category"]] += float(expense["amount"])

        print(f"Total Expense Count: {count}")
        print(f"Total Amount Spent: ${total_amount:.2f}")

        print("\nAmount spent per category:")
        for category, amount in category_totals.items():
            print(f"{category}: ${amount:.2f}")

        average_expense = total_amount / count if count > 0 else 0
        print(f"\nAverage Expense: ${average_expense:.2f}")

    # Month Input: The month argument is an integer from 1 to 12 (1 for January, 2 for February, etc.)
    def view_expenses_summary_by_month(self, month: int) -> None:
        current_year = datetime.now().year  
        expenses = self.utils.read_expenses()

        if not expenses:
            print("No expenses available.")
            return
        
        filtered_expenses = [
            expense for expense in expenses
            if int(expense["created_at"][:4]) == current_year and int(expense["created_at"][5:7]) == month
        ]

        if not filtered_expenses:
            print(f"No expenses found for {current_year}-{month:02d}.")
            return
        
        total_amount = 0
        category_totals = defaultdict(float)
        count = len(filtered_expenses)

        for expense in filtered_expenses:
            total_amount += float(expense["amount"])
            category_totals[expense["category"]] += float(expense["amount"])

        print(f"Summary for {current_year}-{month:02d}:")
        print(f"Total Expenses Count: {count}")
        print(f"Total Amount Spent: ${total_amount:.2f}")

        print("\nAmount spent per category:")
        for category, amount in category_totals.items():
            print(f"{category}: ${amount:.2f}")
        
        average_expense = total_amount / count if count > 0 else 0
        print(f"\nAverage Expense: ${average_expense:.2f}")

    def view_expense_by_category(self, category: str) -> None:
        expenses = self.utils.read_expenses()

        filtered_expenses = [
        expense for expense in expenses if expense["category"].lower() == category.lower()
    ]
        
        if not filtered_expenses:
            print(f"No expenses found for category: {category}.")
            return
        
        print(f"Expenses for category: {category}:")
        for expense in filtered_expenses:
            print(
                f"ID: {expense['id']}, "
                f"Description: {expense['description']}, "
                f"Amount: {expense['amount']}, "
                f"Created At: {expense['created_at']}"
            )

    def view_expenses_summary_by_category(self, category: str) -> None:
        expenses = self.utils.read_expenses()

        filtered_expenses = [
            expense for expense in expenses if expense["category"].lower() == category.lower()
        ]

        if not filtered_expenses:
            print(f"No expenses found for category: {category}.")
            return

        total_amount = 0
        category_totals = defaultdict(float)
        count = len(filtered_expenses)

        for expense in filtered_expenses:
            total_amount += float(expense["amount"])
            category_totals[expense["category"]] += float(expense["amount"])

        print(f"Summary for category: {category}:")
        print(f"Total Expenses Count: {count}")
        print(f"Total Amount Spent: ${total_amount:.2f}")
        print("\nAmount spent per category:")
        for cat, amount in category_totals.items():
            print(f"{cat}: ${amount:.2f}")
        
        average_expense = total_amount / count if count > 0 else 0
        print(f"\nAverage Expense: ${average_expense:.2f}")

    def set_monthly_budget(self, month: int, budget: float) -> None:
        if budget < 0:
            print("Budget must be a positive value.")
            return
    
        self.monthly_budgets.set_monthly_budget(month, budget)
        print(f"Budget for month {month} set to ${budget:.2f}")

    def view_expenses_summary_by_month_with_budget(self, month: int) -> None:
        current_year = datetime.now().year  
        
        budget = self.monthly_budgets.monthly_budgets.get(str(month))

        if budget is None:
            print(f"No budget set for month {month}.")
            return

        expenses = self.utils.read_expenses()

        if not expenses:
            print("No expenses available.")
            return

        filtered_expenses = [
            expense for expense in expenses 
            if int(expense["created_at"][:4]) == current_year and int(expense["created_at"][5:7]) == month
        ]

        if not filtered_expenses:
            print(f"No expenses found for {current_year}-{month:02d}.")
            return

        total_amount = sum(float(expense["amount"]) for expense in filtered_expenses)

        print(f"Summary for {current_year}-{month:02d}:")
        print(f"Total Expenses Count: {len(filtered_expenses)}")
        print(f"Total Amount Spent: ${total_amount:.2f}")
 
        print(f"Budget for {current_year}-{month:02d}: ${budget:.2f}")
        
        if total_amount > budget:
            print(f"WARNING: You have exceeded your budget by ${total_amount - budget:.2f}!")
        else:
            print(f"You're within your budget for {current_year}-{month:02d}.")

        print("\nAmount spent per category:")
        category_totals = defaultdict(float)
        for expense in filtered_expenses:
            category_totals[expense["category"]] += float(expense["amount"])

        for category, amount in category_totals.items():
            print(f"{category}: ${amount:.2f}")

        average_expense = total_amount / len(filtered_expenses) if len(filtered_expenses) > 0 else 0
        print(f"\nAverage Expense: ${average_expense:.2f}")