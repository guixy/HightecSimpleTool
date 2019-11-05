# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Enterlibraries.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LSelect(object):
    def setupUi(self, LSelect):
        LSelect.setObjectName("LSelect")
        LSelect.resize(460, 139)
        self.libraries = QtWidgets.QLineEdit(LSelect)
        self.libraries.setGeometry(QtCore.QRect(10, 40, 441, 21))
        self.libraries.setObjectName("libraries")
        self.label = QtWidgets.QLabel(LSelect)
        self.label.setGeometry(QtCore.QRect(10, 20, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(LSelect)
        self.widget.setGeometry(QtCore.QRect(280, 90, 171, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.l_OK = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_OK.sizePolicy().hasHeightForWidth())
        self.l_OK.setSizePolicy(sizePolicy)
        self.l_OK.setDefault(True)
        self.l_OK.setFlat(False)
        self.l_OK.setObjectName("l_OK")
        self.horizontalLayout.addWidget(self.l_OK)
        self.l_Cancel = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_Cancel.sizePolicy().hasHeightForWidth())
        self.l_Cancel.setSizePolicy(sizePolicy)
        self.l_Cancel.setObjectName("l_Cancel")
        self.horizontalLayout.addWidget(self.l_Cancel)

        self.retranslateUi(LSelect)
        QtCore.QMetaObject.connectSlotsByName(LSelect)

    def retranslateUi(self, LSelect):
        _translate = QtCore.QCoreApplication.translate
        LSelect.setWindowTitle(_translate("LSelect", "Enter Value"))
        self.label.setText(_translate("LSelect", "Libraries（-l）"))
        self.l_OK.setText(_translate("LSelect", "OK"))
        self.l_Cancel.setText(_translate("LSelect", "Cancel"))
