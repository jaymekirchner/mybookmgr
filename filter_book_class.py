from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from SqliteHelper import *
from shared import *


class FilterBook:
    """Filters the booklist data based on user's selection in filter wizard.
    
    METHODS: 
        __init__(self, helper)
            Loads and opens the filter wizard, and loads the filter_results window

        filter_book_by_category(self)
            Opens filter wizard and connects to respective import method based on user's chosen filter category

        import_rating(self) 
            Runs a sqlite query to select all values for rating from the books database
        
        import_author(self) 
            Runs a sqlite query to select all values for author from the books database
        
        import_genre(self)
            Runs a sqlite query to select all values for genre from the books database
        
        import_series(self)
            Runs a sqlite query to select all values for series from the books database
        
        get_options(self, category)
            Creates a new set with the unique values from the database for the user's chosen filter category
        
        get_combobox_values(self, new_set)
            Fills the filter wizard's drop-down menu with the unique values for the user's chosen filter category

        build_table(self)
            Builds a new filter table based on the user's chosen category and value in the filter wizard
        
        load_filter_data(self)
            Loads the results table from the database into the the filter table that is shown in a new window

        clear_filter_data(self)
            Systematically removes existing data from the filter results table by iterating through each row and clearing its data
        
        filter_refresh(self)
            Clears the filter data and then loads the data again so any modifications will be shown
    """

    def __init__(self, helper):
        """Loads and opens the filter wizard, and loads the filter_results window. 

        Parameters: 
            helper: reference to the sqlite object created by SqliteHelper class
        """

        super(FilterBook, self).__init__()
        self.filter_wizard = uic.loadUi("filter_wizard.ui") 
        self.helper = helper
        self.filter_results = uic.loadUi("filter_results.ui")
        self.filter_results.filter_results_table.hideColumn(0)
        self.filter_wizard.setWindowFlags(self.filter_wizard.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    
    def filter_book_by_category(self):
        """Opens filter wizard and connects to respective import method based on user's chosen filter category."""

        self.filter_wizard.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.build_table)
        self.filter_wizard.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.filter_wizard.restart)

        self.filter_wizard.RadioBtn_rating.clicked.connect(self.import_rating)
        self.filter_wizard.RadioBtn_author.clicked.connect(self.import_author)
        self.filter_wizard.RadioBtn_genre.clicked.connect(self.import_genre) 
        self.filter_wizard.RadioBtn_series.clicked.connect(self.import_series)

        self.filter_wizard.exec_()
        
    def import_rating(self): 
        """Runs a sqlite query to select all values for rating from the books database.
        Calls get_options() method to remove duplicate values
        Calls get_combobox_values() method to fill drop-down menu with unique values for user to select
        """

        self.category = self.helper.select("SELECT rating FROM books") 
        self.category_set = self.get_options(self.category)
        self.get_combobox_values(self.category_set)

    def import_author(self): 
        """Runs a sqlite query to select all values for author from the books database.
        Calls get_options() method to remove duplicate values
        Calls get_combobox_values() method to fill drop-down menu with unique values for user to select
        """

        self.category = self.helper.select("SELECT author FROM books") 
        self.category_set = self.get_options(self.category)
        self.get_combobox_values(self.category_set)

    def import_genre(self): 
        """Runs a sqlite query to select all values for genre from the books database.
        Calls get_options() method to remove duplicate values
        Calls get_combobox_values() method to fill drop-down menu with unique values for user to select
        """

        self.category = self.helper.select("SELECT genre FROM books") 
        self.category_set = self.get_options(self.category)
        self.get_combobox_values(self.category_set)

    def import_series(self): 
        """Runs a sqlite query to select all values for series from the books database.
        Calls get_options() method to remove duplicate values
        Calls get_combobox_values() method to fill drop-down menu with unique values for user to select
        """

        self.category = self.helper.select("SELECT series FROM books") 
        self.category_set = self.get_options(self.category)
        self.get_combobox_values(self.category_set)
        
    def get_options(self, category):
        """Called by the import methods to create a new set with the unique values from the database for the user's chosen filter category.
        Punctuation is removed before the value is added to the set.

        Returns
            set of unique values for user's chosen category
        """

        self.options = set() 
        
        for item in category:
            item = str(remove_punctuation(item)) 
            self.options.add(item)

        return self.options

    def get_combobox_values(self, new_set):
        """Called by the import methods to fill the filter wizard's drop-down menu with the unique values for the user's chosen filter category 
        """
        self.filter_wizard.comboBox.clear()
    
        for name in new_set:
            self.filter_wizard.comboBox.addItem(name)
            
    def build_table(self):
        """Builds a new filter table based on the user's chosen category and value in the filter wizard.
        """

        self.filter_results.close_Button.clicked.connect(self.filter_results.close)
        
        self.helper.create_filter_table()

        self.data = self.filter_wizard.comboBox.currentText()

        if self.filter_wizard.RadioBtn_author.isChecked():
            self.helper.filter_items("author", self.data) 
            self.filter_wizard.RadioBtn_author.setChecked(False)

        elif self.filter_wizard.RadioBtn_rating.isChecked():
            self.helper.filter_items("rating", self.data) 
            self.filter_wizard.RadioBtn_rating.setChecked(False)

        elif self.filter_wizard.RadioBtn_genre.isChecked():
            self.helper.filter_items("genre", self.data) 
            self.filter_wizard.RadioBtn_genre.setChecked(False)

        elif self.filter_wizard.RadioBtn_series.isChecked():
            self.helper.filter_items("series", self.data) 
            self.filter_wizard.RadioBtn_series.setChecked(False)

        self.filter_refresh()
        self.filter_results.show()

    def load_filter_data(self):   
        """Loads the results table from the database into the the filter table that is shown in a new window.
        """
        self.helper.create_filter_table() 

        filtered_table = self.helper.select("SELECT * FROM results ORDER BY id")    
        
        for row_num, book in enumerate(filtered_table):
            self.filter_results.filter_results_table.insertRow(row_num)
            for col_num, data in enumerate(book):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.filter_results.filter_results_table.setItem(row_num, col_num, cell)
        
        self.helper.delete("DROP TABLE results") #TESTED WITH DB BROWSER (SQLITE) PROGRAM

    def clear_filter_data(self):
        """Systematically removes existing data from the filter results table by iterating through each row and clearing its data.
        """

        self.filter_results.filter_results_table.clearSelection()
        
        while (self.filter_results.filter_results_table.rowCount() > 0):
            self.filter_results.filter_results_table.removeRow(0)
            self.filter_results.filter_results_table.clearSelection()
        
    def filter_refresh(self):
        """Clears the filter data and then loads the data again so any modifications will be shown"""
        self.clear_filter_data()
        self.load_filter_data() 
