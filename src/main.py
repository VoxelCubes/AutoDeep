import os
# QT plugins are copied from the site-packages folder into .\qtplugins\ for the pyinstaller build.
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "qtplugins"

import sys
import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
from PySide6.QtGui import QColor, QPalette
from driver_mainwindow import MainWindow



class DarkPalette(QPalette):
    """A Dark palette meant to be used with the Fusion theme."""
    def __init__(self, *__args):
        super().__init__(*__args)

        self.setColor(QPalette.WindowText, QColor(0xdcddde))  # white
        self.setColor(QPalette.Button, QColor(0x4f545c))          #dark grey (drop down arrow colour and tabs)
        self.setColor(QPalette.Light, QColor(0x42454a))          #med gray (lines around stuff)
        self.setColor(QPalette.Midlight, QColor(53, 0, 0))          #dunno
        self.setColor(QPalette.Dark, QColor(0x202225))          #dunno
        self.setColor(QPalette.Mid, QColor(0x303235))          #dunno
        self.setColor(QPalette.Text, QColor(0xdcddde))         #white dunno
        self.setColor(QPalette.BrightText, QColor(0xAAFFFF))       #red dunno
        self.setColor(QPalette.ButtonText, QColor(0xFFFFFF))   #white
        self.setColor(QPalette.Base, QColor(0x2f3136))            #darker grey (selected text in pop up)
        self.setColor(QPalette.Window, QColor(0x36393f))  # dark grey (normal background widgets and main)
        self.setColor(QPalette.Shadow, QColor(0x202225))  # darker grey
        self.setColor(QPalette.Highlight, QColor(0x7289da))     #blue
        self.setColor(QPalette.HighlightedText, QColor(0xFFFFFF))    #black
        self.setColor(QPalette.Link, QColor(0x00b0d0))          #blue
        self.setColor(QPalette.LinkVisited, QColor(150, 50, 255))   #purple
        self.setColor(QPalette.AlternateBase, QColor(0x393c42))   #dark grey (alternating color in lists)
        self.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))  #white
        self.setColor(QPalette.ToolTipText, QColor(255, 255, 255))  #white
        self.setColor(QPalette.PlaceholderText, QColor(0x72767D))  #light gray

        # If item is disabled, use alternative colours
        self.setColor(QPalette.Disabled, QPalette.Button, QColor(53, 53, 53))       #dark grey
        self.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(25, 25, 25))   #darker grey


if __name__ == "__main__":

    app = Qw.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QToolTip { color: #ffffff; background-color: grey; border: 1px solid white; }
        """)
    app.setPalette(DarkPalette())
    app.setFont(Qg.QFont("segoe", 11))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
