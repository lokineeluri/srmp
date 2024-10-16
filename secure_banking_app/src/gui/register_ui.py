import tkinter as tk
from tkinter import messagebox
from ..auth.register import register_user

class RegisterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("User Registration")
        self.master.geometry("300x200")  # Set the width and height of the window
        
        tk.Label(master, text="Username:").grid(row=0, padx=10, pady=10)
        tk.Label(master, text="Password:").grid(row=1, padx=10, pady=10)
        
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")
        
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1, pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        result = register_user(username, password)
        if "User registered successfully!" in result:
            messagebox.showinfo("Registration Success", result)
        else:
            messagebox.showerror("Registration Failed", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterApp(root)
    root.mainloop()
