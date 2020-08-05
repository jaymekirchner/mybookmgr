from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
import string

"""These functions are used by multiple classes in the program so they are together in this file.

FUNCTIONS:
    remove_punctuation(category)
        Removes punctuation from a list of tuples.

    show_message(title = "Error", message = "Please input data")
        Pop-up window with brief message to user when exception is raised

"""

def remove_punctuation(category):
    """Removes punctuation from a list of tuples.

    Accepts a list of tuples and iterates through each character in each item of the tuple to remove punctuation. 
    When the method finds a character that is not punctuation, it saves it into a new string called word.
    
    Parameters:
        category (list of tuples) - accepts a list of tuples to iterate through
    
    Variables: 
        word (string) - created from all characters in iterated tuple that is not punctuation

    Returns string of all characters from the tuple that is not punctuation
    """

    word = ""
    for item in category:
        item = str(item) 
            
        for char in item:
            if char not in string.punctuation:
                word += char
            
    return word

def show_message(title = "Error", message = "Please input data"):
    """Pop-up window with brief message to user when exception is raised.

    Parameters: 
        title (string) - default is "Error"
        message (string) - default is "Please input data"
    """
    QMessageBox.information(None, title, message)
