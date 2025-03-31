import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="100719",
    database="mysql",
    auth_plugin='mysql_native_password'
)
cursor = conn.cursor()

# Fetch functions
def fetch_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

def fetch_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

def fetch_orders():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()

# Prompt for input
def prompt_user(title, fields):
    prompt = tk.Toplevel(root)
    prompt.title(title)
    entries = {}
    values = {}
    def submit():
        nonlocal values
        values = {field: entries[field].get() for field in fields}
        prompt.destroy()
    for idx, field in enumerate(fields):
        tk.Label(prompt, text=field).grid(row=idx, column=0)
        entry = tk.Entry(prompt)
        entry.grid(row=idx, column=1)
        entries[field] = entry
    tk.Button(prompt, text="Submit", command=submit).grid(row=len(fields), columnspan=2)
    prompt.wait_window()
    return values

# Add User
def add_user():
    values = prompt_user("Add User", ["User ID", "Name", "Phone", "Address"])
    if values:
        cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (values["User ID"], values["Name"], values["Phone"], values["Address"]))
        conn.commit()
        refresh_users()
        refresh_products()
        refresh_orders()
        messagebox.showinfo("Success", "User added successfully!")

# Add Product
def add_product():
    values = prompt_user("Add Product", ["Product ID", "Name", "Price", "Stock", "Description"])
    if values:
        cursor.execute("INSERT INTO products VALUES (%s, %s, %s, %s, %s)", (values["Product ID"], values["Name"], values["Price"], values["Stock"], values["Description"]))
        conn.commit()
        refresh_users()
        refresh_products()
        refresh_orders()
        messagebox.showinfo("Success", "Product added successfully!")

# Add Order and Update Stock
def add_order():
    values = prompt_user("Add Order", ["Order ID", "User ID", "Product ID", "Quantity"])
    if values:
        order_id, user_id, product_id, quantity = values["Order ID"], values["User ID"], values["Product ID"], int(values["Quantity"])
        cursor.execute("SELECT price, stock FROM products WHERE product_id=%s", (product_id,))
        product = cursor.fetchone()
        if product:
            price, stock = product
            if stock >= quantity:
                total_price = price * quantity
                cursor.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s, 'Pending')", (order_id, user_id, product_id, quantity, total_price))
                cursor.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))
                conn.commit()
                refresh_users()
                refresh_products()
                refresh_orders()
                messagebox.showinfo("Success", "Order placed successfully!")
            else:
                messagebox.showerror("Error", "Not enough stock!")
        else:
            messagebox.showerror("Error", "Product not found!")

# Refresh functions
def refresh_users():
    for row in user_tree.get_children():
        user_tree.delete(row)
    for user in fetch_users():
        user_tree.insert("", "end", values=user)

def refresh_products():
    for row in product_tree.get_children():
        product_tree.delete(row)
    for product in fetch_products():
        product_tree.insert("", "end", values=product)

def refresh_orders():
    for row in order_tree.get_children():
        order_tree.delete(row)
    for order in fetch_orders():
        order_tree.insert("", "end", values=order)

# Tkinter UI
root = tk.Tk()
root.title("Ecommerce Admin Panel")
root.geometry("800x600")

# Users Section
tk.Label(root, text="Users", font=("Arial", 14)).pack()
user_tree = ttk.Treeview(root, columns=("ID", "Name", "Phone", "Address"), show="headings")
user_tree.heading("ID", text="ID")
user_tree.heading("Name", text="Name")
user_tree.heading("Phone", text="Phone")
user_tree.heading("Address", text="Address")
user_tree.pack()
refresh_users()

# Add User Button
tk.Button(root, text="Add User", command=add_user).pack()

# Products Section
tk.Label(root, text="Products", font=("Arial", 14)).pack()
product_tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Stock"), show="headings")
product_tree.heading("ID", text="ID")
product_tree.heading("Name", text="Name")
product_tree.heading("Price", text="Price")
product_tree.heading("Stock", text="Stock")
product_tree.pack()
refresh_products()

# Add Product Button
tk.Button(root, text="Add Product", command=add_product).pack()

# Orders Section
tk.Label(root, text="Orders", font=("Arial", 14)).pack()
order_tree = ttk.Treeview(root, columns=("ID", "User", "Product", "Quantity", "Total Price", "Status"), show="headings")
order_tree.heading("ID", text="ID")
order_tree.heading("User", text="User")
order_tree.heading("Product", text="Product")
order_tree.heading("Quantity", text="Quantity")
order_tree.heading("Total Price", text="Total Price")
order_tree.heading("Status", text="Status")
order_tree.pack()
refresh_orders()

# Add Order Button
tk.Button(root, text="Add Order", command=add_order).pack()

root.mainloop()
