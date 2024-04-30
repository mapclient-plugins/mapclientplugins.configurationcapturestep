

from PySide6 import QtWidgets, QtCore, QtGui
from cmlibs.widgets.delegates.checkboxdelegate import CheckBoxDelegate
from mapclientplugins.configurationcapturestep.ui_configuredialog import Ui_ConfigureDialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


class ConfigureDialog(QtWidgets.QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._identifier_model = CustomTableModel(labels=['Identifier', 'Use'])
        self._name_model = CustomTableModel(labels=['Name', 'Use'])
        self._checked_names = []
        self._checked_identifiers = []

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)
        self._ui.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        check_box_delegate = CheckBoxDelegate(self._ui.tableView)
        self._ui.tableView.setItemDelegateForColumn(1, check_box_delegate)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._model_changed()
        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditIdentifier.textChanged.connect(self.validate)
        self._ui.radioButtonListByName.toggled.connect(self._model_changed)
        self._ui.radioButtonListByIdentifier.toggled.connect(self._model_changed)

    def _model_changed(self):
        if self._ui.radioButtonListByIdentifier.isChecked():
            self._ui.tableView.setModel(self._identifier_model)
        elif self._ui.radioButtonListByName.isChecked():
            self._ui.tableView.setModel(self._name_model)

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.StandardButton.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(
                self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            QtWidgets.QDialog.accept(self)

    def setData(self, identifier_data, name_data):
        identifier_checked_data = [identifier in self._checked_identifiers for identifier in identifier_data]
        name_checked_data = [name in self._checked_names for name in name_data]
        self._identifier_model.reset_data(identifier_data, identifier_checked_data)
        self._name_model.reset_data(name_data, name_checked_data)

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        value = self.identifierOccursCount(self._ui.lineEditIdentifier.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEditIdentifier.text())
        if valid:
            self._ui.lineEditIdentifier.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEditIdentifier.setStyleSheet(INVALID_STYLE_SHEET)

        identifiers_valid = True
        for identifier in self._checked_identifiers:
            if not self._identifier_model.exists(identifier):
                identifiers_valid = False

        names_valid = True
        for name in self._checked_names:
            if not self._name_model.exists(name):
                names_valid = False

        return valid and identifiers_valid and names_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """

        self._previousIdentifier = self._ui.lineEditIdentifier.text()
        config = {
            'identifier': self._ui.lineEditIdentifier.text(),
            'active_model': 'names' if self._ui.radioButtonListByName.isChecked() else 'identifiers',
            'checked_names': self._name_model.checked(),
            'checked_identifiers': self._identifier_model.checked(),
        }
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = config['identifier']
        self._ui.lineEditIdentifier.setText(config['identifier'])
        self._ui.radioButtonListByName.setChecked(config['active_model'] == 'names')
        self._ui.radioButtonListByIdentifier.setChecked(config['active_model'] == 'identifiers')
        self._checked_names = config['checked_names']
        self._checked_identifiers = config['checked_identifiers']


class CustomTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None, labels=None):
        QtCore.QAbstractTableModel.__init__(self)
        self._column_count = 2
        self._names = data[0] if data else []
        self._labels = labels if labels else ['Name', 'Use']
        self._checked = data[1] if data else []
        self._row_count = len(self._names)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self._row_count

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self._column_count

    def reset_data(self, names, checks):
        self.beginResetModel()
        self._names = names
        self._checked = checks
        self._row_count = len(names)
        self.endResetModel()

    def checked(self):
        checked_names = []
        for index, c in enumerate(self._checked):
            if c:
                checked_names.append(self._names[index])

        return checked_names

    def exists(self, name):
        return name in self._names

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Orientation.Horizontal:
            return self._labels[section]
        else:
            return f"{section}"

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        column = index.column()
        row = index.row()

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return self._names[row]
            elif column == 1:
                return self._checked[row]
        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole and column == 1:
            return QtCore.Qt.AlignmentFlag.AlignCenter

        return None

    def setData(self, index, value, role=QtCore.Qt.ItemDataRole.EditRole):
        if index.isValid():
            column = index.column()
            if role == QtCore.Qt.ItemDataRole.EditRole:
                row = index.row()
                if column == 1:
                    self._checked[row] = not self._checked[row]
                    self.dataChanged.emit(index, index)
                    return True

        return False

    def flags(self, index):
        if index.isValid():
            if index.column() == 1:
                return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable
            else:
                return QtCore.Qt.ItemFlag.ItemIsEnabled

        return QtCore.Qt.ItemFlag.NoItemFlags
