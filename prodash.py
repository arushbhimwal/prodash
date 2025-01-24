import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def setup_database():
    # Create or connect to a SQLite database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Create a table for storing account information if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        account_type TEXT NOT NULL CHECK(account_type IN ('Personal', 'Creator', 'Business'))
                    )''')
    conn.commit()
    conn.close()

# Add account to the database
def add_account(username, password, account_type):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Insert account details into the database
    cursor.execute("INSERT INTO accounts (username, password, account_type) VALUES (?, ?, ?)", (username, password, account_type))
    conn.commit()
    conn.close()

# Fetch all accounts from the database
def fetch_accounts():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Retrieve all account records from the database
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    conn.close()
    return accounts

# Delete an account by ID
def delete_account(account_id):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Delete the account with the specified ID
    cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
    conn.commit()
    conn.close()

# Main application class
class InstagramAccountManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Account Manager")
        self.root.geometry("600x400")

        # Frame for adding accounts
        self.add_frame = ttk.LabelFrame(root, text="Add Account")
        self.add_frame.pack(fill="x", padx=10, pady=5)

        # Input for username
        ttk.Label(self.add_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.add_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Input for password
        ttk.Label(self.add_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.add_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Dropdown for account type
        ttk.Label(self.add_frame, text="Account Type:").grid(row=2, column=0, padx=5, pady=5)
        self.account_type_combobox = ttk.Combobox(self.add_frame, values=["Personal", "Creator", "Business"], state="readonly")
        self.account_type_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.account_type_combobox.set("Personal")  # Default selection

        # Button to add account
        self.add_button = ttk.Button(self.add_frame, text="Add Account", command=self.add_account)
        self.add_button.grid(row=3, columnspan=2, pady=10)

        # Frame for displaying accounts
        self.view_frame = ttk.LabelFrame(root, text="Manage Accounts")
        self.view_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview to display account records
        self.account_tree = ttk.Treeview(self.view_frame, columns=("ID", "Username", "Type"), show="headings")
        self.account_tree.heading("ID", text="ID")
        self.account_tree.heading("Username", text="Username")
        self.account_tree.heading("Type", text="Type")
        self.account_tree.column("ID", width=50, anchor="center")
        self.account_tree.column("Username", width=200, anchor="w")
        self.account_tree.column("Type", width=100, anchor="center")
        self.account_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Button to delete selected account
        self.delete_button = ttk.Button(root, text="Delete Selected Account", command=self.delete_selected_account)
        self.delete_button.pack(pady=10)

        self.load_accounts()  # Load accounts into the treeview

    def add_account(self):
        # Get user input values
        username = self.username_entry.get()
        password = self.password_entry.get()
        account_type = self.account_type_combobox.get()

        # Validate input
        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return

        # Add account to database
        add_account(username, password, account_type)
        messagebox.showinfo("Success", "Account added successfully!")
        self.clear_form()  # Clear input fields
        self.load_accounts()  # Reload account list

    def clear_form(self):
        # Reset input fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.account_type_combobox.set("Personal")

    def load_accounts(self):
        # Clear the treeview
        for row in self.account_tree.get_children():
            self.account_tree.delete(row)

        # Fetch accounts from the database and populate the treeview
        accounts = fetch_accounts()
        for account in accounts:
            self.account_tree.insert("", "end", values=(account[0], account[1], account[3]))

    def delete_selected_account(self):
        # Get selected item
        selected_item = self.account_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No account selected.")
            return

        # Get account ID of selected item
        account_id = self.account_tree.item(selected_item[0], "values")[0]
        delete_account(account_id)  # Delete account from database
        messagebox.showinfo("Success", "Account deleted successfully!")
        self.load_accounts()  # Reload account list

# Main execution
if __name__ == "__main__":
    setup_database()  # Ensure the database is ready
    root = tk.Tk()
    app = InstagramAccountManagerApp(root)
    root.mainloop()
