from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from shared import remove_punctuation, show_message


class AddBook(QtWidgets.QDialog):
    """Adds the new book in the booklist table.
    
    METHODS: 
        __init__(self, window, helper)
            Loads the dialog window so the user can type in the details of the new book to add to the database table.
             
        open_add_form(self)
            Opens a blank dialog form so they user can input book details and then runs a check for duplicate entries
        
        reset_form(self)
            Clears the dialog window form by changing all text categories (title, author, genre, series, notes) to empty strings and the integer category (rating) to 0
    """

    def __init__(self, window, helper):
        """Loads the dialog window so the user can type in the details of the new book to add to the database table.

        Parameters: 
            window: reference to the main screen created by MainWindow class
            helper: reference to the sqlite object created by SqliteHelper class
        """
        super(AddBook, self).__init__()
        uic.loadUi("book_details_form.ui", self) 
        self.window = window
        self.helper = helper

    def open_add_form(self):
        """Opens a blank dialog form so they user can input book details and then runs a check for duplicate entries
        """
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        self.setWindowTitle("MyBookMgr - Add Book Details")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.reset_form() 
        self.early_cancel = self.exec_() 

        self.title = remove_punctuation(self.lineEdit.text()).title()
        self.author = remove_punctuation(self.lineEdit_2.text()).title()
        self.rating = self.spinBox.text()
        self.genre = remove_punctuation(self.lineEdit_3.text().title())
        self.series = remove_punctuation(self.lineEdit_4.text().title())
        self.notes = self.lineEdit_5.text()

        if self.early_cancel == QDialog.Rejected:
            self.close()

        elif self.title.strip(" ") != "" and self.author.strip(" ") != "":
            self.book = (self.title, self.author, int(self.rating), self.genre, self.series, self.notes)

            self.toCheck = (self.title, self.author)
            self.dupe_id = self.helper.sort_items("SELECT id FROM books WHERE title=$title AND author=$author", self.toCheck)

            if len(self.dupe_id) == 0: #new entry is not a duplicate
                self.helper.insert("INSERT INTO books (title, author, rating, genre, series, notes) VALUES (?, ?, ?, ?, ?, ?)", self.book)
                self.window.refresh_data()

            else: #duplicate exists 
                self.simple_dupes_dialog = uic.loadUi("simple_duplicates_dialog.ui")
                self.simple_dupes_dialog.OK_Button.clicked.connect(self.simple_dupes_dialog.close)
                self.simple_dupes_dialog.exec_()

        else: 
            show_message("Error", "Enter valid book details")   
            pass       

    def reset_form(self):
        """Clears the dialog window form by setting all text edits to empty strings and the spinbox to 0.
        """

        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.spinBox.setValue(0)
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")