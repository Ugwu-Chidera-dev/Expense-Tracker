import json
import logging
import time

def load_expenses():
    try:
        with open("expenses.json") as file:
            data_ = json.load(file)
            if type(data_) is not list:
                raise TypeError("Expenses data must be a list")
            for expense in data_:
                if type(expense) is not dict:
                    raise TypeError("Expenses data must be a dict")
                if 'expense_id' not in expense:
                    raise ValueError("Expense id not matched")
                if 'expense_description' not in expense:
                    raise ValueError("Expense description not matched")
                if 'expense_amount' not in expense:
                    raise ValueError("Expense amount not matched")
                if 'expense_category' not in expense:
                    raise ValueError("Expense category not matched")
                if 'expense_date' not in expense:
                    raise ValueError("Expense date not matched")
            return data_
    except FileNotFoundError:
        logging.error("File path not found")
        print("File not found")
        return []
    except json.decoder.JSONDecodeError:
        logging.error("JSON decode error")
        return []
    except ValueError as e:
        logging.error(e)
        print(e)
        return []
    except TypeError as e:
        logging.error(e)
        print(e)
        return []

def save_expenses(info):
    with open("expenses.json", "w") as file:
        json.dump(info, file, indent=4)

def add_expense():
    data = load_expenses()
    try:
        expense_id = input("Enter expense id: ").strip().lower()
        if expense_id == "":
            logging.error("Entered an empty expense id")
            raise ValueError("Expense id cannot be empty")
        for expense in data:
            if expense['expense_id'].lower() == expense_id:
                logging.info(f"Expense id {expense_id} already exists.")
                raise ValueError("Expense id already exists")
        description = input("Enter expense description: ")
        amount = float(input("Enter expense amount: "))
        if amount < 0:
            logging.error("Entered a negative amount")
            raise ValueError("Expense amount cannot be negative")
        category = input("Enter expense category: ")
        date = time.strftime("%m/%d/%Y")
    except ValueError as e:
        print(e)
    else:
        expense = {
            'expense_id': expense_id,
            'expense_description': description,
            'expense_amount': amount,
            'expense_category': category,
            'expense_date': date
        }
        data.append(expense)
        save_expenses(data)
        logging.info(f"Added expense {expense_id} successfully")

def view_expenses():
    data = load_expenses()
    try:
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        for expense in data:
            print("---------------------------")
            print(expense['expense_id'])
            print(expense['expense_description'])
            print(expense['expense_amount'])
            print(expense['expense_category'])
            print(expense['expense_date'])
        print('All available expenses printed out.')
        logging.info("Successfully printed out all available expenses.")

def search_expense():
    data = load_expenses()
    try:
        expense_id = input("Enter expense id: ").strip().lower()
        if expense_id == "":
            raise ValueError("Entered an empty expense id")
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        for expense in data:
            if expense['expense_id'].lower() == expense_id:
                print(expense['expense_id'])
                print(expense['expense_description'])
                print(expense['expense_amount'])
                print(expense['expense_category'])
                print(expense['expense_date'])
                print('Expense printed out successfully.')
                logging.info(f"Successfully printed out expense {expense_id}.")
                return
        logging.warning("Expense id not matched")
        print("Expense id not matched")

def delete_expense():
    data = load_expenses()
    try:
        expense_id = input("Enter expense id: ").strip().lower()
        if expense_id == "":
            raise ValueError("Entered an empty expense id")
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        for expense in data:
            if expense['expense_id'].lower() == expense_id:
                data.remove(expense)
                save_expenses(data)
                logging.info(f"Successfully deleted expense {expense_id}.")
                return
        logging.warning("Expense id not matched")
        print("Expense id not matched")

def total_expenses():
    data = load_expenses()
    try:
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        total_expense = 0.0
        for expense in data:
            total_expense += expense['expense_amount']
        print(f'The total amount for all expenses: {total_expense}')
        logging.info(f'successful calculation of the total amount for all expenses: {total_expense}')

def filter_by_category():
    data = load_expenses()
    try:
        category = input("Enter expense category: ").strip().lower()
        if category == "":
            logging.error("Entered an empty expense category")
            raise ValueError("Entered an empty expense category")
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        categorized_expenses = []
        status = False
        for expense in data:
            if expense['expense_category'].lower() == category:
                status = True
                categorized_expenses.append(expense)
        if not status:
            logging.warning("Expense category not matched")
            print("Expense category not matched")
            return
        for expense in categorized_expenses:
            print("---------------------------")
            print(expense['expense_id'])
            print(expense['expense_description'])
            print(expense['expense_amount'])
            print(expense['expense_category'])
            print(expense['expense_date'])

def expense_summary():
    data = load_expenses()
    try:
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        total_expense = 0.0
        count = 0
        for expense in data:
            total_expense += expense['expense_amount']
            count += 1
        amounts = []
        for expense in data:
            amounts.append(expense['expense_amount'])
        amounts.sort()
        print(f'The total amount for all expenses: {total_expense}')
        print(f'The amount of expenses printed out: {count}')
        print(f'The total average for all expenses: {total_expense / count}')
        print(f'The highest expense value: {amounts[-1]}')
        print(f'The lowest expense value: {amounts[0]}')
        logging.info(f"Successfully printed out the expense summary.")

def category_summary():
    data = load_expenses()
    try:
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        expense_categories = {}

        for expense in data:
            if expense['expense_category'].lower() not in expense_categories:
                expense_categories[expense['expense_category']] = expense['expense_amount']
            else:
                expense_categories[expense['expense_category']] += expense['expense_amount']
        for key, value in expense_categories.items():
            print(f'{key}: {value}')
        logging.info(f"Successfully printed out the expense summary.")

def monthly_expenses():
    data = load_expenses()
    try:
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        try:
            month = int(input("Enter month (MM): ").strip())
            if month not in range(1, 13):
                raise ValueError("Month should be between 1 and 12")
            year = int(input("Enter year (YYYY): "))
            if year not in range(1, 10000):
                raise ValueError("Year should be between 0000 and 9999")
        except ValueError as e:
            logging.error(e)
            print(e)
        else:
            monthly_expense = []
            for expense in data:
                if expense['expense_date']:
                    date = expense['expense_date'].split('/')
                    if month == int(date[0]) and year == int(date[2]):
                        monthly_expense.append(expense)

            total_expense = 0.0
            if not monthly_expense:
                logging.warning("Empty expense for the specified date")
                print("No expense for the specified date")
                return

            for expense in monthly_expense:
                total_expense += expense['expense_amount']
                print("--------------------------")
                print(expense['expense_id'])
                print(expense['expense_description'])
                print(expense['expense_amount'])
                print(expense['expense_category'])
                print(expense['expense_date'])
            print(f'Total expenses for the specified month: {total_expense}')

def budget_check():
    data = load_expenses()
    try:
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        try:
            month = int(input("Enter month (MM): ").strip())
            if month not in range(1, 13):
                raise ValueError("Month should be between 1 and 12")
            year = int(input("Enter year (YYYY): "))
            if year not in range(1, 10000):
                raise ValueError("Year should be between 0000 and 9999")
            monthly_budget = float(input("Enter monthly budget: "))
            if monthly_budget <= 0:
                raise ValueError("Monthly budget should be greater than 0")
        except ValueError as e:
            logging.error(e)
            print(e)
        else:
            monthly_expense = []
            for expense in data:
                if expense['expense_date']:
                    date = expense['expense_date'].split('/')
                    if month == int(date[0]) and year == int(date[2]):
                        monthly_expense.append(expense)

            total_expense = 0.0
            if not monthly_expense:
                logging.warning("Empty expense for the specified date")
                print("No expense for the specified date")
                return
            for expense in monthly_expense:
                total_expense += expense['expense_amount']

            print(f"Total spent: {total_expense}")
            if total_expense < monthly_budget:
                print(f"You are {monthly_budget - total_expense} under the budget")
            elif total_expense == monthly_budget:
                print("You hit the budget")
            elif total_expense > monthly_budget:
                print(f"You are {total_expense - monthly_budget} over the budget")

def top_category():
    data = load_expenses()
    try:
        if not data:
            logging.error("No expense data found in file")
            raise ValueError("No expense data found")
    except ValueError as e:
        print(e)
    else:
        expense_categories = {}
        for expense in data:
            if expense['expense_category'].lower() not in expense_categories:
                expense_categories[expense['expense_category']] = expense['expense_amount']
            else:
                expense_categories[expense['expense_category']] += expense['expense_amount']
        sorted_expense_categories = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)

        print(f"Top spending category: {sorted_expense_categories[0][0]}")
        print(f"Amount Spent: {sorted_expense_categories[0][1]}")

def show_menu():
    while True:
        try:
            opt = int(input("""Enter your option (Input must be in digits): 
            1. Add expense
            2. View expenses
            3. Search expense
            4. Delete expense
            5. Filter by category
            6. Expense summary
            7. Category summary
            8. Monthly expenses
            9. Budget check
            10. Top spending category
            11. Exit
            \nInput: """))

            if opt not in range(1, 12):
                logging.error("Option not in the range of 1 - 11")
                raise ValueError("Invalid option")
        except ValueError as e:
            print(e)
        else:
            return opt

def main():
    while True:
        option = show_menu()
        if option == 1:
            add_expense()
        elif option == 2:
            view_expenses()
        elif option == 3:
            search_expense()
        elif option == 4:
            delete_expense()
        elif option == 5:
            filter_by_category()
        elif option == 6:
            expense_summary()
        elif option == 7:
            category_summary()
        elif option == 8:
            monthly_expenses()
        elif option == 9:
            budget_check()
        elif option == 10:
            top_category()
        elif option == 11:
            print("Exiting....")
            break

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='expense.log')
    main()