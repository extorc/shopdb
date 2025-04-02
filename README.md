# E-Commerce Database System

## Project Overview
The E-Commerce Management System is a database-driven application designed for the Manager/Admin’s POV to enable smooth management of an online shopping platform.
The system enables users to browse products, place orders, manage inventory, and handle customer transactions efficiently.
The project implements various database operations, including CRUD (Create, Read, Update, Delete) functionalities, ensuring data integrity and consistency.
Note that this project is an application designed for the Manager/Admin’s POV to enable a smooth management of an online retail platform.


## Methodology
The sidebar provides navigation between different sections such as Users, Products, Orders, and Statistics.
Each section loads data dynamically from the MySQL database and presents it using QTableWidget.
Users can add new records via pop-up dialogs using QDialog and submit the data to the database.
The Statistics section allows filtering order data and computing key metrics such as revenue, best-selling products, and highest-spending customers.
The UI elements are styled using built-in PyQt5 methods to ensure consistency and readability.

## Technologies Used
- **Database**: MySQL 
- **Backend**: SQL 
- **Frontend**: Python, PyQt5 for the GUI
- **Interface**: mysql.connector()


## UI Overview
1. 
  ![UI Overview]([https://example.com/image.png](https://github.com/rohanshenoy30/shopdb/blob/main/images/WhatsApp%20Image%202025-04-01%20at%2016.34.46.jpeg))


2. Set up the database:
   ```sql
   CREATE DATABASE ecommerce_db;
   ```
3. Import the schema:
   ```bash
   mysql -u root -p ecommerce_db < schema.sql
   ```
4. (Optional) Set up a backend connection if integrating with a web app.

## Usage
- Run SQL queries for inserting, updating, and retrieving data.
- Execute SQL scripts to generate sales reports and analyze trends.
- (Optional) Access the frontend interface to interact with the database visually.

## Conclusion
Our E-Commerce Management System project effectively demonstrates the use of database systems in handling online business operations. 
The system ensures seamless order processing, product management, and admin control, making it a scalable solution for real-world e-commerce applications
Future improvements may include payment gateway integration, user analytics, and enhanced security measures.

- Implement an API to connect the database with a web application.
- Add AI-driven analytics for customer behavior prediction.
- Implement advanced security measures for payment transactions.

## Contributors
- **Rohan Shenoy**
- **Shaurya Mittal**

## License
This project is open-source and available under the MIT License.
