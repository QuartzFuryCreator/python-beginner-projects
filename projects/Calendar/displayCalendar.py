import calendar

# A dictionary to store events by date
events = {}

def display_cal(year_input, month_input):
    """
    Display a calendar for the desired year and month.
    """
    print(calendar.month(year_input, month_input))
    display_events(year_input, month_input)

def fetch_year():
    """
    Prompts the user for a valid year and returns the year as an integer.
    """
    while True:
        try:
            year_input = int(input("Enter year: "))
            if year_input < 0:
                raise ValueError("Year must be a positive integer")
            return year_input
        except ValueError:
            print("Invalid input. Please enter a valid year.")

def fetch_month():
    """
    Function that asks the user to enter a month, validates the input, and returns the valid month.
    """
    while True:
        try:
            month_input = int(input("Enter month: "))
            if month_input < 1 or month_input > 12:
                raise ValueError("Month must be between 1 and 12")
            return month_input
        except ValueError:
            print("Invalid input. Please enter a valid month.")

def add_event(year_input, month_input):
    """
    Add an event to a specific date.
    """
    day_input = int(input("Enter day for the event (1-31): "))
    event_title = input("Enter event title: ")

    # Validate the day
    if day_input < 1 or day_input > 31:
        print("Invalid day. Please enter a day between 1 and 31.")
        return

    # Store event in dictionary
    date_key = f"{year_input}-{month_input:02d}-{day_input:02d}"
    events[date_key] = event_title
    print(f"✅ Event '{event_title}' added to {date_key}")

def view_events():
    """
    View all added events.
    """
    if not events:
        print("No events added yet.")
    else:
        print("\nUpcoming Events:")
        for date, event in events.items():
            print(f"{date} - {event}")

def delete_event():
    """
    Deletes an event from the events dictionary.
    """
    if not events:
        print("No events to delete.")
        return

    print("\nYour Events:")
    for idx, (date, event) in enumerate(events.items(), 1):
        print(f"{idx}. {date} - {event}")

    try:
        choice = int(input("Enter the event number to delete: "))
        if 1 <= choice <= len(events):
            date_to_delete = list(events.keys())[choice - 1]
            removed_event = events.pop(date_to_delete)
            print(f"✅ Event '{removed_event}' on {date_to_delete} deleted successfully!")
        else:
            print("❌ Invalid event number.")
    except ValueError:
        print("❌ Please enter a valid number.")

def display_events(year_input, month_input):
    """
    Display all events for a specific month and year.
    """
    print("\nEvents in the calendar:")
    for date, event in events.items():
        event_year, event_month, _ = date.split("-")
        if int(event_year) == year_input and int(event_month) == month_input:
            print(f"{date} - {event}")

def main_menu():
    year_input = fetch_year()
    month_input = fetch_month()

    while True:
        print("\nMenu:")
        print("1. Display Calendar")
        print("2. Add Event")
        print("3. View Events")
        print("4. Delete Event")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            display_cal(year_input, month_input)
        elif choice == "2":
            add_event(year_input, month_input)
        elif choice == "3":
            view_events()
        elif choice == "4":
            delete_event()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    main_menu()
