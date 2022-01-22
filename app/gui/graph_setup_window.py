# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/ui/graph_setup.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(367, 208)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 160, 331, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(270, 10, 77, 129))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox.setMaximum(300)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_3.addWidget(self.spinBox)
        self.prob1 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.prob1.setObjectName("prob1")
        self.verticalLayout_3.addWidget(self.prob1)
        self.prob2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.prob2.setObjectName("prob2")
        self.verticalLayout_3.addWidget(self.prob2)
        self.k = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.k.setObjectName("k")
        self.verticalLayout_3.addWidget(self.k)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(220, 10, 41, 131))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 10, 187, 131))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget_4)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_4.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_4)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_4.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.verticalLayoutWidget_4)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_4.addWidget(self.radioButton_3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "N="))
        self.label_3.setText(_translate("Dialog", "p1="))
        self.label_4.setText(_translate("Dialog", "p2="))
        self.label_6.setText(_translate("Dialog", "k="))
        self.radioButton.setText(_translate("Dialog", "Erdos-Renyi model"))
        self.radioButton_2.setText(_translate("Dialog", "Watts-Strogatz model"))
        self.radioButton_3.setText(_translate("Dialog", "Song-Wang model"))