import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="amazon_clone"
)
cursor = conn.cursor()

# Functions to interact with the database
def fetch_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

def add_product(name, price, stock):
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", (name, price, stock))
    conn.commit()
    messagebox.showinfo("Success", "Product added successfully")

def delete_product(product_id):
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    messagebox.showinfo("Success", "Product deleted successfully")

def fetch_orders():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()

# UI Setup
root = tk.Tk()
root.title("Amazon Clone - Admin Panel")
root.geometry("600x400")

# Product Management Section
tk.Label(root, text="Product Management", font=("Arial", 14)).pack()
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Name").grid(row=0, column=0)
tk.Label(frame, text="Price").grid(row=0, column=1)
tk.Label(frame, text="Stock").grid(row=0, column=2)

name_entry = tk.Entry(frame)
name_entry.grid(row=1, column=0)
price_entry = tk.Entry(frame)
price_entry.grid(row=1, column=1)
stock_entry = tk.Entry(frame)
stock_entry.grid(row=1, column=2)

tk.Button(frame, text="Add Product", command=lambda: add_product(name_entry.get(), price_entry.get(), stock_entry.get())).grid(row=1, column=3)

def refresh_product_list():
    for row in tree.get_children():
        tree.delete(row)
    for product in fetch_products():
        tree.insert("", "end", values=product)

tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Stock"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.heading("Stock", text="Stock")
tree.pack()
refresh_product_list()

# Orders Section
tk.Label(root, text="Orders", font=("Arial", 14)).pack()
order_tree = ttk.Treeview(root, columns=("ID", "Product", "Quantity", "Status"), show="headings")
order_tree.heading("ID", text="ID")
order_tree.heading("Product", text="Product")
order_tree.heading("Quantity", text="Quantity")
order_tree.heading("Status", text="Status")
order_tree.pack()

for order in fetch_orders():
    order_tree.insert("", "end", values=order)

root.mainloop()
