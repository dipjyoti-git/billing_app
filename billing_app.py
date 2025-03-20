from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGroupBox
from PySide6.QtGui import QFont
import mysql.connector
import sys


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin@123",
        database="billing_app"
    )


class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Billing App")
        self.resize(500, 500)  # Window size
        self.setStyleSheet("background-color: #f0f0f0; color: black;")  # Background color and text color


        title = QLabel("Billing Management System")
        title.setFont(QFont('Arial', 16))
        title.setStyleSheet("color: black; padding: 10px;")


        input_group = QGroupBox("Customer Details")
        input_group.setStyleSheet("color: black;")
        input_layout = QVBoxLayout()


        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Customer Name")
        self.name_input.setStyleSheet("padding: 5px; border: 1px solid #aaa; color: black;")


        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact Info")
        self.contact_input.setStyleSheet("padding: 5px; border: 1px solid #aaa; color: black;")


        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Bill Amount")
        self.amount_input.setStyleSheet("padding: 5px; border: 1px solid #aaa; color: black;")

        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.contact_input)
        input_layout.addWidget(self.amount_input)
        input_group.setLayout(input_layout)


        button_layout = QHBoxLayout()


        self.submit_btn = QPushButton("Add Bill")
        self.submit_btn.setStyleSheet("""
            background-color: #28a745; 
            color: black; 
            padding: 8px; 
            border-radius: 5px;
            font-weight: bold;
        """)
        self.submit_btn.clicked.connect(self.add_bill)


        self.show_btn = QPushButton("Show All Bills")
        self.show_btn.setStyleSheet("""
            background-color: #007bff; 
            color: black; 
            padding: 8px; 
            border-radius: 5px;
            font-weight: bold;
        """)
        self.show_btn.clicked.connect(self.show_bills)

        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.show_btn)


        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: white; padding: 10px; color: black;")


        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(input_group)
        layout.addLayout(button_layout)


        bill_label = QLabel("Bill Records:")
        bill_label.setStyleSheet("color: black;")
        layout.addWidget(bill_label)

        layout.addWidget(self.output)
        self.setLayout(layout)


    def add_bill(self):
        name = self.name_input.text()
        contact = self.contact_input.text()
        amount = self.amount_input.text()

        if name and contact and amount:
            db = connect_db()
            cursor = db.cursor()


            cursor.execute("INSERT INTO customers (name, contact) VALUES (%s, %s)", (name, contact))
            customer_id = cursor.lastrowid


            cursor.execute("INSERT INTO bills (customer_id, amount) VALUES (%s, %s)", (customer_id, amount))

            db.commit()
            db.close()

            self.output.setText("Bill added successfully!\n")


            self.name_input.clear()
            self.contact_input.clear()
            self.amount_input.clear()
        else:
            self.output.setText("Please fill all fields!")


    def show_bills(self):
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT customers.name, customers.contact, bills.amount, bills.date
            FROM bills
            JOIN customers ON bills.customer_id = customers.id
        """)

        data = cursor.fetchall()
        db.close()

        if data:
            text = ""
            for row in data:
                text += f"Name: {row[0]} | Contact: {row[1]} | Amount: {row[2]} | Date: {row[3]}\n"
            self.output.setText(text)
        else:
            self.output.setText("No records found.")


app = QApplication(sys.argv)
window = BillingApp()
window.show()
sys.exit(app.exec())
