# Expense Tracker CLI

A simple command-line interface (CLI) application to help you track and manage your personal expenses.

## Features

- Add new expenses with descriptions, amounts, and categories
- Update existing expenses
- Delete expenses
- View all expenses
- View expense summaries
- Track expenses by category
- Set and monitor monthly budgets
- Generate monthly reports

## Installation

Make sure you have Python 3.x installed
1. Clone the repository:
   ```bash
   git clone https://github.com/codefromlani/Roadmap.sh-Projects.git

2. Navigate to the project directory:

    cd beginner

    cd expense-tracker

## Usage

1. Adding an Expense
    ```bash
    python main.py add "Expense Description" amount category

Example:
    ```bash
    python main.py add "Grocery Shopping" 150.50 Food

2. Updating an Expense
    ```bash
    python main.py update expense_id --new_description "New Description" --new_amount amount --new_category category

Example:
    ```bash
    python main.py update abc123 --new_amount 200.00 --new_category Food

3. Deleting an Expense
    ```bash
    python main.py delete expense_id

4. Viewing All Expenses
    ```bash
    python main.py view

5. Viewing Expense Summary
    ```bash
    python main.py summary

6. Viewing Expenses by Category
    ```bash
    python main.py view_by_category category

Example:
    ```bash
    python main.py view_by_category Food

7. Setting Monthly Budget
    ```bash
    python main.py budgets month amount

Example:
    ```bash
    python main.py budgets 2 2500.00

8. Viewing Monthly Budget Summary
    ```bash
    python main.py budgets_summary month
Example:
    ```bash
    python main.py budgets_summary 2

9. Categories
- Available expense categories:

    Rent
    Car
    Food
    Family
    Miscellaneous

## File Structure

- main.py: Main CLI application
- expense_tracker.py: Core expense tracking functionality
- utils.py: Utility functions for file handling
- expense_validators.py: Input validation functions

## Data Storage

Expenses are stored in expense.csv
Budgets are stored in budgets.json

## Support
This is a basic expense tracking tool. For feature requests or bug reports, please open an issue in the repository.