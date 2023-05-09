import sqlite3


class DatabaseSetup:
    def __init__(self):
        self.conn = sqlite3.connect("expense_buddy.db")
        self.cursor = self.conn.cursor()

        # Create the "groups" table if it doesn't exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS groups (name TEXT)")

        # Create the "expenses" table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            paid_by TEXT,
            group_name TEXT,
            date TEXT
        )''')

        # Create the "persons" table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            group_name TEXT
        )''')

    # Calling destructor
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_group(self, group_name):
        # Check if the group name already exists in the database
        self.cursor.execute("SELECT name FROM groups WHERE name=?", (group_name,))
        if self.cursor.fetchone():
            # Show a message saying "Group name already exists"
            return "Group name already exists"
        else:
            # Save the group name in the database
            self.cursor.execute("INSERT INTO groups(name) VALUES(?)", (group_name,))
            self.conn.commit()

            # Show a message saying "Group has been created"
            return "Group has been created"

    def get_persons_for_group(self, group_name):
        # Convert group_name to string if necessary
        group_name = str(group_name)

        # Execute the SQL query
        self.cursor.execute("SELECT name FROM persons WHERE group_name=?", (group_name,))

        # Fetch the results
        return self.cursor.fetchall()

    def get_all_groups(self):
        self.cursor.execute("SELECT name FROM groups")
        return self.cursor.fetchall()

    def add_person_to_group(self, group_name, person_name):
        # Add the person to the database for the selected group
        self.cursor.execute("INSERT INTO persons (group_name, name) VALUES (?, ?)", (group_name, person_name))
        self.conn.commit()

    def add_expense(self, group_name, date, expense_name, amount, paid_by):
        self.cursor.execute(
            "INSERT INTO expenses (group_name, date, description, amount, paid_by) "
            "VALUES (?, ?, ?, ?, ?)",
            (group_name, date, expense_name, amount, paid_by))

        self.conn.commit()

    def rename_group(self, old_group_name, new_group_name):
        self.cursor.execute("SELECT name FROM groups WHERE name=?", (new_group_name,))
        group_exists = self.cursor.fetchone()

        if group_exists and group_exists != old_group_name:
            # Show an error message if the group name already exists
            return "Group name already exists"
        else:
            # Update the selected group name in the database
            self.cursor.execute("UPDATE groups SET name=? WHERE name=?", (new_group_name, old_group_name))
            self.conn.commit()

            # Show a message saying "Group name has been updated"
            return "Group name has been updated"

    def delete_group(self, group_name):
        self.cursor.execute("DELETE FROM groups WHERE name=?", (group_name,))
        self.conn.commit()