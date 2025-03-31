import sys
import mysql.connector
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, 
                             QFrame, QFormLayout, QDialog)
from PyQt5.QtCore import Qt

class AmazonAdminUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Amazon Admin Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        # Database Connection
        self.conn = mysql.connector.connect(host="localhost", user="root", password="100719", database="mysql", auth_plugin='mysql_native_password')
        self.cursor = self.conn.cursor()
        
        # Main Layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Content Area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        main_layout.addWidget(self.content_area)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self.load_users()

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #232F3E; color: white;")
        
        sidebar_layout = QVBoxLayout()
        
        menu_items = [
            ("Users", self.load_users),
            ("Products", self.load_products),
            ("Orders", self.load_orders)
        ]
        
        for item, function in menu_items:
            button = QPushButton(item)
            button.setStyleSheet("color: white; background-color: transparent; border: none; padding: 10px;")
            button.clicked.connect(function)
            sidebar_layout.addWidget(button)
        
        sidebar_layout.addStretch(1)
        sidebar.setLayout(sidebar_layout)
        return sidebar
    
    def load_users(self):
        self.clear_content()
        
        label = QLabel("Users")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.content_layout.addWidget(label)
        
        add_button = QPushButton("Add User")
        add_button.clicked.connect(self.add_user)
        self.content_layout.addWidget(add_button)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["User ID", "Full Name", "Phone", "Address"])
        
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            for col, value in enumerate(user):
                table.setItem(row, col, QTableWidgetItem(str(value)))
        
        self.content_layout.addWidget(table)
    
    def load_products(self):
        self.clear_content()
        
        label = QLabel("Products")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.content_layout.addWidget(label)
        
        add_button = QPushButton("Add Product")
        add_button.clicked.connect(self.add_product)
        self.content_layout.addWidget(add_button)
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Product ID", "Name", "Price", "Stock", "Description"])
        
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            for col, value in enumerate(product):
                table.setItem(row, col, QTableWidgetItem(str(value)))
        
        self.content_layout.addWidget(table)
    
    def load_orders(self):
        self.clear_content()
        
        label = QLabel("Orders")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.content_layout.addWidget(label)
        
        add_button = QPushButton("Add Order")
        add_button.clicked.connect(self.add_order)
        self.content_layout.addWidget(add_button)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Order ID", "User ID", "Product ID", "Quantity"])
        
        self.cursor.execute("SELECT * FROM orders")
        orders = self.cursor.fetchall()
        table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            for col, value in enumerate(order):
                table.setItem(row, col, QTableWidgetItem(str(value)))
        
        self.content_layout.addWidget(table)
    
    def add_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add User")
        layout = QFormLayout()
        
        user_id = QLineEdit()
        full_name = QLineEdit()
        phone = QLineEdit()
        address = QLineEdit()
        
        layout.addRow("User ID:", user_id)
        layout.addRow("Full Name:", full_name)
        layout.addRow("Phone:", phone)
        layout.addRow("Address:", address)
        
        submit_btn = QPushButton("Add")
        submit_btn.clicked.connect(lambda: self.insert_user(dialog, user_id.text(), full_name.text(), phone.text(), address.text()))
        layout.addWidget(submit_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def add_product(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Product")
        dialog_layout = QFormLayout()
        
        product_id_input = QLineEdit()
        name_input = QLineEdit()
        price_input = QLineEdit()
        stock_input = QLineEdit()
        description_input = QLineEdit()
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.insert_product(dialog, product_id_input.text(), name_input.text(), price_input.text(), stock_input.text(), description_input.text()))
        
        dialog_layout.addRow("Product ID:", product_id_input)
        dialog_layout.addRow("Product Name:", name_input)
        dialog_layout.addRow("Price:", price_input)
        dialog_layout.addRow("Stock:", stock_input)
        dialog_layout.addRow("Description:", description_input)
        dialog_layout.addRow(add_button)
        
        dialog.setLayout(dialog_layout)
        dialog.exec_()
        
        self.load_products()
        
    def insert_user(self, dialog, user_id, full_name, phone, address):
        self.cursor.execute("INSERT INTO users (user_id, full_name, phone, address) VALUES (%s, %s, %s, %s)", (user_id, full_name, phone, address))
        self.conn.commit()
        dialog.close()
        self.load_users()
    
    def insert_product(self, dialog, product_id, name, price, stock, description):
        self.cursor.execute("INSERT INTO products (product_id, name, price, stock, description) VALUES (%s, %s, %s, %s, %s)", (product_id, name, price, stock, description))
        self.conn.commit()
        dialog.close()
        self.load_products()

    def add_order(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Order")
        dialog_layout = QFormLayout()
        
        order_id_input = QLineEdit()
        user_id_input = QLineEdit()
        product_id_input = QLineEdit()
        quantity_input = QLineEdit()
        status_input = QLineEdit()
        price_input = QLineEdit()
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.insert_order(dialog, order_id_input.text(), user_id_input.text(), product_id_input.text(), quantity_input.text(), status_input.text(), price_input.text()))
        
        dialog_layout.addRow("Order ID:", order_id_input)
        dialog_layout.addRow("User ID:", user_id_input)
        dialog_layout.addRow("Product ID:", product_id_input)
        dialog_layout.addRow("Quantity:", quantity_input)
        dialog_layout.addRow("Status:", status_input)
        dialog_layout.addRow("Price:", price_input)
        dialog_layout.addRow(add_button)
        
        dialog.setLayout(dialog_layout)
        dialog.exec_()
        
        self.load_orders()
    
    def insert_order(self, dialog, order_id, user_id, product_id, quantity, status, price):
        self.cursor.execute("INSERT INTO orders (order_id, user_id, product_id, quantity, status, total_price) VALUES (%s, %s, %s, %s, %s, %s)", (order_id, user_id, product_id, quantity, status, price))
        self.conn.commit()
        dialog.close()
        self.load_orders()

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AmazonAdminUI()
    window.show()
    sys.exit(app.exec_())
