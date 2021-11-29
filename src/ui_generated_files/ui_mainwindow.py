# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from src.CustomQ.CTableWidget import CTableWidget
from src.CustomQ.CComboBox import CComboBox

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 550)
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_config = QHBoxLayout()
        self.horizontalLayout_config.setObjectName(u"horizontalLayout_config")
        self.groupBox_cfg_lang = QGroupBox(self.centralwidget)
        self.groupBox_cfg_lang.setObjectName(u"groupBox_cfg_lang")
        self.verticalLayout = QVBoxLayout(self.groupBox_cfg_lang)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox_cfg_lang)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.comboBox = CComboBox(self.groupBox_cfg_lang)
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.checkBox_use_glossary = QCheckBox(self.groupBox_cfg_lang)
        self.checkBox_use_glossary.setObjectName(u"checkBox_use_glossary")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.checkBox_use_glossary)

        self.pushButton_get_glossary = QPushButton(self.groupBox_cfg_lang)
        self.pushButton_get_glossary.setObjectName(u"pushButton_get_glossary")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pushButton_get_glossary)


        self.verticalLayout.addLayout(self.formLayout)

        self.label_glossary = QLabel(self.groupBox_cfg_lang)
        self.label_glossary.setObjectName(u"label_glossary")
        font1 = QFont()
        font1.setPointSize(11)
        font1.setItalic(True)
        self.label_glossary.setFont(font1)
        self.label_glossary.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_glossary)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.horizontalLayout_config.addWidget(self.groupBox_cfg_lang)

        self.groupBox_cfg_time = QGroupBox(self.centralwidget)
        self.groupBox_cfg_time.setObjectName(u"groupBox_cfg_time")
        self.formLayout_2 = QFormLayout(self.groupBox_cfg_time)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(-1, -1, 6, -1)
        self.label_5 = QLabel(self.groupBox_cfg_time)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.doubleSpinBox_min_wait = QDoubleSpinBox(self.groupBox_cfg_time)
        self.doubleSpinBox_min_wait.setObjectName(u"doubleSpinBox_min_wait")
        self.doubleSpinBox_min_wait.setMinimum(7.000000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_min_wait)

        self.pushButton_reset_min_wait = QPushButton(self.groupBox_cfg_time)
        self.pushButton_reset_min_wait.setObjectName(u"pushButton_reset_min_wait")
        icon = QIcon()
        icon.addFile(u":/general/arrow-circle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_reset_min_wait.setIcon(icon)
        self.pushButton_reset_min_wait.setFlat(True)

        self.horizontalLayout_6.addWidget(self.pushButton_reset_min_wait)

        self.horizontalLayout_6.setStretch(0, 1)

        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.label_6 = QLabel(self.groupBox_cfg_time)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.doubleSpinBox_char_wait = QDoubleSpinBox(self.groupBox_cfg_time)
        self.doubleSpinBox_char_wait.setObjectName(u"doubleSpinBox_char_wait")

        self.horizontalLayout_5.addWidget(self.doubleSpinBox_char_wait)

        self.pushButton_reset_char_wait = QPushButton(self.groupBox_cfg_time)
        self.pushButton_reset_char_wait.setObjectName(u"pushButton_reset_char_wait")
        self.pushButton_reset_char_wait.setIcon(icon)
        self.pushButton_reset_char_wait.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_reset_char_wait)

        self.horizontalLayout_5.setStretch(0, 1)

        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.label_7 = QLabel(self.groupBox_cfg_time)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.doubleSpinBox_batch_time = QDoubleSpinBox(self.groupBox_cfg_time)
        self.doubleSpinBox_batch_time.setObjectName(u"doubleSpinBox_batch_time")

        self.horizontalLayout_4.addWidget(self.doubleSpinBox_batch_time)

        self.pushButton_reset_batch_time = QPushButton(self.groupBox_cfg_time)
        self.pushButton_reset_batch_time.setObjectName(u"pushButton_reset_batch_time")
        self.pushButton_reset_batch_time.setIcon(icon)
        self.pushButton_reset_batch_time.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_reset_batch_time)

        self.horizontalLayout_4.setStretch(0, 1)

        self.formLayout_2.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.horizontalLayout_config.addWidget(self.groupBox_cfg_time)

        self.groupBox_cfg_batches = QGroupBox(self.centralwidget)
        self.groupBox_cfg_batches.setObjectName(u"groupBox_cfg_batches")
        self.formLayout_3 = QFormLayout(self.groupBox_cfg_batches)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.formLayout_3.setContentsMargins(-1, -1, 6, -1)
        self.label_8 = QLabel(self.groupBox_cfg_batches)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.spinBox_max_chars = QSpinBox(self.groupBox_cfg_batches)
        self.spinBox_max_chars.setObjectName(u"spinBox_max_chars")
        self.spinBox_max_chars.setMinimum(10)
        self.spinBox_max_chars.setMaximum(99999)

        self.horizontalLayout_7.addWidget(self.spinBox_max_chars)

        self.pushButton_reset_max_chars = QPushButton(self.groupBox_cfg_batches)
        self.pushButton_reset_max_chars.setObjectName(u"pushButton_reset_max_chars")
        self.pushButton_reset_max_chars.setIcon(icon)
        self.pushButton_reset_max_chars.setFlat(True)

        self.horizontalLayout_7.addWidget(self.pushButton_reset_max_chars)

        self.horizontalLayout_7.setStretch(0, 1)

        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.label_9 = QLabel(self.groupBox_cfg_batches)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.spinBox_max_batches = QSpinBox(self.groupBox_cfg_batches)
        self.spinBox_max_batches.setObjectName(u"spinBox_max_batches")
        self.spinBox_max_batches.setMinimum(1)

        self.horizontalLayout_8.addWidget(self.spinBox_max_batches)

        self.pushButton_reset_max_batches = QPushButton(self.groupBox_cfg_batches)
        self.pushButton_reset_max_batches.setObjectName(u"pushButton_reset_max_batches")
        self.pushButton_reset_max_batches.setIcon(icon)
        self.pushButton_reset_max_batches.setFlat(True)

        self.horizontalLayout_8.addWidget(self.pushButton_reset_max_batches)

        self.horizontalLayout_8.setStretch(0, 1)

        self.formLayout_3.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.checkBox_banners = QCheckBox(self.groupBox_cfg_batches)
        self.checkBox_banners.setObjectName(u"checkBox_banners")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.checkBox_banners)


        self.horizontalLayout_config.addWidget(self.groupBox_cfg_batches)


        self.verticalLayout_2.addLayout(self.horizontalLayout_config)

        self.horizontalLayout_files = QHBoxLayout()
        self.horizontalLayout_files.setObjectName(u"horizontalLayout_files")
        self.pushButton_new_file = QPushButton(self.centralwidget)
        self.pushButton_new_file.setObjectName(u"pushButton_new_file")
        icon1 = QIcon()
        icon1.addFile(u":/general/page_white_text_plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_new_file.setIcon(icon1)

        self.horizontalLayout_files.addWidget(self.pushButton_new_file)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_files.addItem(self.horizontalSpacer)

        self.pushButton_save_file_glossary = QPushButton(self.centralwidget)
        self.pushButton_save_file_glossary.setObjectName(u"pushButton_save_file_glossary")
        self.pushButton_save_file_glossary.setEnabled(False)

        self.horizontalLayout_files.addWidget(self.pushButton_save_file_glossary)

        self.pushButton_cfg_save = QPushButton(self.centralwidget)
        self.pushButton_cfg_save.setObjectName(u"pushButton_cfg_save")

        self.horizontalLayout_files.addWidget(self.pushButton_cfg_save)

        self.pushButton_cfg_load = QPushButton(self.centralwidget)
        self.pushButton_cfg_load.setObjectName(u"pushButton_cfg_load")

        self.horizontalLayout_files.addWidget(self.pushButton_cfg_load)


        self.verticalLayout_2.addLayout(self.horizontalLayout_files)

        self.tableWidget = CTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(Qt.ElideNone)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_refresh_estimate = QPushButton(self.centralwidget)
        self.pushButton_refresh_estimate.setObjectName(u"pushButton_refresh_estimate")
        icon2 = QIcon()
        icon2.addFile(u":/general/arrow-circle-double-135.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_refresh_estimate.setIcon(icon2)
        self.pushButton_refresh_estimate.setFlat(True)

        self.horizontalLayout_9.addWidget(self.pushButton_refresh_estimate)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_9.addWidget(self.label)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_9)

        self.label_time = QLabel(self.centralwidget)
        self.label_time.setObjectName(u"label_time")

        self.horizontalLayout_3.addWidget(self.label_time)

        self.pushButton_clear = QPushButton(self.centralwidget)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.horizontalLayout_3.addWidget(self.pushButton_clear)

        self.pushButton_abort = QPushButton(self.centralwidget)
        self.pushButton_abort.setObjectName(u"pushButton_abort")
        icon3 = QIcon()
        icon3.addFile(u":/general/cancel.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_abort.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.pushButton_abort)

        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        icon4 = QIcon()
        icon4.addFile(u":/general/accept.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_start.setIcon(icon4)

        self.horizontalLayout_3.addWidget(self.pushButton_start)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")

        self.verticalLayout_2.addWidget(self.progressBar)

        self.verticalLayout_2.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Auto Deep Ver.1.4", None))
        self.groupBox_cfg_lang.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Translate to", None))
        self.checkBox_use_glossary.setText(QCoreApplication.translate("MainWindow", u"Use a glossary", None))
        self.pushButton_get_glossary.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.label_glossary.setText(QCoreApplication.translate("MainWindow", u"<No glossary selected>", None))
        self.groupBox_cfg_time.setTitle(QCoreApplication.translate("MainWindow", u"Timing", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Min. wait time per batch (seconds)", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_min_wait.setToolTip(QCoreApplication.translate("MainWindow", u"Restore default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_min_wait.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Wait time per character (milli seconds)", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_char_wait.setToolTip(QCoreApplication.translate("MainWindow", u"Restore default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_char_wait.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Wait time between batches (seconds)", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_batch_time.setToolTip(QCoreApplication.translate("MainWindow", u"Restore default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_batch_time.setText("")
        self.groupBox_cfg_batches.setTitle(QCoreApplication.translate("MainWindow", u"Batches", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Max. number of characters per batch", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_max_chars.setToolTip(QCoreApplication.translate("MainWindow", u"Restore default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_max_chars.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Max. number of batches per session", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_max_batches.setToolTip(QCoreApplication.translate("MainWindow", u"Restore default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_max_batches.setText("")
        self.checkBox_banners.setText(QCoreApplication.translate("MainWindow", u"Close banners", None))
        self.pushButton_new_file.setText(QCoreApplication.translate("MainWindow", u"Add File", None))
        self.pushButton_save_file_glossary.setText(QCoreApplication.translate("MainWindow", u"Save File With Glossary", None))
        self.pushButton_cfg_save.setText(QCoreApplication.translate("MainWindow", u"Save Configuration", None))
        self.pushButton_cfg_load.setText(QCoreApplication.translate("MainWindow", u"Load Configuration", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"File", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Output", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Status", None));
#if QT_CONFIG(tooltip)
        self.pushButton_refresh_estimate.setToolTip(QCoreApplication.translate("MainWindow", u"Restore default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_refresh_estimate.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Time Estimate:", None))
        self.label_time.setText("")
        self.pushButton_clear.setText(QCoreApplication.translate("MainWindow", u"Clear Selection", None))
        self.pushButton_abort.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi

