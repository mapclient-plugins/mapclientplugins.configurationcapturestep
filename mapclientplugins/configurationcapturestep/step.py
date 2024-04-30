
"""
MAP Client Plugin Step
"""
import json

from PySide6 import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclient.settings.general import get_configuration_file
from mapclientplugins.configurationcapturestep.configuredialog import ConfigureDialog


class ConfigurationCaptureStep(WorkflowStepMountPoint):
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

    def __init__(self, location):
        super(ConfigurationCaptureStep, self).__init__('ConfigurationCapture', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Utility'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/configurationcapturestep/images/utility.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides-list-of',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        # Port data:
        self._portData0 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        # Config:
        self._config = {
            'identifier': '',
            'active_model': 'names',
            'checked_names': [],
            'checked_identifiers': [],
        }

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.
        self._doneExecution()

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.

        :param index: Index of the port to return.
        """
        identifiers = self._config['checked_identifiers']
        if self._config['active_model'] == 'names':
            identifiers = []
            scene = self._main_window.model().workflowManager().scene()
            for name in self._config['checked_names']:
                identifiers.extend(scene.matching_identifiers(name))

        config_files = [get_configuration_file(self._location, identifier) for identifier in identifiers]

        return config_files  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location

    def _workflow_steps_info(self):
        scene = self._main_window.model().workflowManager().scene()
        return scene.step_list(), scene.step_list(by='name')

    def _set_configure_dialog_data(self, dlg):
        identifier_data, name_data = self._workflow_steps_info()
        dlg.setData(identifier_data, name_data)

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        self._set_configure_dialog_data(dlg)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def serialize(self):
        """
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.

        :param string: JSON representation of the configuration in a string.
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._set_configure_dialog_data(d)
        self._configured = d.validate()
