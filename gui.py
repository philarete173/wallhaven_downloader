# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(330, 290)
        MainWindow.setMinimumSize(QSize(330, 290))
        MainWindow.setMaximumSize(QSize(330, 290))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.folderfield = QLineEdit(self.centralwidget)
        self.folderfield.setObjectName(u"folderfield")
        self.folderfield.setMinimumSize(QSize(0, 25))
        self.folderfield.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.folderfield)

        self.folderbutton = QPushButton(self.centralwidget)
        self.folderbutton.setObjectName(u"folderbutton")
        self.folderbutton.setMinimumSize(QSize(100, 25))
        self.folderbutton.setMaximumSize(QSize(100, 25))

        self.horizontalLayout.addWidget(self.folderbutton)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.submitspacerleft = QSpacerItem(37, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.submitspacerleft)

        self.submitbutton = QPushButton(self.centralwidget)
        self.submitbutton.setObjectName(u"submitbutton")
        self.submitbutton.setMinimumSize(QSize(100, 25))
        self.submitbutton.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_2.addWidget(self.submitbutton)

        self.submitspacerright = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.submitspacerright)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.logarea = QPlainTextEdit(self.centralwidget)
        self.logarea.setObjectName(u"logarea")
        self.logarea.setMinimumSize(QSize(0, 0))
        self.logarea.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(9)
        self.logarea.setFont(font)
        self.logarea.setReadOnly(True)

        self.gridLayout.addWidget(self.logarea, 0, 0, 1, 1)

        self.apikeyEdit = QLineEdit(self.centralwidget)
        self.apikeyEdit.setObjectName(u"apikeyEdit")
        self.apikeyEdit.setMinimumSize(QSize(0, 25))
        self.apikeyEdit.setMaximumSize(QSize(16777215, 25))

        self.gridLayout.addWidget(self.apikeyEdit, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Wallhaven.cc wallpapers downloader", None))
        self.folderfield.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Destination folder", None))
        self.folderbutton.setText(QCoreApplication.translate("MainWindow", u"Choose Folder", None))
        self.submitbutton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.apikeyEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"API key", None))
    # retranslateUi

