# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(962, 593)
        self.set_voice = QAction(MainWindow)
        self.set_voice.setObjectName(u"set_voice")
        self.set_output = QAction(MainWindow)
        self.set_output.setObjectName(u"set_output")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_7 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.soundList = QListWidget(self.centralwidget)
        self.soundList.setObjectName(u"soundList")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.soundList.sizePolicy().hasHeightForWidth())
        self.soundList.setSizePolicy(sizePolicy)
        self.soundList.setMaximumSize(QSize(400, 16777215))

        self.horizontalLayout_7.addWidget(self.soundList)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.saveLine = QLineEdit(self.centralwidget)
        self.saveLine.setObjectName(u"saveLine")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.saveLine.sizePolicy().hasHeightForWidth())
        self.saveLine.setSizePolicy(sizePolicy1)
        self.saveLine.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_3.addWidget(self.saveLine)

        self.saveButt = QPushButton(self.centralwidget)
        self.saveButt.setObjectName(u"saveButt")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.saveButt.sizePolicy().hasHeightForWidth())
        self.saveButt.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.saveButt)

        self.playButt = QPushButton(self.centralwidget)
        self.playButt.setObjectName(u"playButt")
        sizePolicy2.setHeightForWidth(self.playButt.sizePolicy().hasHeightForWidth())
        self.playButt.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.playButt)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_2.addWidget(self.textEdit)


        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 962, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.set_voice)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.set_voice.setText(QCoreApplication.translate("MainWindow", u"\u0413\u043e\u043b\u043e\u0441", None))
        self.set_output.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f \u0444\u0430\u0439\u043b\u0430 \u0434\u043b\u044f \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f", None))
        self.saveLine.setText("")
        self.saveButt.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.playButt.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0433\u0440\u0430\u0442\u044c", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
    # retranslateUi

