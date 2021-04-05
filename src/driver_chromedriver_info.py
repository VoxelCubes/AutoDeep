import PySide6.QtWidgets as Qw
from src.ui_generated_files.ui_chromedriverInfo import Ui_ChromedriverInfo



class ChromedriverInfo(Qw.QDialog, Ui_ChromedriverInfo):
    """Info box"""


    def __init__(self):
        Qw.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Error")
