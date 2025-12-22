from PyQt6.QtWidgets import QDockWidget, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from UI.actions import *

def set_dock_start(self):
    StartAction=start_action(self)
    self.boutton_ok=QPushButton(QIcon('./UI/icons/ok_apply.svg'),'Démarrer')
    self.boutton_ok.setMinimumHeight(40)
    self.boutton_ok.clicked.connect(StartAction.trigger)
         
    dockWidget=QDockWidget(self)
    dockWidget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
    dockWidget.setWidget(self.boutton_ok)
    dockWidget.setMaximumWidth(200)
    self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,dockWidget)