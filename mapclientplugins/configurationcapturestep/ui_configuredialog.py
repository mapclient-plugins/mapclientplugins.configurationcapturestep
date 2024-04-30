# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        if not ConfigureDialog.objectName():
            ConfigureDialog.setObjectName(u"ConfigureDialog")
        ConfigureDialog.resize(661, 552)
        self.gridLayout = QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.configGroupBox = QGroupBox(ConfigureDialog)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.formLayout = QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.labelIdentifier = QLabel(self.configGroupBox)
        self.labelIdentifier.setObjectName(u"labelIdentifier")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelIdentifier)

        self.lineEditIdentifier = QLineEdit(self.configGroupBox)
        self.lineEditIdentifier.setObjectName(u"lineEditIdentifier")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEditIdentifier)

        self.groupBoxListBy = QGroupBox(self.configGroupBox)
        self.groupBoxListBy.setObjectName(u"groupBoxListBy")
        self.verticalLayout = QVBoxLayout(self.groupBoxListBy)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioButtonListByIdentifier = QRadioButton(self.groupBoxListBy)
        self.radioButtonListByIdentifier.setObjectName(u"radioButtonListByIdentifier")
        self.radioButtonListByIdentifier.setChecked(True)

        self.verticalLayout.addWidget(self.radioButtonListByIdentifier)

        self.radioButtonListByName = QRadioButton(self.groupBoxListBy)
        self.radioButtonListByName.setObjectName(u"radioButtonListByName")

        self.verticalLayout.addWidget(self.radioButtonListByName)


        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.groupBoxListBy)

        self.tableView = QTableView(self.configGroupBox)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.tableView)


        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(ConfigureDialog)
        self.buttonBox.accepted.connect(ConfigureDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDialog.reject)

        QMetaObject.connectSlotsByName(ConfigureDialog)
    # setupUi

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QCoreApplication.translate("ConfigureDialog", u"Configure ConfigurationCapture", None))
        self.configGroupBox.setTitle("")
        self.labelIdentifier.setText(QCoreApplication.translate("ConfigureDialog", u"Identifier:  ", None))
        self.groupBoxListBy.setTitle(QCoreApplication.translate("ConfigureDialog", u"List by:", None))
        self.radioButtonListByIdentifier.setText(QCoreApplication.translate("ConfigureDialog", u"Identifer", None))
        self.radioButtonListByName.setText(QCoreApplication.translate("ConfigureDialog", u"Name", None))
    # retranslateUi

