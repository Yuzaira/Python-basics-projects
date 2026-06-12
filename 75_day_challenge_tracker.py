"""
75-Day Challenge Tracker
A simple console-based habit tracker using Python basics:
dictionaries, functions, loops, conditionals, file handling, datetime.
"""

import os
from datetime import date

HABITS_FILE = "habits.txt"
LOG_FILE = "daily_log.txt"
TOTAL_DAYS = 75


# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------
def setup_habits():
    """Ask user for habits (only if not already set up) and save to file."""
    if os.path.exists(HABITS_FILE):
        with open(HABITS_FILE, "r") as f:
            habits = [line.strip() for line in f.readlines() if line.strip()]
        print("Loaded existing habits:", habits)
        return habits

    print("Let's set up your 75-Day Challenge!")
    print("Enter your habits one by one. Type 'done' when finished.\n")

    habits = []
    while True:
        habit = input("Enter habit name: ").strip()
        if habit.lower() == "done":
            if len(habits) == 0:
                print("Please add at least one habit.")
                continue
            break
        if habit == "":
            print("Habit name can't be empty.")
            continue
        habits.append(habit)
        print(f"Added: {habit}")

    with open(HABITS_FILE, "w") as f:
        for h in habits:
            f.write(h + "\n")

    print("\nHabits saved! Setup complete.\n")
    return habits


# ---------------------------------------------------------
# LOGGING A DAY
# ---------------------------------------------------------
def get_day_number():
    """Calculate which day number this is based on existing log entries."""
    if not os.path.exists(LOG_FILE):
        return 1

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    day_count = 0
    for line in lines:
        if line.startswith("DAY:"):
            day_count += 1

    return day_count + 1


def log_day(habits):
    """Log today's habit completion."""
    day_number = get_day_number()

    if day_number > TOTAL_DAYS:
        print(f"\nYou've already completed all {TOTAL_DAYS} days! 🎉")
        print("You can still view your history or reset the challenge.")
        return

    print(f"\n--- Day {day_number} of {TOTAL_DAYS} ---")
    today = date.today().strftime("%Y-%m-%d")

    results = {}
    for habit in habits:
        while True:
            response = input(f"Did you complete '{habit}'? (y/n): ").strip().lower()
            if response in ("y", "n"):
                results[habit] = "yes" if response == "y" else "no"
                break
            print("Please enter 'y' or 'n'.")



    # Save to log file
    with open(LOG_FILE, "a") as f:
        f.write(f"DAY:{day_number}\n")
        f.write(f"DATE:{today}\n")
        for habit, status in results.items():
            f.write(f"{habit}:{status}\n")
        f.write("---\n")

    # Show summary
    completed = sum(1 for v in results.values() if v == "yes")
    total = len(results)
    percent = round((completed / total) * 100)

    print(f"\nDay {day_number} logged! {completed}/{total} habits done ({percent}%)")
    show_motivation(percent)


def show_motivation(percent):
    if percent == 100:
        print("Perfect day! Keep this streak alive! 🔥")
    elif percent >= 70:
        print("Great job, almost there! Push a little more tomorrow 💪")
    elif percent >= 40:
        print("Decent effort. Tomorrow's a fresh start! 🙂")
    else:
        print("Tough day, that's okay. Don't give up — restart tomorrow!")


# ---------------------------------------------------------
# READING LOG DATA
# ---------------------------------------------------------
def read_all_entries():
    """Parse log file into a list of day-dictionaries."""
    if not os.path.exists(LOG_FILE):
        return []

    entries = []
    current = {}

    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line == "---":
                if current:
                    entries.append(current)
                    current = {}
            elif line.startswith("DAY:"):
                current["day"] = int(line.split(":", 1)[1])
            elif line.startswith("DATE:"):
                current["date"] = line.split(":", 1)[1]
            elif ":" in line:
                habit, status = line.split(":", 1)
                current.setdefault("habits", {})[habit] = status

    return entries


# ---------------------------------------------------------
# VIEW HISTORY
# ---------------------------------------------------------
def view_history():
    entries = read_all_entries()

    if not entries:
        print("\nNo history yet.")
        return

    print("\n=== HISTORY ===")
    for entry in entries:
        print(f"\nDay {entry['day']} - {entry.get('date', '')}")
        for habit, status in entry.get("habits", {}).items():
            mark = "✅" if status == "yes" else "❌"
            print(f"  {mark} {habit}")
        if entry.get("notes"):
            print(f"  Notes: {entry['notes']}")


# ---------------------------------------------------------
# RESET CHALLENGE
# ---------------------------------------------------------
def reset_challenge():
    confirm = input("Are you sure you want to reset everything? (y/n): ").strip().lower()
    if confirm == "y":
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        if os.path.exists(HABITS_FILE):
            os.remove(HABITS_FILE)
        print("Challenge reset! Restart the program to set up again.")
        return True
    return False


# ---------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------
def main():
    print("=" * 40)
    print("   75-DAY CHALLENGE TRACKER")
    print("=" * 40)

    habits = setup_habits()

    while True:
        print("\n--- MENU ---")
        print("1. Log today's progress")
        print("2. View history")
        print("3. Reset challenge")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            log_day(habits)
        elif choice == "2":
            view_history()
        elif choice == "3":
            if reset_challenge():
                break
        elif choice == "4":
            print("\nKeep up the great work! See you tomorrow. 👋")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()