import tkinter as tk
from tkinter import messagebox, simpledialog
from ..auth.login import login_user, verify_otp
from ..auth.register import register_user
from ..db import users_collection;
class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure Login")
        self.master.geometry("300x200")  # Set initial size for main window
        
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        
        tk.Label(master, text="Username:").grid(row=0, padx=10, pady=10, sticky="e")
        tk.Label(master, text="Password:").grid(row=1, padx=10, pady=10, sticky="e")
        
        self.username_entry = tk.Entry(master, width=25)
        self.password_entry = tk.Entry(master, show="*", width=25)
        
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.login_button = tk.Button(master, text="Login", command=self.login, width=15)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.signup_button = tk.Button(master, text="Signup", command=self.open_signup_window, width=15)
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        result = login_user(username, password)
        if "OTP generated" in result:
            # Prompt the user for the OTP
            user_otp = simpledialog.askstring("OTP Verification", "Enter the OTP sent to your device:")
            if user_otp:
                # Verify the OTP
                otp_result = verify_otp(username, user_otp)
                if "Login successful!" in otp_result:
                    messagebox.showinfo("Login Success", otp_result)
                    # Show profile dialog after API/JWT dialog is closed
                    self.show_profile(username)
                else:
                    messagebox.showerror("Login Failed", otp_result)
            else:
                messagebox.showerror("Login Failed", "OTP input was canceled")
        else:
            messagebox.showerror("Login Failed", result)



    def show_profile(self, username):
        # Fetch user details from MongoDB
        user = users_collection.find_one({"username": username})

        profile_window = tk.Toplevel(self.master)
        profile_window.title("Profile")
        profile_window.geometry("300x200")
           # Fallback to username if 'name' is not present in the document
        
        
        name = user.get('name', username)

        name_label = tk.Label(profile_window, text=f"Name: {name}")
        name_label.pack()

        balance_label = tk.Label(profile_window, text=f"Balance: {user.get('balance', 0.0)}")
        balance_label.pack()

        new_balance_label = tk.Label(profile_window, text="Update Balance:")
        new_balance_label.pack()

        new_balance_entry = tk.Entry(profile_window)
        new_balance_entry.pack()
        def update_balance():
            try:
                new_balance = float(new_balance_entry.get())
                users_collection.update_one(
                    {"username": username}, {"$set": {"balance": new_balance}}
                )
                messagebox.showinfo("Update Success", "Balance updated successfully!")
                balance_label.config(text=f"Balance: {new_balance}")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid balance.")

        update_button = tk.Button(profile_window, text="Update Balance", command=update_balance)
        update_button.pack()


    def open_signup_window(self):
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Signup")
        signup_window.geometry("300x200")  # Set size for signup window
        
        signup_window.grid_columnconfigure(0, weight=1)
        signup_window.grid_columnconfigure(1, weight=1)
        
        tk.Label(signup_window, text="Username:").grid(row=0, padx=10, pady=10, sticky="e")
        tk.Label(signup_window, text="Password:").grid(row=1, padx=10, pady=10, sticky="e")
        
        self.signup_username_entry = tk.Entry(signup_window, width=25)
        self.signup_password_entry = tk.Entry(signup_window, show="*", width=25)
        
        self.signup_username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.signup_password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        signup_button = tk.Button(signup_window, text="Register", command=self.register, width=15)
        signup_button.grid(row=2, column=0, columnspan=2, pady=20)
    
    def register(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Signup Failed", "Please fill all fields")
            return
        
        result = register_user(username, password)
        if "User registered successfully!" in result:
            messagebox.showinfo("Signup Success", result)
        else:
            messagebox.showerror("Signup Failed", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
