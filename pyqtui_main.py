import sys
import mysql.connector
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, 
                             QFrame, QFormLayout, QDialog, QComboBox)
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
            ("Orders", self.load_orders),
            ("Statistics", self.load_statistics)
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
        table.setColumnCount(6)  # Increased from 4 to 5 columns
        table.setHorizontalHeaderLabels(["Order ID", "User ID", "Product ID", "Quantity", "Price", "Status"])  # Added "Status" column
        
        self.cursor.execute("SELECT order_id, user_id, product_id, quantity, total_price, status FROM orders")  # Fetch status as well
        orders = self.cursor.fetchall()
        table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            for col, value in enumerate(order):
                table.setItem(row, col, QTableWidgetItem(str(value)))
        
        self.content_layout.addWidget(table)

        change_status_button = QPushButton("Change Order Status")
        change_status_button.clicked.connect(self.change_order_status)
        self.content_layout.addWidget(change_status_button)

    def load_statistics(self):
        self.clear_content()

        label = QLabel("Statistics")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.content_layout.addWidget(label)

        # Dropdown and Input for Filtering
        filter_layout = QHBoxLayout()
        
        self.filter_type = QComboBox()
        self.filter_type.addItems(["Orders Above ₹", "Orders Below ₹", "Products Above ₹", "Products Below ₹"])

        self.filter_value = QLineEdit()
        self.filter_value.setPlaceholderText("Enter price")

        filter_button = QPushButton("Apply Filter")
        filter_button.clicked.connect(self.apply_statistics_filter)

        filter_layout.addWidget(self.filter_type)
        filter_layout.addWidget(self.filter_value)
        filter_layout.addWidget(filter_button)

        self.content_layout.addLayout(filter_layout)

        # Dropdown for selecting statistics type
        stats_layout = QHBoxLayout()
        
        self.stats_type = QComboBox()
        self.stats_type.addItems(["Best Selling Product", "Worst Selling Product", "Highest Spending Customer"])
        
        stats_button = QPushButton("Show Statistics")
        stats_button.clicked.connect(self.apply_stats_query)

        stats_layout.addWidget(self.stats_type)
        stats_layout.addWidget(stats_button)

        self.content_layout.addLayout(stats_layout)

        # Revenue Label
        self.revenue_label = QLabel("Total Revenue: ₹0")
        self.revenue_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        self.content_layout.addWidget(self.revenue_label)

        # Dynamic Statistics Display Label
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("font-size: 14px; color: blue;")
        self.content_layout.addWidget(self.stats_label)

        # Load statistics initially
        self.display_statistics()


    def display_statistics(self, filter_query=None, filter_value=None):
        if filter_query:
            self.cursor.execute(filter_query, (filter_value,))
        else:
            self.cursor.execute("SELECT SUM(total_price) FROM orders")

        revenue = self.cursor.fetchone()[0]
        revenue = revenue if revenue else 0  

        self.revenue_label.setText(f"Total Revenue: ₹{revenue}")


    def apply_statistics_filter(self):
        filter_option = self.filter_type.currentText()
        filter_value = self.filter_value.text()

        if not filter_value.isdigit():
            return  # Ignore invalid input

        filter_value = int(filter_value)

        if filter_option == "Orders Above ₹":
            filter_query = "SELECT SUM(total_price) FROM orders WHERE total_price > %s"
        elif filter_option == "Orders Below ₹":
            filter_query = "SELECT SUM(total_price) FROM orders WHERE total_price < %s"
        elif filter_option == "Products Above ₹":
            filter_query = "SELECT SUM(total_price) FROM orders WHERE product_id IN (SELECT product_id FROM products WHERE price > %s)"
        elif filter_option == "Products Below ₹":
            filter_query = "SELECT SUM(total_price) FROM orders WHERE product_id IN (SELECT product_id FROM products WHERE price < %s)"
        else:
            return

        self.display_statistics(filter_query, filter_value)


    def apply_stats_query(self):
        selected_stat = self.stats_type.currentText()

        if selected_stat == "Best Selling Product":
            query = """
                SELECT p.name, SUM(o.quantity) AS total_sold
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                GROUP BY p.product_id
                ORDER BY total_sold DESC
                LIMIT 1
            """
        elif selected_stat == "Worst Selling Product":
            query = """
                SELECT p.name, COALESCE(SUM(o.quantity), 0) AS total_sold
                FROM products p
                LEFT JOIN orders o ON p.product_id = o.product_id
                GROUP BY p.product_id
                ORDER BY total_sold ASC
                LIMIT 1
            """
        elif selected_stat == "Highest Spending Customer":
            query = """
                SELECT u.full_name, SUM(o.total_price) AS total_spent
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                GROUP BY u.user_id
                ORDER BY total_spent DESC
                LIMIT 1
            """
        else:
            return

        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result:
            self.stats_label.setText(f"{selected_stat}: {result[0]} (₹{result[1]})")
        else:
            self.stats_label.setText(f"{selected_stat}: No Data Available")


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

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.insert_order(dialog, order_id_input.text(), user_id_input.text(), product_id_input.text(), quantity_input.text(), status_input.text()))
        
        dialog_layout.addRow("Order ID:", order_id_input)
        dialog_layout.addRow("User ID:", user_id_input)
        dialog_layout.addRow("Product ID:", product_id_input)
        dialog_layout.addRow("Quantity:", quantity_input)
        dialog_layout.addRow("Status:", status_input)
        dialog_layout.addRow(add_button)
        
        dialog.setLayout(dialog_layout)
        dialog.exec_()
        
        self.load_orders()

    
    def insert_order(self, dialog, order_id, user_id, product_id, quantity, status):
        try:
            self.cursor.execute("SELECT price, stock FROM products WHERE product_id = %s", (product_id,))
            result = self.cursor.fetchone()
            
            if result:
                product_price, current_stock = result
                quantity = int(quantity)

                if quantity > current_stock:
                    print("Not enough stock available!")  # You can show a pop-up instead
                    return

                total_price = quantity * float(product_price)

                # Insert the order
                self.cursor.execute(
                    "INSERT INTO orders (order_id, user_id, product_id, quantity, status, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
                    (order_id, user_id, product_id, quantity, status, total_price)
                )

                # Reduce the stock
                new_stock = current_stock - quantity
                self.cursor.execute("UPDATE products SET stock = %s WHERE product_id = %s", (new_stock, product_id))

                self.conn.commit()
                dialog.close()
                self.load_orders()
                self.load_products()  # Refresh product stock display

            else:
                print("Product not found!")
        
        except Exception as e:
            print(f"Error: {e}")


    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def change_order_status(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Change Order Status")
        layout = QFormLayout()

        order_id_input = QLineEdit()
        status_dropdown = QComboBox()
        status_dropdown.addItems(["Pending", "Processing", "Shipped", "Delivered", "Cancelled"])

        layout.addRow("Order ID:", order_id_input)
        layout.addRow("New Status:", status_dropdown)

        submit_btn = QPushButton("Update")
        submit_btn.clicked.connect(lambda: self.update_order_status(dialog, order_id_input.text(), status_dropdown.currentText()))
        layout.addWidget(submit_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def update_order_status(self, dialog, order_id, new_status):
        self.cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
        self.conn.commit()
        dialog.close()
        self.load_orders()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AmazonAdminUI()
    window.show()
    sys.exit(app.exec_())
