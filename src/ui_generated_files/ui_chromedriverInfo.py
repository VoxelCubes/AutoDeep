# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chromedriverInfo.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_ChromedriverInfo(object):
    def setupUi(self, ChromedriverInfo):
        if not ChromedriverInfo.objectName():
            ChromedriverInfo.setObjectName(u"ChromedriverInfo")
        ChromedriverInfo.resize(400, 196)
        self.verticalLayout = QVBoxLayout(ChromedriverInfo)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(ChromedriverInfo)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label = QLabel(ChromedriverInfo)
        self.label.setObjectName(u"label")
        self.label.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.label)

        self.buttonBox = QDialogButtonBox(ChromedriverInfo)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ChromedriverInfo)
        self.buttonBox.accepted.connect(ChromedriverInfo.accept)
        self.buttonBox.rejected.connect(ChromedriverInfo.reject)

        QMetaObject.connectSlotsByName(ChromedriverInfo)
    # setupUi

    def retranslateUi(self, ChromedriverInfo):
        ChromedriverInfo.setWindowTitle(QCoreApplication.translate("ChromedriverInfo", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("ChromedriverInfo", u"Please ensure a chromedriver.exe file is present in this program's folder. If it is missing or outdated, download the latest version below. Chrome or Chromium must also be installed.", None))
        self.label.setText(QCoreApplication.translate("ChromedriverInfo", u"<html><head/><body><p><a href=\"https://chromedriver.chromium.org/\"><span style=\" text-decoration: underline; color:#aaffff;\">https://chromedriver.chromium.org/</span></a></p></body></html>", None))
    # retranslateUi

