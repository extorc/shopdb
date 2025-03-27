import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, 
                             QScrollArea, QFrame, QGridLayout, QComboBox)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize

class AmazonAdminUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Amazon Admin Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Main Content Area
        content_area = self.create_content_area()
        main_layout.addWidget(content_area)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Apply Amazon-like styling
        self.setStyleSheet("""
            QMainWindow { background-color: #F3F3F3; }
            QWidget { font-family: Arial, sans-serif; }
            QPushButton { 
                background-color: #F0C14B; 
                border: 1px solid #A88734; 
                border-radius: 3px; 
                padding: 5px 10px; 
            }
            QPushButton:hover { 
                background-color: #F4D278; 
            }
            QLineEdit { 
                border: 1px solid #A6A6A6; 
                border-radius: 3px; 
                padding: 5px; 
            }
            QTableWidget { 
                background-color: white; 
                alternate-background-color: #F7F7F7; 
            }
        """)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #232F3E; color: white;")
        
        sidebar_layout = QVBoxLayout()
        
        # Amazon logo
        logo = QLabel("Amazon")
        logo.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 15px;")
        sidebar_layout.addWidget(logo)
        
        # Sidebar menu items
        menu_items = [
            "Dashboard", 
            "Product Management", 
            "Order Management", 
            "Customer Management", 
            "Analytics", 
            "Settings"
        ]
        
        for item in menu_items:
            menu_button = QPushButton(item)
            menu_button.setStyleSheet("""
                QPushButton { 
                    text-align: left; 
                    padding: 10px; 
                    color: white; 
                    background-color: transparent; 
                    border: none; 
                }
                QPushButton:hover { 
                    background-color: #3A4E68; 
                }
            """)
            sidebar_layout.addWidget(menu_button)
        
        sidebar_layout.addStretch(1)
        sidebar.setLayout(sidebar_layout)
        
        return sidebar

    def create_content_area(self):
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search products, orders...")
        search_input.setFixedHeight(40)
        
        notification_btn = QPushButton("🔔")
        profile_btn = QPushButton("👤")
        
        header_layout.addWidget(search_input)
        header_layout.addWidget(notification_btn)
        header_layout.addWidget(profile_btn)
        header.setLayout(header_layout)
        
        content_layout.addWidget(header)
        
        # Dashboard Stats
        stats_layout = QHBoxLayout()
        stats_widgets = [
            ("Total Products", "1,254"),
            ("Total Orders", "3,672"),
            ("Revenue", "$542,890"),
            ("Pending Orders", "45")
        ]
        
        for title, value in stats_widgets:
            stat_widget = QFrame()
            stat_layout = QVBoxLayout()
            
            stat_title = QLabel(title)
            stat_value = QLabel(value)
            stat_value.setStyleSheet("font-size: 24px; font-weight: bold;")
            
            stat_layout.addWidget(stat_title)
            stat_layout.addWidget(stat_value)
            stat_widget.setLayout(stat_layout)
            stat_widget.setStyleSheet("""
                QFrame { 
                    background-color: white; 
                    border: 1px solid #E0E0E0; 
                    border-radius: 5px; 
                    padding: 15px; 
                }
            """)
            
            stats_layout.addWidget(stat_widget)
        
        stats_widget = QWidget()
        stats_widget.setLayout(stats_layout)
        content_layout.addWidget(stats_widget)
        
        # Recent Products and Orders
        recent_section = QHBoxLayout()
        
        # Recent Products
        recent_products = QFrame()
        recent_products_layout = QVBoxLayout()
        recent_products_label = QLabel("Recent Products")
        recent_products_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        products_table = QTableWidget(5, 4)
        products_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock"])
        products_table.setStyleSheet("alternate-background-color: #F7F7F7;")
        
        sample_products = [
            ["1", "Wireless Headphones", "$99.99", "250"],
            ["2", "Smart Watch", "$199.99", "100"],
            ["3", "Bluetooth Speaker", "$79.99", "300"],
            ["4", "Laptop Stand", "$49.99", "150"],
            ["5", "Portable Charger", "$29.99", "400"]
        ]
        
        for row, product in enumerate(sample_products):
            for col, value in enumerate(product):
                products_table.setItem(row, col, QTableWidgetItem(value))
        
        recent_products_layout.addWidget(recent_products_label)
        recent_products_layout.addWidget(products_table)
        recent_products.setLayout(recent_products_layout)
        
        # Recent Orders
        recent_orders = QFrame()
        recent_orders_layout = QVBoxLayout()
        recent_orders_label = QLabel("Recent Orders")
        recent_orders_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        orders_table = QTableWidget(5, 4)
        orders_table.setHorizontalHeaderLabels(["Order ID", "Customer", "Total", "Status"])
        orders_table.setStyleSheet("alternate-background-color: #F7F7F7;")
        
        sample_orders = [
            ["A101", "John Doe", "$299.99", "Shipped"],
            ["A102", "Jane Smith", "$149.99", "Processing"],
            ["A103", "Mike Johnson", "$79.99", "Delivered"],
            ["A104", "Sarah Brown", "$199.99", "Shipped"],
            ["A105", "Tom Wilson", "$49.99", "Pending"]
        ]
        
        for row, order in enumerate(sample_orders):
            for col, value in enumerate(order):
                orders_table.setItem(row, col, QTableWidgetItem(value))
        
        recent_orders_layout.addWidget(recent_orders_label)
        recent_orders_layout.addWidget(orders_table)
        recent_orders.setLayout(recent_orders_layout)
        
        recent_section.addWidget(recent_products)
        recent_section.addWidget(recent_orders)
        
        recent_widget = QWidget()
        recent_widget.setLayout(recent_section)
        content_layout.addWidget(recent_widget)
        
        content_widget.setLayout(content_layout)
        return content_widget

def main():
    app = QApplication(sys.argv)
    window = AmazonAdminUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()