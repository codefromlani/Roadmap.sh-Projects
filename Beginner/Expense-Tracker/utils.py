import csv
import os
import json


class CSVHandler:

    def __init__(self, file_name='expense.csv'):
        self.file_name = file_name
        self.fieldnames = ["id", "description", "amount", "category", "created_at", "updated_at"]

    def read_expenses(self):
        if not os.path.exists(self.file_name):
            expenses = []
            return expenses
        
        try:
            with open(self.file_name, mode="r", newline='') as f:
                reader = csv.DictReader(f)
                expenses = [] 
                for row in reader:
                    expense = {
                        'id': row['id'], 
                        'description': row['description'],
                        'amount': float(row['amount']),
                        'category': row['category'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    }
                    expenses.append(expense)
            return expenses
            
        except Exception as e:
            print(f"Error occurred while reading the file: {e}")
            return []

    def write_expenses(self, expenses):

        try:
            file_exists = os.path.exists(self.file_name)
            
            with open(self.file_name, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)

                writer.writeheader()  
                for expense in expenses:
                    writer.writerow(expense)
                    
        except Exception as e:
            print(f"Error occurred while writing to the file: {e}")


class BudgetsHandler():

    def __init__(self, file_name='budgets.json'):
        self.file_name = file_name
        self.monthly_budgets = self.load_budgets()

    def load_budgets(self):

        try:
            if not os.path.exists(self.file_name):
                with open(self.file_name, 'w') as f:
                    json.dump({}, f)
                return {}
            
            with open(self.file_name, 'r') as f:
                content = f.read().strip()
                if not content:  
                    return {}
                return json.loads(content)
            
        except FileNotFoundError:
            return {}
        
    def save_budgets(self):

        with open(self.file_name, 'w') as f:
            json.dump(self.monthly_budgets, f, indent=4)

    def set_monthly_budget(self, month: int, budget: float) -> None:
        self.monthly_budgets[str(month)] = budget
        self.save_budgets()