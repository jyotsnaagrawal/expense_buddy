import sqlite3


class DatabaseSetup:
    def __init__(self):
        self.conn = sqlite3.connect("expense_buddy.db")
        self.cursor = self.conn.cursor()

        try:
            # Create the "groups" table if it doesn't exist
            self.cursor.execute("CREATE TABLE IF NOT EXISTS groups (name TEXT)")
        except sqlite3.Error:
            print("Error: Groups table could not be created.")

        try:
            # Create the "expenses" table if it doesn't exist
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                amount REAL,
                paid_by TEXT,
                group_name TEXT,
                date TEXT
            )''')
        except sqlite3.Error:
            print("Error: Expenses table could not be created.")

        try:
            # Create the "persons" table if it doesn't exist
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                group_name TEXT
            )''')
        except sqlite3.Error:
            print("Error: Persons table could not be created.")

        try:
            # Create the "expenses" table if it doesn't exist
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses_owe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT,
                owed_by TEXT,
                owe_to TEXT,
                amount REAL
            )''')
        except sqlite3.Error:
            print("Error: expenses_owe table could not be created.")

    # Calling destructor
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_group(self, group_name):
        try:
            # Check if the group name already exists in the database
            self.cursor.execute("SELECT name FROM groups WHERE name=?", (group_name,))
            if self.cursor.fetchone():
                return False
            else:
                # Save the group name in the database
                self.cursor.execute("INSERT INTO groups(name) VALUES(?)", (group_name,))
                self.conn.commit()
                return True
        except sqlite3.Error:
            print(f"Error: group {group_name} could not be created.")

    def get_persons_for_group(self, group_name):
        # Convert group_name to string if necessary
        group_name = str(group_name)

        try:
            # Execute the SQL query
            self.cursor.execute("SELECT name FROM persons WHERE group_name=?", (group_name,))

            # Fetch the results
            return self.cursor.fetchall()
        except sqlite3.Error:
            print("Error: group members could not be retrieved.")
            return None

    def get_all_groups(self):
        try:
            self.cursor.execute("SELECT name FROM groups")
            return self.cursor.fetchall()
        except sqlite3.Error:
            print("Error: group list could not be retrieved.")
            return None

    def add_person_to_group(self, group_name, person_name):
        try:
            # Add the person to the database for the selected group
            self.cursor.execute("INSERT INTO persons (group_name, name) VALUES (?, ?)", (group_name, person_name))
            self.conn.commit()
        except sqlite3.Error:
            print(f"Error: Person {person_name} could not be added to the group {group_name}.")

    def add_expense(self, group_name, date, expense_name, amount, paid_by):
        try:
            self.cursor.execute(
                "INSERT INTO expenses (group_name, date, description, amount, paid_by) "
                "VALUES (?, ?, ?, ?, ?)",
                (group_name, date, expense_name, amount, paid_by))

            self.conn.commit()
        except sqlite3.Error:
            print(f"Error: Expense {expense_name} could not be added to the group {group_name}.")

    def get_all_expenses(self, group_name):
        try:
            self.cursor.execute("SELECT group_name, date, description, amount, paid_by FROM expenses where group_name=?",
                                (group_name,))
            return self.cursor.fetchall()
        except sqlite3.Error:
            print("Error: Expense list could not be retrieved.")
            return None

    def rename_group(self, old_group_name, new_group_name):
        try:
            self.cursor.execute("SELECT name FROM groups WHERE name=?", (new_group_name,))
            group_exists = self.cursor.fetchone()

            if group_exists and group_exists != old_group_name:
                return False
            else:
                # Update the selected group name in the database
                self.cursor.execute("UPDATE groups SET name=? WHERE name=?", (new_group_name, old_group_name))
                self.cursor.execute("UPDATE persons SET group_name=? WHERE group_name=?",
                                    (new_group_name, old_group_name))
                self.cursor.execute("UPDATE expenses SET group_name=? WHERE group_name=?",
                                    (new_group_name, old_group_name))
                self.cursor.execute("UPDATE expenses_owe SET group_name=? WHERE group_name=?",
                                    (new_group_name, old_group_name))
                self.conn.commit()
                return True
        except sqlite3.Error:
            print(f"Error: group {old_group_name} could not be renamed.")
            return False

    def delete_group(self, group_name):
        try:
            self.cursor.execute("DELETE FROM groups WHERE name=?", (group_name,))
            self.cursor.execute("DELETE FROM persons WHERE name=?", (group_name,))
            self.cursor.execute("DELETE FROM expenses WHERE name=?", (group_name,))
            self.cursor.execute("DELETE FROM expenses_owe WHERE name=?", (group_name,))
            self.conn.commit()
        except sqlite3.Error:
            print(f"Error: group {group_name} could not be deleted.")

    def add_expense_owed(self, group_name, owed_by, owe_to, amount):
        try:
            self.cursor.execute("SELECT amount FROM expenses_owe where group_name=? and owed_by=? and owe_to=?",
                                (group_name, owed_by, owe_to))
            existing_amount = self.cursor.fetchone()
            if existing_amount is None:
                self.cursor.execute(
                    "INSERT INTO expenses_owe (group_name, owed_by, owe_to, amount) "
                    "VALUES (?, ?, ?, ?)",
                    (group_name, owed_by, owe_to, amount))
                self.conn.commit()
            else:
                self.cursor.execute(
                    "UPDATE expenses_owe SET amount=? where group_name=? and owed_by=? and owe_to=?",
                                (existing_amount + amount, group_name, owed_by, owe_to))
                self.conn.commit()
        except sqlite3.Error:
            print(f"Error: Expenses owed by {owed_by} owe to {owe_to} could not be added .")

    def get_all_dues(self, group_name):
        try:
            self.cursor.execute("SELECT owed_by, amount, owe_to FROM expenses_owe where group_name=?", (group_name,))
            return self.cursor.fetchall()
        except sqlite3.Error:
            print("Error: Expense owe list could not be retrieved.")
            return None