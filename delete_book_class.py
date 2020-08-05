from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from shared import *

class DeleteBook(QtWidgets.QDialog):
    """Deletes the selected book in the booklist table.
    
    METHODS: 
        __init__(self, window, helper)
            Loads the dialog window to confirm user's request to delete the selected book
        
        confirm_ok(self)
            Attempts to get the selected book id and opens dialog winodw for user to confirm deletion
        
        delete_book(self)
            Called by confirm_ok() when user clicks the OK button, this method sends a SQLite query to delete the book from the database
    """

    def __init__(self, window, helper):
        """Loads the dialog window to confirm user's request to delete the selected book
        
        Parameters: 
            window: reference to the main screen created by MainWindow class
            helper: reference to the sqlite object created by SqliteHelper class
        """
        super(DeleteBook, self).__init__()
        uic.loadUi("dialog_confirm.ui", self)
        self.window = window
        self.helper = helper
        self.confirm = uic.loadUi("dialog_confirm.ui")
    
    def delete_book(self):
        """Sends a SQLite query to delete the book from the database.
        Called by confirm_ok() when user clicks the OK button
        """
        
        self.bookToDelete = self.window.getBookId()
        self.helper.delete("DELETE FROM books WHERE id=" + self.bookToDelete)

    def confirm_ok(self):  
        """Attempts to get the selected book id and opens dialog winodw for user to confirm deletion

            Raises AttributeError if no book is selected
                Please select a book
        """

        try:
            self.confirm.OK_button.clicked.connect(self.delete_book)
            self.confirm.Cancel_button.clicked.connect(self.confirm.close)
            self.bookToDelete = self.window.getBookId()       
            self.confirm.exec_()
            self.window.refresh_data()
        except AttributeError:
            show_message("Error", "Please select a book")
            self.window.refresh_data()
            pass