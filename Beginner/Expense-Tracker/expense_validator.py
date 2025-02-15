

class ExpenseValidator:
    @staticmethod
    def validate_category(category: str) -> bool:
        valid_categories = ["Rent", "Car", "Food", "Family", "Miscellaneous"]

        if category not in valid_categories:
            print(f"Invalid category. Valid categories are: {valid_categories}")
            return False
        return True

    @staticmethod
    def validate_amount(amount: float) -> bool:

        if amount < 0:
            print("Amount cannot be negative.")
            return False
        return True

    @staticmethod
    def validate_expense_id(expense_id: str) -> bool:
        
        if not expense_id:
            print("Expense ID cannot be empty.")
            return False
        return True
