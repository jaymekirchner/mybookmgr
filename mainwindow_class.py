from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from SqliteHelper import *
import string, time
from datetime import datetime
from add_book_class import AddBook
from delete_book_class import DeleteBook
from update_book_class import UpdateBook
from filter_book_class import FilterBook
from shared import *

helper = SqliteHelper("booklist.db")

class MainWindow(QtWidgets.QMainWindow):
    """
    This is the class that sets up the main window which appears at initial program load.

    BUTTONS FOR USER INTERACTION:
        Booklist Table on left of screen:
            Add Book
                Activates AddBook class when clicked
            Update Book
                Activates UpdateBook class when clicked
            Delete Book
                Activates DeleteBook class when clicked
            Filter Booklist
                Activates FilterBook class when clicked
        
        Reminders Table on right of screen:
            Add Reminder 
                Clicking on this button calls the add_event() method
            Delete Reminder
                Clicking on this button calls the delete_event() method

    FUNCTIONS:
        __init__(self) 
            Sets up the main window, buttons, and imports the database details and relevant UI files for initial program load
        
        getRowId(self)
            Returns the current row of the booklist
        
        getBookId(self)
            Returns the text for book item's ID number at index 0 in the current row
        
        load_calendar(self)
            Loads the calendar table from the database and enables the Delete Reminder button 
            if there is at least 1 entry in the table. The Add Reminder Button is automatically enabled.
        
        load_data(self)
            Loads the books table from the database for the booklist table on the main screen. After loading data for the main booklist, it calls load_calendar().
        
        clear_data(self)
            Systematically removes existing data from the booklist table and the reminders table on the main screen by iterating through each table and clearing the selection for each table row.
        
        refresh_data(self)
            Calls the clear_data() method followed by the load_data() method to refresh the screen for the user each time a book or reminder is added or modified.
        
        add_event(self)
            Called when the user clicks on the Add Reminder button. 
            Opens a dialog box for the user to input title, author, and release date for an upcoming book. 
            Details from the dialog box are added into the reminders table.
        
        delete_event(self)
            Called when the user clicks on the Delte Reminder button. 
            
            Raises AttributeError if no book is selected before clicking the Delete Reminder button
                Please select a book.
    """

    def __init__(self):
        """Sets up the main window, buttons, and imports the database details and relevant UI files for initial program load
        """

        super(MainWindow, self).__init__()

        uic.loadUi("mainscreen_calendar.ui", self)
        self.reminder = uic.loadUi("set_reminder.ui")
        self.reminder.setWindowFlags(self.reminder.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.booklist_db.hideColumn(0)
        self.reminders_table.hideColumn(0)

        self.add_details = AddBook(self, helper)
        self.delete_book = DeleteBook(self, helper)
        self.update_details = UpdateBook(self, helper)
        self.filter_books = FilterBook(helper)

        self.Close_Button.clicked.connect(self.close)
        self.addButton.clicked.connect(self.add_details.open_add_form)  
        self.deleteButton.clicked.connect(self.delete_book.confirm_ok)
        self.updateButton.clicked.connect(self.update_details.update_book)
        self.filterButton.clicked.connect(self.filter_books.filter_book_by_category)
        self.btn_addReminder.clicked.connect(self.add_event)
        self.btn_deleteReminder.clicked.connect(self.delete_event)

        self.load_data()
        self.show()

    def getRowId(self):
        """Returns the current row of the booklist"""
        
        return self.booklist_db.currentRow()

    def getBookId(self): 
        """Returns the text for book item's ID number at index 0 in the current row"""
        
        return self.booklist_db.item(self.getRowId(), 0).text()

    def load_calendar(self):
        """Loads the calendar table from the database and enables the Delete Reminder button 
        if there is at least 1 entry in the table. The Add Reminder Button is automatically enabled.
        """

        helper.create_calendar_table()

        calendar_reminder = helper.select("SELECT * FROM calendar ORDER BY date ASC")

        for row_num, event in enumerate(calendar_reminder):
            self.reminders_table.insertRow(row_num)
            for col_num, data in enumerate(event):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.reminders_table.setItem(row_num, col_num, cell)
        
        if len(calendar_reminder) == 0:
            self.btn_deleteReminder.setEnabled(False)
        else:
            self.btn_deleteReminder.setEnabled(True)     

        self.reminder_header = self.reminders_table.horizontalHeader()       
        self.reminder_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.reminder_header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents) 
        self.reminder_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents) 
        self.reminder_header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch) 
    
    def load_data(self):
        """Loads the books table from the database for the booklist table on the main screen. 
        After loading data for the main booklist, it calls load_calendar().
        """
        
        helper.create_table()
        
        table_of_books = helper.select("SELECT * FROM books ORDER BY id") #refers to "books" table in db 

        if len(table_of_books) == 0:
            self.deleteButton.setEnabled(False)
            self.updateButton.setEnabled(False)
            self.filterButton.setEnabled(False)
        else:
            self.deleteButton.setEnabled(True)
            self.updateButton.setEnabled(True)
            self.filterButton.setEnabled(True)
        
        for row_num, book in enumerate(table_of_books):
            self.booklist_db.insertRow(row_num)
            for col_num, data in enumerate(book):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.booklist_db.setItem(row_num, col_num, cell)
        
        self.load_calendar()

    def clear_data(self):
        """Systematically removes existing data from the booklist table and the reminders table on the main screen by iterating through each table and clearing the selection for each table row.
        """
        
        self.booklist_db.clearSelection()
        while (self.booklist_db.rowCount() > 0):
            self.booklist_db.removeRow(0) 
            self.booklist_db.clearSelection()
        
        self.reminders_table.clearSelection()
        while (self.reminders_table.rowCount() > 0):
            self.reminders_table.removeRow(0) 
            self.reminders_table.clearSelection()

    def refresh_data(self):
        """Calls the clear_data() method followed by the load_data() method to refresh the screen for the user each time a book or reminder is added or modified."""
        self.clear_data()
        self.load_data()

    def add_event(self):
        """Called when the user clicks on the Add Reminder button. 
            Opens a dialog box for the user to input title, author, and release date for an upcoming book. 
            Details from the dialog box are added into the reminders table.
        """

        self.reminder.buttonBox_reminder.rejected.connect(self.reminder.reject)
        self.reminder.buttonBox_reminder.accepted.connect(self.reminder.accept)

        self.reminder.lineEdit.setText("")
        self.reminder.lineEdit_2.setText("")
        self.reminder.dateEdit.date().toString('yyyy-mm-dd')

        early_cancel = self.reminder.exec_() 

        title = remove_punctuation(self.reminder.lineEdit.text()).title()
        author = remove_punctuation(self.reminder.lineEdit_2.text()).title()
        date = self.reminder.dateEdit.date().toString('yyyy-MM-dd')
        
        if early_cancel == QDialog.Rejected:
            self.reminder.close()

        elif title.strip(" ") != "" and author.strip(" ") != "":
                event = (title, author, date)
                helper.insert("INSERT INTO calendar (title, author, date) VALUES (?, ?, ?)", event)
                self.refresh_data()
        
        else: 
            show_message("Error", "Enter valid details.")
 
    def delete_event(self):
        """Called when the user clicks on the Delte Reminder button. 
            
            Raises AttributeError if no book is selected before clicking the Delete Reminder button
                Please select a book.
        """
        try:
            event_id = self.reminders_table.item(self.reminders_table.currentRow(), 0).text()
            helper.delete("DELETE FROM calendar WHERE id="+event_id)
            self.refresh_data()
        
        except AttributeError:
            show_message("Error", "Please select a book")
            self.refresh_data()
            pass