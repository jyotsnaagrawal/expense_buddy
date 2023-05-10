import tkinter as tk

from PIL import Image, ImageTk

from ExpenseBuddyGUI import GroupWindow
from ManageGroupGUI import ManageGroupGUI


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
        self.create_large_button(root, "New Group", GroupWindow)

        # Create the "Manage Groups" button
        self.create_large_button(root, "Manage Groups", ManageGroupGUI)

        # Add text on top of the main window
        text_label = tk.Label(root, text="Welcome to the Expense Buddy Bills Split App", font=("Helvetica", 26),
                              bg="white")
        text_label.place(relx=0.5, rely=0.1, anchor="center")

        # Start the main event loop
        root.mainloop()

    def create_large_button(self, root, name, callback_method):
        new_group_button = tk.Button(root, text=name, command=callback_method, padx=70, pady=20, font=60, border=80,
                                     background="white")
        new_group_button.pack(padx=10, pady=100)


gui = ExpenseBuddyApp()
