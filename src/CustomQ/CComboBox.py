import PySide6.QtWidgets as Qw


class CComboBox(Qw.QComboBox):
    """
    Extends the functionality with custom helpers
    And includes a secondary array for data linked to each item
    """
    def __init__(self, parent=None):
        Qw.QComboBox.__init__(self, parent)
        self.linked_data = []


    def clear(self):
        Qw.QComboBox.clear(self)
        self.linked_data.clear()


    def addTextItemLinkedData(self, text: str, data: any):
        self.addItem(text)
        self.linked_data.append(data)


    def setCurrentIndexByLinkedData(self, data: any):
        self.setCurrentIndex(self.linked_data.index(data))


    def indexLinkedData(self, data: any):
        return self.linked_data.index(data)


    def currentLinkedData(self):
        return self.linked_data[self.currentIndex()]
