import tkinter as tk

from PIL import Image, ImageTk

from DatabaseSetup import DatabaseSetup
from ExpenseBuddyGUI import GroupWindow
from ManageGroupGUI import ManageGroupGUI

db = DatabaseSetup()


def main():
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
    new_group_button = tk.Button(root, text="New Group", command=GroupWindow, padx=70, pady=20, font=60, border=100,
                                 background="white")
    new_group_button.pack(padx=10, pady=100)

    # Create the "Manage Groups" button
    manage_groups_button = tk.Button(root, text="Manage Groups", command=ManageGroupGUI, padx=70, pady=20,
                                     font=60, border=100, background="white")
    manage_groups_button.pack(padx=10, pady=10)
    # Add text on top of the main window
    text_label = tk.Label(root, text="Welcome to the Expense Buddy Bills Split App", font=("Helvetica", 26), bg="white")
    text_label.place(relx=0.5, rely=0.1, anchor="center")

    # Start the main event loop
    root.mainloop()


main()
