from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from SqliteHelper import *
from shared import *

class UpdateBook:
    """Updates the book details in the booklist as per user input.
    
    METHODS: 
        __init__(self, window, helper)
            Loads the book_details form with the existing data from the database and sets the title/author fields as read-only
        
        update_book(self)
            Pulls the existing details from the database into the dialog window.
        
        update_details(self)
            Overwrites the existing data for rating, genre, series, and notes and updates the database with this new data.       
    """

    def __init__(self, window, helper):
        """Loads the book_details form with the existing data from the database and sets the title/author fields as read-only
        
        Parameters: 
            window: reference to the main screen created by MainWindow class
            helper: reference to the sqlite object created by SqliteHelper class
        """
        
        super(UpdateBook, self).__init__()
        self.window = window
        self.helper = helper
        self.details_form = uic.loadUi("book_details_form.ui")
        self.details_form.setWindowTitle("MyBookMgr - Update Book Details")
        self.details_form.setWindowFlags(self.details_form.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.palette_title = self.details_form.lineEdit.palette()
        self.palette_title.setColor(QtGui.QPalette.Base, QtGui.QColor('lightgrey'))
        self.details_form.lineEdit.setPalette(self.palette_title)

        self.palette_author = self.details_form.lineEdit_2.palette()
        self.palette_author.setColor(QtGui.QPalette.Base, QtGui.QColor('lightgrey'))
        self.details_form.lineEdit_2.setPalette(self.palette_author)

    def update_book(self): 
        """Called when user clicks the Update Book button on the mainscreen, this method pulls the existing details from the database into the dialog window.
        
        Raises Attribute Error if no book is selected in table when button is clicked
            Please select a book
        """
        self.details_form.buttonBox.rejected.connect(self.details_form.reject)
        self.details_form.buttonBox.accepted.connect(self.update_details)
        
        try:
            self.selected_row = self.window.getRowId()
            self.title = self.window.booklist_db.item(self.selected_row, 1).text()
            self.author = self.window.booklist_db.item(self.selected_row, 2).text()
            self.rating = self.window.booklist_db.item(self.selected_row, 3).text()    
            self.genre = self.window.booklist_db.item(self.selected_row, 4).text()
            self.series = self.window.booklist_db.item(self.selected_row, 5).text()    
            self.notes = self.window.booklist_db.item(self.selected_row, 6).text()
    
            self.details_form.lineEdit.setText(self.title)
            self.details_form.lineEdit.setReadOnly(True)
            self.details_form.lineEdit_2.setText(self.author)
            self.details_form.lineEdit_2.setReadOnly(True)

            self.details_form.spinBox.setValue(int(self.rating))
            self.details_form.lineEdit_3.setText(self.genre)
            self.details_form.lineEdit_4.setText(self.series)
            self.details_form.lineEdit_5.setText(self.notes)
            
            self.early_cancel = self.details_form.exec_()

            if self.early_cancel == QDialog.Rejected:
                self.details_form.close()
        
        except AttributeError:
            show_message("Error", "Please select a book")
            self.window.refresh_data()
            pass

    def update_details(self):
        """Overwrites the existing data for rating, genre, series, and notes and updates the database with this new data.
        This method is called when the user clicks the OK button on the dialog window.

        Raises AttributeError if no changes were made to a section
            pass
        """

        try: 
            self.book_id = self.window.getBookId()
            self.rating = self.details_form.spinBox.text()
            self.genre = remove_punctuation(self.details_form.lineEdit_3.text().title())
            self.series = remove_punctuation(self.details_form.lineEdit_4.text().title())
            self.notes = self.details_form.lineEdit_5.text()

            self.helper.update("UPDATE books SET rating=?, genre=?, series=?, notes=? WHERE id=$book_id", (self.rating, self.genre, self.series, self.notes, self.book_id))
            self.window.refresh_data()
            self.details_form.close()
                    
        except AttributeError: 
            self.window.refresh_data()
            pass
