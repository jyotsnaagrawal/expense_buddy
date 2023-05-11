import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

from DatabaseSetup import DatabaseSetup
from ExpenseBuddyGUI import GroupWindow

db = DatabaseSetup()


class ManageGroupGUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.selected_group_name = None
        self.persons_listbox = None
        self.expenses_listbox = None
        self.dues_listbox = None
        self.title("Manage Groups (Double click on Group Name)")
        self.groups_listbox = tk.Listbox(self)
        self.groups_listbox.pack(padx=10, pady=50, ipady= 20, ipadx= 30)
        self.scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.groups_listbox.yview)
        self.scrollbar.pack(padx=30, pady=10)
        self.groups_listbox.config(yscrollcommand=self.scrollbar.set)
        self.groups_listbox.bind("<Double-Button-1>", self.on_double_click)
        self.groups_listbox.bind("<<ListboxSelect>>", self.on_select)
        self.modify_button = tk.Button(self, text="Rename", command=self.modify_group_name)
        self.modify_button.pack(padx=10, pady=10, )
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_group_name)
        self.delete_button.pack(padx=10, pady=10)

        # Populate the listbox with group names
        self.populate_listbox()

    def populate_listbox(self):
        # Clear the listbox
        self.groups_listbox.delete(0, tk.END)

        # Get the group names from the database and insert them into the listbox
        groups = db.get_all_groups()
        for group in groups:
            self.groups_listbox.insert(tk.END, group[0])

    def on_double_click(self, _):
        if self.groups_listbox.curselection():
            self.selected_group_name = self.groups_listbox.get(self.groups_listbox.curselection()[0])
            self.create_new_window()

    def on_select(self, _):
        if self.groups_listbox.curselection():
            self.selected_group_name = self.groups_listbox.get(self.groups_listbox.curselection()[0])

    def create_new_window(self):
        new_window = tk.Toplevel(self)
        new_window.title(self.selected_group_name)
        # Set the width and height of the new window
        new_window.geometry("1000x900")

        # Create three buttons in the new window
        person_button = tk.Button(new_window, text="Person", width=40, height=5, background= "White", font=30,
                                  border=10, command=self.show_person_list)
        person_button.pack(padx=30, pady=40)
        expenses_button = tk.Button(new_window, text="Expenses", width=40, height=5, background="White", font=20,
                                    border=10, command=self.show_expense_list)
        expenses_button.pack(padx=50, pady=50)

        to_be_paid_button = tk.Button(new_window, text="To Be Paid", width=40, height=5, background="White", font=20,
                                      border=10, command=self.show_dues_list)
        to_be_paid_button.pack(padx=50, pady=30)

    def show_person_list(self):

        # Create the persons listbox
        # Create a new Toplevel window for showing the person list
        person_list_window = tk.Toplevel(self)
        person_list_window.title("Person List")

        # Create the label and entry box for entering a person's name
        person_name_label = tk.Label(person_list_window, text="Enter Person Name:")
        person_name_label.pack(padx=10, pady=10)
        person_name_entry = tk.Entry(person_list_window)
        person_name_entry.pack(padx=10, pady=10)
        save_button = tk.Button(person_list_window, text="Add", command=lambda: self.add_person(person_name_entry))
        save_button.pack(padx=10, pady=10)

        # Fetch the existing list of persons for the selected group
        persons = db.get_persons_for_group(self.selected_group_name)

        # Create a listbox to display the existing persons
        self.persons_listbox = tk.Listbox(person_list_window)
        self.persons_listbox.pack(padx=10, pady=10)

        # Add the existing persons to the listbox
        for person in persons:
            self.persons_listbox.insert(tk.END, person)

        # Create the "Close" button to close the window
        close_button = tk.Button(person_list_window, text="Close", command=person_list_window.destroy)
        close_button.pack(padx=10, pady=10)

    def add_person(self, person_name_entry):
        # Get the entered person name from the entry box
        person_name = person_name_entry.get()

        # Add the person to the database for the selected group
        db.add_person_to_group(self.selected_group_name, person_name)

        # Clear the entry box
        person_name_entry.delete(0, tk.END)

        # Update the persons listbox with the newly added person
        self.persons_listbox.insert(tk.END, person_name)

    def show_expense_list(self):

        # Create the persons listbox
        # Create a new Toplevel window for showing the person list
        expense_list_window = tk.Toplevel(self)
        expense_list_window.title("Expense List")
        expense_list_window.geometry("300x500")

        save_button = tk.Button(expense_list_window, text="Add Expense", command=lambda: self.show_expenses_window(),
                                font= 5)
        save_button.pack(padx=10, pady=10, ipadx= 10, ipady= 10)

        # Fetch the existing list of persons for the selected group
        expenses = db.get_all_expenses(self.selected_group_name)

        expense_list = []
        for expense in expenses:
            expense_list.append(f"{expense[4]} paid ${expense[3]} on {expense[1]} for {expense[2]}")

        # Create a listbox to display the existing persons
        self.expenses_listbox = tk.Listbox(expense_list_window)
        self.expenses_listbox.pack(padx=30, pady=20, ipadx= 60, ipady= 50)

        # Add the existing persons to the listbox
        self.expenses_listbox.insert(tk.END, *expense_list)

        # Create the "Close" button to close the window
        close_button = tk.Button(expense_list_window, text="Close", command=expense_list_window.destroy, font= 20)
        close_button.pack(pady= 10, padx=10, ipady= 5, ipadx= 20 )

    def show_expenses_window(self):
        # Create a new Toplevel window for expenses
        expenses_window = tk.Toplevel(self)
        expenses_window.title("Expenses")
        expenses_window.geometry("400x400")

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
                                command=lambda: self.save_expense(expenses_window, date_entry.get(),
                                                                  expense_name_entry.get(),
                                                                  expense_amount_entry.get(), self.selected_group_name))

        save_button.pack(padx=10, pady=10)

        # Create a "Close" button to close the window
        close_button = tk.Button(expenses_window, text="Close", command=expenses_window.destroy)
        close_button.pack(padx=10, pady=10)

    def save_expense(self, expenses_window, selected_date, expense_name, expense_amount, selected_group_name):
        # Retrieve the number of persons for the selected group
        persons = db.get_persons_for_group(selected_group_name)
        num_persons = len(persons)

        # Check if there are persons associated with the group
        if num_persons == 0:
            # Handle the case where there are no persons
            # Display an error message or take appropriate action
            expenses_window.destroy()
            messagebox.showerror("Error", "Please add person to the group.")
            return

        # Create a new Toplevel window for selecting the person who paid
        paid_by_window = tk.Toplevel(self)
        paid_by_window.title("Who Paid")
        paid_by_window.geometry("500x500")

        # Create a label for the person selection
        paid_by_label = tk.Label(paid_by_window, text="Who paid for this expense?")
        paid_by_label.pack(padx=10, pady=10)

        # Create a variable to store the selected person
        selected_person = tk.StringVar()

        # Create an OptionMenu to select the person who paid
        paid_by_menu = tk.OptionMenu(paid_by_window, selected_person, *persons)
        paid_by_menu.pack(padx=10, pady=10)

        # Create a button to save the expense with the selected person who paid
        next_button = tk.Button(paid_by_window, text="Next",
                                command=lambda: self.paid_for_check_boxes(selected_date, expense_name, expense_amount,
                                                                          selected_group_name, selected_person))
        next_button.pack(padx=10, pady=10)

    def paid_for_check_boxes(self, selected_date, expense_name, expense_amount, group_name, selected_person):
        # Get the selected person who paid
        paid_by = tk.Entry(textvariable=selected_person).get()

        # Retrieve the number of persons for the selected group
        persons = db.get_persons_for_group(group_name)

        # Create a new Toplevel window for selecting the person who paid
        paid_for_window = tk.Toplevel(self)
        paid_for_window.title("Paid for?")
        paid_for_window.geometry("300x400")

        # Create a label for the person selection
        paid_for_label = tk.Label(paid_for_window, text="Select the people involved in expense:")
        paid_for_label.pack(padx=50, pady=10)

        check_button_dict = {}
        for person in persons:
            check_state = tk.BooleanVar()

            # Create Checkbutton to select the person involved in expense
            checkbox = tk.Checkbutton(paid_for_window, text=person,
                                      variable=check_state,
                                      onvalue=True,
                                      offvalue=False,
                                      height=2,
                                      width=10)
            check_button_dict[person] = [checkbox, check_state]

        for checkbox in check_button_dict:
            check_button_dict[checkbox][0].pack()

        def save_expense_with_paid_by():
            person_list = []
            for person_name in check_button_dict:
                checkbutton = check_button_dict[person_name][1]
                if checkbutton.get():
                    person_list.append(str(person_name[0]))

            # Perform the division
            split_amount = round(float(expense_amount) / len(person_list), 2)

            # Save the expense and split amount in the database
            db.add_expense(group_name, selected_date, expense_name, expense_amount, paid_by)

            for owed_by in person_list:
                db.add_expense_owed(group_name, owed_by, paid_by, split_amount)

            # Show a message indicating that the expense has been saved
            messagebox.showinfo("Success", f"Expense for {selected_date} with name '{expense_name}'"
                                           f" and amount '{expense_amount}' has been saved")

            # Close the paid_by_window
            paid_for_window.destroy()

        # Create a button to save the expense with the selected person who paid
        save_button = tk.Button(paid_for_window, text="Save", command=save_expense_with_paid_by)
        save_button.pack(padx=10, pady=10)

    def show_dues_list(self):

        # Create the persons listbox
        # Create a new Toplevel window for showing the person list
        dues_list_window = tk.Toplevel(self)
        dues_list_window.title("Dues List")

        # Fetch the existing list of persons for the selected group
        amount_dues = db.get_all_dues(self.selected_group_name)
        dues_list = []
        for dues in amount_dues:
            dues_list.append(f"{dues[0]} owes ${dues[1]} to {dues[2]}")

        # Create a listbox to display the existing persons
        self.dues_listbox = tk.Listbox(dues_list_window)
        self.dues_listbox.pack(padx=70, pady=70, ipady= 20, ipadx= 40)

        # Add the existing persons to the listbox
        self.dues_listbox.insert(tk.END, *dues_list)

        # Create the "Close" button to close the window
        close_button = tk.Button(dues_list_window, text="Close", command=dues_list_window.destroy)
        close_button.pack(padx=10, pady=10)

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
                if db.rename_group(self.selected_group_name, new_group_name):
                    # Show a message saying "Group name has been updated"
                    messagebox.showinfo("Success", "Group name has been updated")
                    # Close the "Modify Group" window
                    group_window.destroy()
                else:
                    messagebox.showerror("Error", "Group name already exists")

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
                db.delete_group(self.selected_group_name)

                # Show a message saying "Group has been deleted"
                messagebox.showinfo("Success", "Group has been deleted")

                # Clear the selected group name attribute and repopulate the listbox
                del self.selected_group_name
                self.populate_listbox()
