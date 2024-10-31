import tkinter as tk
import requests
import json
from tkinter import messagebox, simpledialog
from src.auth.login import login_user, verify_otp
from src.auth.register import register_user
from src.db import users_collection  # Adjusted path for users_collection

import os
import urllib3



# Assuming secure server endpoint is available at https://localhost:5000
SECURE_SERVER_URL = "https://localhost:5000"

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
        user = users_collection.find_one({"username": username})
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        CERT_DIR = os.path.join(BASE_DIR, 'src', 'certificates')

    # Prepare headers for authorization
        headers = {
        'Authorization': f'Bearer {user["jwt"]}',
        'X-API-Key': user['api_key']
        }
        try:
                    # Get absolute paths for certificates
            client_cert = os.path.join(CERT_DIR, 'client.pem')
            client_key = os.path.join(CERT_DIR, 'client.key')
            server_cert = os.path.join(CERT_DIR, 'rootCA.pem')
        # HTTPS request with mTLS using the client certificate and key
            
            response = requests.get(
                f"{SECURE_SERVER_URL}/profile",
                headers=headers,
                cert=(client_cert, client_key),
                verify=server_cert
            )

            if response.status_code == 200:
                profile_data = response.json()
                # Use the response data to display profile information
                profile_window = tk.Toplevel(self.master)
                profile_window.title("Profile")
                profile_window.geometry("300x200")

                name = profile_data.get('name', username)
                name_label = tk.Label(profile_window, text=f"Name: {name}")
                name_label.pack()
    
                balance_label = tk.Label(profile_window, text=f"Balance: {profile_data.get('balance', 0.0)}")
                balance_label.pack()
    
                # Update Balance section
                new_balance_label = tk.Label(profile_window, text="Update Balance:")
                new_balance_label.pack()
    
                new_balance_entry = tk.Entry(profile_window)
                new_balance_entry.pack()

                def update_balance():
                    try:
                        new_balance = float(new_balance_entry.get())
                        # Prepare data for updating balance
                        data = {'balance': new_balance}
                        update_response = requests.put(
                            f"{SECURE_SERVER_URL}/profile/balance",
                            headers=headers,
                            json=data,
                            cert=(client_cert, client_key),
                            verify=server_cert
                        )
                        if update_response.status_code == 200:
                            messagebox.showinfo("Update Success", "Balance updated successfully!")
                            balance_label.config(text=f"Balance: {new_balance}")
                        else:
                            messagebox.showerror("Update Failed", "Failed to update balance.")
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Please enter a valid balance.")

                update_button = tk.Button(profile_window, text="Update Balance", command=update_balance)
                update_button.pack()

            else:
                messagebox.showerror("Authorization Failed", "Unauthorized access to profile data.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the server: {e}")


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
