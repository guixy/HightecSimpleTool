# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddLibraryPath.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LSelect(object):
    def setupUi(self, LSelect):
        LSelect.setObjectName("LSelect")
        LSelect.resize(460, 139)
        self.LibraryP = QtWidgets.QLineEdit(LSelect)
        self.LibraryP.setGeometry(QtCore.QRect(10, 40, 441, 21))
        self.LibraryP.setObjectName("LibraryP")
        self.label = QtWidgets.QLabel(LSelect)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(LSelect)
        self.widget.setGeometry(QtCore.QRect(120, 90, 331, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.L_OK = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L_OK.sizePolicy().hasHeightForWidth())
        self.L_OK.setSizePolicy(sizePolicy)
        self.L_OK.setObjectName("L_OK")
        self.horizontalLayout.addWidget(self.L_OK)
        self.L_Cancel = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L_Cancel.sizePolicy().hasHeightForWidth())
        self.L_Cancel.setSizePolicy(sizePolicy)
        self.L_Cancel.setObjectName("L_Cancel")
        self.horizontalLayout.addWidget(self.L_Cancel)
        self.L_Workspace = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L_Workspace.sizePolicy().hasHeightForWidth())
        self.L_Workspace.setSizePolicy(sizePolicy)
        self.L_Workspace.setMinimumSize(QtCore.QSize(0, 0))
        self.L_Workspace.setAutoDefault(False)
        self.L_Workspace.setDefault(False)
        self.L_Workspace.setFlat(False)
        self.L_Workspace.setObjectName("L_Workspace")
        self.horizontalLayout.addWidget(self.L_Workspace)
        self.L_FileSys = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L_FileSys.sizePolicy().hasHeightForWidth())
        self.L_FileSys.setSizePolicy(sizePolicy)
        self.L_FileSys.setObjectName("L_FileSys")
        self.horizontalLayout.addWidget(self.L_FileSys)

        self.retranslateUi(LSelect)
        QtCore.QMetaObject.connectSlotsByName(LSelect)

    def retranslateUi(self, LSelect):
        _translate = QtCore.QCoreApplication.translate
        LSelect.setWindowTitle(_translate("LSelect", "Add directory path"))
        self.label.setText(_translate("LSelect", "Directory："))
        self.L_OK.setText(_translate("LSelect", "OK"))
        self.L_Cancel.setText(_translate("LSelect", "Cancel"))
        self.L_Workspace.setText(_translate("LSelect", "Workspace"))
        self.L_FileSys.setText(_translate("LSelect", "File System"))
