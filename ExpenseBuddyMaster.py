"""
Description About What my program purpose:-
**My project Expenses_Bills_Buddy is an application to split expenses between a group of people,
which will help users calculate the amount each person owes and generate a report of the split expenses.
The application has been built using Python programming language, and the GUI is created using the Tkinter library.
Following Libraries has been used while building this application:-

Tkinter
PIL/Image
PIL/ImageTk(https://www.activestate.com/resources/quick-reads/how-to-add-images-in-tkinter/
File | Settings | Project: expense_buddy | Python Interpreter add + button for searching PIL Tool
tkcalendar (File | Settings | Project: expense_buddy | Python Interpreter add + button for searching tkcalendar)
https://www.geeksforgeeks.org/create-a-date-picker-calendar-tkinter/
Sqlite3**
To run this application please run ExpenseBuddyMaster.py file
Resources and help
# (Gaddis, 2022)
# PIL libraries and image tk I learnt from Google and how to find in pycharm learnt by self exploring pycharm
# image sources saved by google (Adobe Stock)

"""
import tkinter as tk

from PIL import Image, ImageTk

from ExpenseBuddyGUI import GroupWindow
from ManageGroupGUI import ManageGroupGUI


def create_large_button(root, name, callback_method):
    new_group_button = tk.Button(root, text=name, command=callback_method, padx=70, pady=14, font=60, border=80,
                                 background="white")
    new_group_button.pack(padx=60, pady=95)


class ExpenseBuddyApp:
    def __init__(self):
        root = tk.Tk()
        root.title("Expense Buddy App")
        root.geometry("1000x900")
        # Load the background image
        image = Image.open("Money split.jpg")
        background_image = ImageTk.PhotoImage(image)

        # Create a label widget to display the background image
        background_label = tk.Label(root, image=background_image, background="black")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the "New Group" button
        create_large_button(root, "New Group", GroupWindow)

        # Create the "Manage Groups" button
        create_large_button(root, "Manage Groups", ManageGroupGUI)

        # Add text on top of the main window
        text_label = tk.Label(root, text="Welcome to the Expense Buddy Bills Split App", font=("Helvetica", 26),
                              bg="white")
        text_label.place(relx=0.5, rely=0.1, anchor="center")

        # Start the main event loop
        root.mainloop()


def main():
    # Start the application.
    ExpenseBuddyApp()


main()