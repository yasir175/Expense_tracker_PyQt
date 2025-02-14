
from PyQt5.QtWidgets import QHeaderView,QTableWidgetItem,QMessageBox, QApplication ,QWidget,QLabel,QPushButton,QLineEdit,QComboBox,QDateEdit,QTableWidget,QVBoxLayout,QHBoxLayout
from PyQt5.QtSql import QSqlQuery,QSqlDatabase
from PyQt5.QtCore import QDate,Qt
import sys



class Expense_tracker(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(550,500)
        self.setWindowTitle("Expense_tracker")

        self.date=QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.dropbox=QComboBox()
        self.amount=QLineEdit()
        self.description=QLineEdit()

        self.add_button=QPushButton("Add expense")
        self.delete_button=QPushButton("Delete expense")
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)




        self.table=QTableWidget()
        self.table.setColumnCount(5)
        header_list=["ID","DATE","CATAGORY","AMOUNT","DESCRIPTION"]
        self.table.setHorizontalHeaderLabels(header_list)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(1,Qt.DescendingOrder)






        self.dropbox.addItems(["FOOD","TRANSPORT","RENT","BILL","SHOPPING","MEDICAL","OTHERS"])

        self.master_layout=QVBoxLayout()
        self.row1=QHBoxLayout()
        self.row2=QHBoxLayout()
        self.row3=QHBoxLayout()

        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date)
        self.row1.addWidget(QLabel("Catagory:"))
        self.row1.addWidget(self.dropbox)

        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addWidget(self.table)
        self.setLayout(self.master_layout)
        self.load_table()

    def load_table(self):
        self.table.setRowCount(0)

        query=QSqlQuery("SELECT * FROM expenses")
        row=0
        while query.next():
            expense_id=query.value(0)
            date=query.value(1)
            catagory=query.value(2)
            amount=query.value(3)
            description=query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(str(expense_id))),
            self.table.setItem(row,1,QTableWidgetItem(date)),
            self.table.setItem(row,2,QTableWidgetItem(catagory)),
            self.table.setItem(row,3,QTableWidgetItem(str(amount))),
            self.table.setItem(row,4,QTableWidgetItem(description)),

            row+=1

    def add_expense(self):
        date=self.date.date().toString("yyyy-MM-dd")
        catagory=self.dropbox.currentText()
        amount=self.amount.text()
        description=self.description.text()

        query=QSqlQuery()
        query.prepare("""
                        INSERT INTO expenses (date,catagory,amount,description)
                        VALUES (?,?,?,?)
                      """)

        query.addBindValue(date)
        query.addBindValue(catagory)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        self.date.setDate(QDate.currentDate())
        self.dropbox.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()
        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row ==-1:
            QMessageBox.warning(self,"nothing to select","choose again")
            return

        expense_id = int(self.table.item(selected_row,0).text())

        confirm_delete=QMessageBox.question(self,"Are you sure?",None,QMessageBox.Yes |QMessageBox.No)

        if confirm_delete==QMessageBox.No:
            return

        query=QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()

        self.load_table()


database=QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None,"Error","could not open database")
    sys.exit(1)

query=QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                catagory TEXT,
                amount REAL,
                description TEXT
            )
            """)





if __name__ in "__main__":
    app=QApplication([])
    main=Expense_tracker()
    main.show()
    app.exec_()
