### CREATED BY AHMED SALEH ALSAYADI 
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedStyle
import sqlite3
from tkinter import ttk
import subprocess  # Import the subprocess module

# Create a connection to the SQLite database
conn = sqlite3.connect("userdata.db")
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
""")
conn.commit()

def show_login():
  login_frame.grid(row=0, column=0, sticky="nsew")
  signup_frame.grid_forget()

def show_signup():
  signup_frame.grid(row=0, column=0, sticky="nsew")
  login_frame.grid_forget()

def login():
  # Implement your login logic here
  username = username_entry.get()
  password = password_entry.get()

  # Example validation
  cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
  if cursor.fetchone() is not None:
    messagebox.showinfo("Login", "Login successful!")
    # Run the upload.py script on successful login
    try:
        subprocess.run(["python", "upload.py"])
    except FileNotFoundError:
        messagebox.showerror("Login", "upload.py script not found.")
  else:
    messagebox.showerror("Login", "Invalid username or password.")

def signup():
  # Implement your signup logic here
  username = new_username_entry.get()
  password = new_password_entry.get()

  # Example validation
  if len(username) > 0 and len(password) > 0:
    try:
      # Insert the user data into the users table
      cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
      conn.commit()
      messagebox.showinfo("Signup", "Signup successful!")
    except sqlite3.IntegrityError:
      messagebox.showerror("Signup", "Username already exists.")
  else:
    messagebox.showerror("Signup", "Invalid username or password.")

# Create the main window
window = tk.Tk()
window.title("Signup/Login GUI")

# Set window size and background color
# Set window size and background color
window.geometry("600x600")  # Adjust width and height as desired
window.config(bg="#30365e")  # Set background color to black

# Show the window controls
window.overrideredirect(False)

# Apply a themed style to the window (optional)
# Apply a themed style to the window
style = ThemedStyle(window)
style.set_theme("adapta")

# Create a custom style for the entry widget
entry_style = ttk.Style()
entry_style.configure("Custom.TEntry",
                      fieldbackground="black",
                      foreground="black",
                      borderwidth=0,
                      background="black",
                      focuscolor="",
                      padding=5
                     )
# Configure the style for various elements
style.configure("TLabel", foreground="white", background="#ff1919", font=("Helvetica", 15))
style.configure("TEntry", background="#1A1B1D", foreground="white", font=("Helvetica", 15))
# Create a global padding variable for consistency
padding = 20

global_margin = 105

# Create the login frame
login_frame = tk.Frame(window, padx=global_margin)
login_frame.config(bg="#30365e")  # Set login frame background

login_label = tk.Label(login_frame, text="Login", font=("Helvetica", 25, "bold"), fg="white", bg="#30365e")
login_label.grid(row=0, column=0, columnspan=2, pady=padding)

username_label = tk.Label(login_frame, text="Username:", fg="white", bg="#30365e", font=("Helvetica", 14, "bold"))
username_label.grid(row=1, column=1, sticky="w", padx=(padding, 0), pady=padding/10)
username_entry = ttk.Entry(login_frame, width=44, style="Custom.TEntry")
username_entry.grid(row=2, column=1, padx=(padding, 0), pady=padding)  # Adjust left padding

password_label = tk.Label(login_frame, text="Password:", fg="white", bg="#30365e", font=("Helvetica", 14, "bold"))
password_label.grid(row=3, column=1, sticky="w", padx=(padding, 0), pady=padding/10)
password_entry = ttk.Entry(login_frame, show="*", width=44, style="Custom.TEntry")
password_entry.grid(row=4, column=1, padx=(padding, 0), pady=padding)  # Adjust left padding

login_button = tk.Button(login_frame, text="Login", command=login, width=25, fg="white", bg="#005ab6", font=("Helvetica", 14, "underline"))
login_button.grid(row=5, column=1, columnspan=2, padx=(padding, 0), pady=padding)

signup_link = tk.Label(login_frame, text="Don't have an account? Sign up!",
                        fg="#2196f3", bg="#30365e", cursor="hand2", font=("Helvetica", 14, "underline"))
signup_link.grid(row=6, column=1, columnspan=2, pady=padding)
signup_link.bind("<Button-1>", lambda e: show_signup())

# Create the signup frame
signup_frame = tk.Frame(window, padx=global_margin)
signup_frame.config(bg="#30365e")  # Set signup frame background

signup_label = tk.Label(signup_frame, text="Signup", font=("Helvetica", 25, "bold"), fg="white", bg="#30365e")
signup_label.grid(row=0, column=0, columnspan=2, pady=padding)

new_username_label = tk.Label(signup_frame, text="New Username:", fg="white", bg="#30365e", font=("Helvetica", 14, "bold"))
new_username_label.grid(row=1, column=1, sticky="w", padx=(padding, 0), pady=padding/10)
new_username_entry = ttk.Entry(signup_frame,  width=44, style="Custom.TEntry")
new_username_entry.grid(row=2, column=1, padx=(padding, 0), pady=padding)  # Adjust left padding

new_password_label = tk.Label(signup_frame, text="New Password:", fg="white", bg="#30365e", font=("Helvetica", 14, "bold"))
new_password_label.grid(row=3, column=1, sticky="w", padx=(padding, 0), pady=padding/10)
new_password_entry = ttk.Entry(signup_frame, show="*",  width=44, style="Custom.TEntry")
new_password_entry.grid(row=4, column=1, padx=(padding, 0), pady=padding)  # Adjust left padding

signup_button = tk.Button(signup_frame, text="Signup", command=signup, width=25, fg="white", bg="#005ab6", bd=2, font=("Helvetica", 14, "underline"))
signup_button.grid(row=5, column=1, columnspan=4, padx=(padding, 0), pady=padding)

login_link = tk.Label(signup_frame, text="Already have an account? Login!",
                    fg="#2196f3", bg="#30365e", cursor="hand2", font=("Helvetica", 14, "underline"))
login_link.grid(row=6, column=0, columnspan=2, pady=padding)
login_link.bind("<Button-1>", lambda e: show_login())

# Show the login frame initially
show_login()

# Start the main event loop
window.mainloop()

conn.close()  # Close the database connection at the end
