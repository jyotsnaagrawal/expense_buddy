import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk


class GroupWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Create New Group")
        # Set the width and height of the new window
        self.geometry("1000x900")
        # Load the image
        image2 = Image.open("Money split.jpg")
        # Resize the image if needed
        resized_image = image2.resize((300, 300))  # Adjust the size as per your requirements

        # Convert the image to a Tkinter-compatible format
        photo = ImageTk.PhotoImage(resized_image)

        # Create a Label widget to display the image
        self.image_label = tk.Label(self, image=photo, background="Black", border=50)
        self.image_label.image = photo  # Keep a reference to the image
        self.image_label.pack(padx=10, pady=10)
        self.group_name_label = tk.Label(self, text="Create New Group", font=65, border=10)
        self.group_name_label.pack(padx=10, pady=10)
        self.group_name_entry = tk.Entry(self, border=20)
        self.group_name_entry.pack(padx=10, pady=10, ipady=20, ipadx=70)
        self.save_button = tk.Button(self, text="Save", command=self.save_group_name, background="GREEN", font=80,
                                     border=20)
        self.save_button.pack(padx=10, pady=10, ipadx=50, ipady=10, )

    def save_group_name(self):
        # Get the group name entered by the user
        group_name = self.group_name_entry.get()

        # Check if the group name already exists in the database
        cursor.execute("SELECT name FROM groups WHERE name=?", (group_name,))
        if cursor.fetchone():
            # Show a message saying "Group name already exists"
            messagebox.showerror("Error", "Group name already exists")
        else:
            # Save the group name in the database
            cursor.execute("INSERT INTO groups(name) VALUES(?)", (group_name,))
            conn.commit()

            # Show a message saying "Group has been created"
            messagebox.showinfo("Success", "Group has been created")

            # Close the "Create New Group" window
            self.destroy()


def get_persons_for_group(group_name):
    # Convert group_name to string if necessary
    group_name = str(group_name)

    # Execute the SQL query
    cursor.execute("SELECT name FROM persons WHERE group_name=?", (group_name,))

    # Fetch the results
    persons = cursor.fetchall()

    # Process the results if needed

    return persons


class ManageGroupsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.selected_group_name = None
        self.persons_listbox = None
        self.title("Manage Groups")
        self.groups_listbox = tk.Listbox(self)
        self.groups_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.groups_listbox.yview)
        self.scrollbar.grid(row=0, column=1, padx=10, pady=10, sticky="NS")
        self.groups_listbox.config(yscrollcommand=self.scrollbar.set)
        self.groups_listbox.bind("<Double-Button-1>", self.on_select)
        self.modify_button = tk.Button(self, text="Rename", command=self.modify_group_name)
        self.modify_button.grid(row=1, column=1, padx=10, pady=10)
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_group_name)
        self.delete_button.grid(row=1, column=2, padx=10, pady=10)
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
        table_exists = cursor.fetchone()

        # If the table does not exist, create it
        if not table_exists:
            cursor.execute('''CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                amount REAL,
                paid_by TEXT,
                group_name TEXT,
                date TEXT
            )''')

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='persons'")
        table_exists = cursor.fetchone()

        # If the table does not exist, create it
        if not table_exists:
            cursor.execute('''CREATE TABLE persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                group_name TEXT
            )''')

        # Populate the listbox with group names
        self.populate_listbox()

    def populate_listbox(self):
        # Clear the listbox
        self.groups_listbox.delete(0, tk.END)

        # Get the group names from the database and insert them into the listbox
        cursor.execute("SELECT name FROM groups")
        groups = cursor.fetchall()
        for group in groups:
            self.groups_listbox.insert(tk.END, group[0])

    def on_select(self, _):
        if self.groups_listbox.curselection():
            self.selected_group_name = self.groups_listbox.get(self.groups_listbox.curselection()[0])
            self.create_new_window()

    def create_new_window(self):
        new_window = tk.Toplevel(self)
        new_window.title(self.selected_group_name)
        # Set the width and height of the new window
        new_window.geometry("1000x900")

        # Create three buttons in the new window
        person_button = tk.Button(new_window, text="Person", width=40, height=10, background="green", font=20,
                                  border=20, command=self.show_person_list)
        person_button.pack(padx=30, pady=30)
        expenses_button = tk.Button(new_window, text="Expenses", width=40, height=10, background="green", font=20,
                                    border=20, command=self.show_expenses_window)
        expenses_button.pack(padx=30, pady=10)

        to_be_paid_button = tk.Button(new_window, text="To Be Paid", width=40, height=10, background="green", font=20,
                                      border=20)
        to_be_paid_button.pack(padx=30, pady=10)

    def show_person_list(self):

        # Create the persons listbox
        # Create a new Toplevel window for showing the person list
        person_list_window = tk.Toplevel(self)
        person_list_window.title("Person List")

        # Create the label and entry box for entering a person's name
        person_name_label = tk.Label(person_list_window, text="Enter Person Name:")
        person_name_label.grid(row=0, column=0, padx=10, pady=10)
        person_name_entry = tk.Entry(person_list_window)
        person_name_entry.grid(row=0, column=1, padx=10, pady=10)
        save_button = tk.Button(person_list_window, text="Save", command=lambda: self.save_person(person_name_entry))
        save_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Fetch the existing list of persons for the selected group
        persons = get_persons_for_group(self.selected_group_name)

        # Create a listbox to display the existing persons
        self.persons_listbox = tk.Listbox(person_list_window)
        self.persons_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

        # Add the existing persons to the listbox
        for person in persons:
            self.persons_listbox.insert(tk.END, person)

        # Create the "Back" button to go back to the previous window
        back_button = tk.Button(person_list_window, text="Back", command=person_list_window.destroy)
        back_button.grid(row=3, column=1, padx=10, pady=10)

    def save_person(self, person_name_entry):
        # Get the entered person name from the entry box
        person_name = person_name_entry.get()

        # Add the person to the database for the selected group
        cursor.execute("INSERT INTO persons (group_name, name) VALUES (?, ?)", (self.selected_group_name, person_name))
        conn.commit()

        # Clear the entry box
        person_name_entry.delete(0, tk.END)

        # Update the persons listbox with the newly added person
        self.persons_listbox.insert(tk.END, person_name)

    def add_person(self, person_name_entry):
        # Get the entered person name from the entry box
        person_name = person_name_entry.get()

        # Add the person to the database for the selected group
        cursor.execute("INSERT INTO persons (group_name, name) VALUES (?, ?)", (self.selected_group_name, person_name))
        conn.commit()

        # Clear the entry box
        person_name_entry.delete(0, tk.END)

        # Update the persons listbox with the newly added person
        self.persons_listbox.insert(tk.END, person_name)

    def show_expenses_window(self):
        # Create a new Toplevel window for expenses
        expenses_window = tk.Toplevel(self)
        expenses_window.title("Expenses")

        # Create a label for date selection
        date_label = tk.Label(expenses_window, text="Select Date:")
        date_label.pack(padx=10, pady=10)

        # Create a DateEntry widget
        date_entry = DateEntry(expenses_window, width=12, background='dark-blue',
                               foreground='white', borderwidth=2)
        date_entry.pack(padx=10, pady=10)

        # Create a label for expense name entry
        expense_name_label = tk.Label(expenses_window, text="Expense Name:")
        expense_name_label.pack(padx=10, pady=10)

        # Create an entry box for expense name
        expense_name_entry = tk.Entry(expenses_window)
        expense_name_entry.pack(padx=10, pady=10)

        # Create a label for expense amount entry
        expense_amount_label = tk.Label(expenses_window, text="Expense Amount:")
        expense_amount_label.pack(padx=10, pady=10)

        # Create an entry box for expense amount
        expense_amount_entry = tk.Entry(expenses_window)
        expense_amount_entry.pack(padx=10, pady=10)

        # Create a button to save the expense
        save_button = tk.Button(expenses_window, text="Save",
                                command=lambda: self.save_expense(date_entry.get(), expense_name_entry.get(),
                                                                  expense_amount_entry.get(), self.selected_group_name))

        save_button.pack(padx=10, pady=10)

        # Create a button to go back to the previous window
        back_button = tk.Button(expenses_window, text="Back", command=expenses_window.destroy)
        back_button.pack(padx=10, pady=10)

    def save_expense(self, selected_date, expense_name, expense_amount, selected_group_name):
        # Retrieve the number of persons for the selected group
        persons = get_persons_for_group(selected_group_name)
        num_persons = len(persons)

        # Check if there are persons associated with the group
        if num_persons == 0:
            # Handle the case where there are no persons
            # Display an error message or take appropriate action
            return

        # Perform the division
        split_amount = round(float(expense_amount) / num_persons, 2)

        # Create a new Toplevel window for selecting the person who paid
        paid_by_window = tk.Toplevel(self)
        paid_by_window.title("Who Paid")

        # Create a label for the person selection
        paid_by_label = tk.Label(paid_by_window, text="Who paid for this expense?")
        paid_by_label.pack(padx=10, pady=10)

        # Create a variable to store the selected person
        selected_person = tk.StringVar()

        # Create an OptionMenu to select the person who paid
        paid_by_menu = tk.OptionMenu(paid_by_window, selected_person, *persons)
        paid_by_menu.pack(padx=10, pady=10)

        def save_expense_with_paid_by():
            # Get the selected person who paid
            paid_by = selected_person.get()

            # Save the expense and split amount in the database
            cursor.execute(
                "INSERT INTO expenses (group_name, date, description, amount, paid_by) "
                "VALUES (?, ?, ?, ?, ?)",
                (selected_group_name, selected_date, expense_name, expense_amount, paid_by))

            conn.commit()

            # Show a message indicating that the expense has been saved
            messagebox.showinfo("Success", f"Expense for {selected_date} with name '{expense_name}'"
                                           f" and amount '{expense_amount}' has been saved")

            # Close the paid_by_window
            paid_by_window.destroy()

        # Create a button to save the expense with the selected person who paid
        save_button = tk.Button(paid_by_window, text="Save", command=save_expense_with_paid_by)
        save_button.pack(padx=10, pady=10)

    def modify_group_name(self):
        if hasattr(self, "selected_group_name"):
            group_window = GroupWindow(self)
            group_window.title("Modify Group")

            # Set the group name entry to the selected group name
            group_window.group_name_entry.insert(0, self.selected_group_name)

            def save_modified_group_name():
                # Get the modified group name from the entry field
                new_group_name = group_window.group_name_entry.get()

                # Check if the new group name already exists in the database
                cursor.execute("SELECT name FROM groups WHERE name=?", (new_group_name,))
                group_exists = cursor.fetchone()

                if group_exists and group_exists[0] != self.selected_group_name:
                    # Show an error message if the group name already exists
                    messagebox.showerror("Error", "Group name already exists")
                else:
                    # Update the selected group name in the database
                    cursor.execute("UPDATE groups SET name=? WHERE name=?", (new_group_name, self.selected_group_name))
                    conn.commit()

                    # Show a message saying "Group name has been updated"
                    messagebox.showinfo("Success", "Group name has been updated")

                    # Close the "Modify Group" window
                    group_window.destroy()

                    # Clear the selected group name attribute and repopulate the listbox
                    del self.selected_group_name
                    self.populate_listbox()

            # Replace the save_group_name method with the save_modified_group_name method
            group_window.save_button.config(command=save_modified_group_name)
        # Create a new GroupWindow object and set its title to "Modify Group"

    def delete_group_name(self):
        if hasattr(self, "selected_group_name"):
            # Show a confirmation message before deleting the group name
            response = messagebox.askyesno("Confirm",
                                           f"Are you sure you want to delete the group '{self.selected_group_name}'?")

            if response == tk.YES:
                # Delete the selected group name from the database
                cursor.execute("DELETE FROM groups WHERE name=?", (self.selected_group_name,))
                conn.commit()

                # Show a message saying "Group has been deleted"
                messagebox.showinfo("Success", "Group has been deleted")

                # Clear the selected group name attribute and repopulate the listbox
                del self.selected_group_name
                self.populate_listbox()


# Create a new main window


root = tk.Tk()
root.title("Bills Split App")
root.geometry("1000x900")
# Load the background image
image = Image.open("Money split.jpg")
background_image = ImageTk.PhotoImage(image)

# Create a label widget to display the background image
background_label = tk.Label(root, image=background_image, background="bLACK")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a connection to the database
conn = sqlite3.connect("new_bills.db")
cursor = conn.cursor()
# Create the "groups" table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS groups (name TEXT)")
conn.commit()

# Create the "New Group" button
new_group_button = tk.Button(root, text="New Group", command=GroupWindow, padx=70, pady=20, font=60, border=100,
                             background="white")
new_group_button.pack(padx=10, pady=100)

# Create the "Manage Groups" button
manage_groups_button = tk.Button(root, text="Manage Groups", command=ManageGroupsWindow, padx=70, pady=20,
                                 font=60, border=100, background="white")
manage_groups_button.pack(padx=10, pady=10)
# Add text on top of the main window
text_label = tk.Label(root, text="Welcome to the Bills Split App", font=("Helvetica", 26), bg="white")
text_label.place(relx=0.5, rely=0.1, anchor="center")

# Start the main event loop
root.mainloop()

# Close the database connection
conn.close()
