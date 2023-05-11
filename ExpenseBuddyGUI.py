import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from DatabaseSetup import DatabaseSetup

db = DatabaseSetup()


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

        if db.create_group(group_name):
            # Show a message saying "Group has been created"
            messagebox.showinfo("Success", "Group has been created")
            self.destroy()
        else:
            messagebox.showerror("Error", "Group name already exists")

