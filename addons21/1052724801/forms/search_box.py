# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './search_box.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(997, 488)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pb_help_short = QtWidgets.QPushButton(Dialog)
        self.pb_help_short.setObjectName("pb_help_short")
        self.horizontalLayout_2.addWidget(self.pb_help_short)
        self.pb_help_long = QtWidgets.QPushButton(Dialog)
        self.pb_help_long.setObjectName("pb_help_long")
        self.horizontalLayout_2.addWidget(self.pb_help_long)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ql_filter = QtWidgets.QLabel(Dialog)
        self.ql_filter.setObjectName("ql_filter")
        self.horizontalLayout.addWidget(self.ql_filter)
        self.pb_filter = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_filter.sizePolicy().hasHeightForWidth())
        self.pb_filter.setSizePolicy(sizePolicy)
        self.pb_filter.setMinimumSize(QtCore.QSize(0, 60))
        self.pb_filter.setMaximumSize(QtCore.QSize(16777215, 60))
        self.pb_filter.setObjectName("pb_filter")
        self.horizontalLayout.addWidget(self.pb_filter)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.ql_button_bar = QtWidgets.QLabel(Dialog)
        self.ql_button_bar.setObjectName("ql_button_bar")
        self.verticalLayout.addWidget(self.ql_button_bar)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pb_nc = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_nc.sizePolicy().hasHeightForWidth())
        self.pb_nc.setSizePolicy(sizePolicy)
        self.pb_nc.setMinimumSize(QtCore.QSize(170, 40))
        self.pb_nc.setMaximumSize(QtCore.QSize(16777215, 60))
        self.pb_nc.setObjectName("pb_nc")
        self.horizontalLayout_3.addWidget(self.pb_nc)
        self.pb_nf = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_nf.sizePolicy().hasHeightForWidth())
        self.pb_nf.setSizePolicy(sizePolicy)
        self.pb_nf.setMinimumSize(QtCore.QSize(170, 0))
        self.pb_nf.setObjectName("pb_nf")
        self.horizontalLayout_3.addWidget(self.pb_nf)
        self.pb_deck = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_deck.sizePolicy().hasHeightForWidth())
        self.pb_deck.setSizePolicy(sizePolicy)
        self.pb_deck.setMinimumSize(QtCore.QSize(0, 0))
        self.pb_deck.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pb_deck.setObjectName("pb_deck")
        self.horizontalLayout_3.addWidget(self.pb_deck)
        self.pb_tag = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_tag.sizePolicy().hasHeightForWidth())
        self.pb_tag.setSizePolicy(sizePolicy)
        self.pb_tag.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pb_tag.setObjectName("pb_tag")
        self.horizontalLayout_3.addWidget(self.pb_tag)
        self.pb_card_props = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_card_props.sizePolicy().hasHeightForWidth())
        self.pb_card_props.setSizePolicy(sizePolicy)
        self.pb_card_props.setObjectName("pb_card_props")
        self.horizontalLayout_3.addWidget(self.pb_card_props)
        self.pb_card_state = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_card_state.sizePolicy().hasHeightForWidth())
        self.pb_card_state.setSizePolicy(sizePolicy)
        self.pb_card_state.setObjectName("pb_card_state")
        self.horizontalLayout_3.addWidget(self.pb_card_state)
        self.pb_date_added = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_date_added.sizePolicy().hasHeightForWidth())
        self.pb_date_added.setSizePolicy(sizePolicy)
        self.pb_date_added.setObjectName("pb_date_added")
        self.horizontalLayout_3.addWidget(self.pb_date_added)
        self.pb_date_rated = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_date_rated.sizePolicy().hasHeightForWidth())
        self.pb_date_rated.setSizePolicy(sizePolicy)
        self.pb_date_rated.setObjectName("pb_date_rated")
        self.horizontalLayout_3.addWidget(self.pb_date_rated)
        self.pb_date_edited = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_date_edited.sizePolicy().hasHeightForWidth())
        self.pb_date_edited.setSizePolicy(sizePolicy)
        self.pb_date_edited.setObjectName("pb_date_edited")
        self.horizontalLayout_3.addWidget(self.pb_date_edited)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pte = QtWidgets.QPlainTextEdit(Dialog)
        self.pte.setObjectName("pte")
        self.verticalLayout.addWidget(self.pte)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pb_history = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_history.sizePolicy().hasHeightForWidth())
        self.pb_history.setSizePolicy(sizePolicy)
        self.pb_history.setMinimumSize(QtCore.QSize(200, 0))
        self.pb_history.setObjectName("pb_history")
        self.horizontalLayout_4.addWidget(self.pb_history)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.pb_accepted = QtWidgets.QPushButton(Dialog)
        self.pb_accepted.setMinimumSize(QtCore.QSize(240, 0))
        self.pb_accepted.setObjectName("pb_accepted")
        self.horizontalLayout_4.addWidget(self.pb_accepted)
        self.pb_rejected = QtWidgets.QPushButton(Dialog)
        self.pb_rejected.setMinimumSize(QtCore.QSize(140, 0))
        self.pb_rejected.setObjectName("pb_rejected")
        self.horizontalLayout_4.addWidget(self.pb_rejected)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pb_help_short.setText(_translate("Dialog", "Show Search CheatSheet"))
        self.pb_help_long.setText(_translate("Dialog", "Open Manual"))
        self.ql_filter.setText(_translate("Dialog", "Option 1: add filter from a nested menu. This is similar to the button from the top left of the browser: "))
        self.pb_filter.setText(_translate("Dialog", "Filter"))
        self.ql_button_bar.setText(_translate("Dialog", "Option 2: open dialog to select filter to limit by:"))
        self.pb_nc.setText(_translate("Dialog", "Note Type\n"
"Card"))
        self.pb_nf.setText(_translate("Dialog", "Note Type\n"
"Field"))
        self.pb_deck.setText(_translate("Dialog", "Deck"))
        self.pb_tag.setText(_translate("Dialog", "Tag"))
        self.pb_card_props.setText(_translate("Dialog", "Card\n"
"Properties"))
        self.pb_card_state.setText(_translate("Dialog", "Card\n"
"State"))
        self.pb_date_added.setText(_translate("Dialog", "Date\n"
"Added"))
        self.pb_date_rated.setText(_translate("Dialog", "Date\n"
"Rated"))
        self.pb_date_edited.setText(_translate("Dialog", "Date\n"
"Edited"))
        self.pb_history.setText(_translate("Dialog", "add old Search (History)"))
        self.pb_accepted.setText(_translate("Dialog", "Ok"))
        self.pb_rejected.setText(_translate("Dialog", "Cancel"))
