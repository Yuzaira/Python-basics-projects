def get_income():
    income=float(input("Enter your monthly income : "))
    return income


def get_expenses():
    expenses={}
    print("Enter your expenses one by one. Type 'done' to stop." )

    while True:
        name = input("Expense Name : ")

        if name.lower() == "done":
            break

        else:
            amount = float(input(f"Amount for {name} : "))
            expenses[name] = amount
    return expenses


def show_summary( income, expenses):
    print("\n ======= MONTHLY BUDGET SUMMARY =======")
    print(f"Income : {income}")

    print("\nExpenses:")
    total = 0
    for name, amount in expenses.items():
        total+=amount
        print(f" {name} : {amount}")

    remaining = income - total

    print(f"\nTotal Expenses : {total}")
    print(f"Remaining : {remaining}")

    if remaining > 0:
        print(" Status : ✅ You are within budget! ")
    elif remaining == 0:
        print("Status : ⚠️ You've used exactly your income")
    else:
        print("Overspent this month❗")
        pass


#---Main Program---
income=get_income()
expenses=get_expenses()
show_summary(income,expenses)




