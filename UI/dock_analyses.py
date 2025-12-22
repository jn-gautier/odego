from PyQt6.QtWidgets import QVBoxLayout, QWidget, QCheckBox, QDockWidget, QLabel
from PyQt6.QtCore import Qt

def set_dock_analyses(self):
    self.radio_tab_recap=QCheckBox("Tableau récapitulatif")
    self.radio_tab_recap.setToolTip ('<p>Produire un tableau récapitulatif "classique" avec la sitation globale, la moyenne pondérée et le nombre d\' heures d\'échec.</p>')
    self.radio_tab_recap.setChecked(True)
    self.radio_ana_det=QCheckBox("Analyse detaillée")
    self.radio_ana_det.setToolTip (('<p>Produire un fichier présentant pour chaque élève les détails de ses résultats et les raisons d\' un éventuel échec.</p>'))
    self.radio_ana_det.setChecked(True)
    self.radio_classmt=QCheckBox("Classement")
    self.radio_classmt.setToolTip (('<p>Produire un tableau avec le classement des élèves en fonction de leur moyenne pondérée.</p>'))
    #
    v_layout=QVBoxLayout()
    v_layout.addWidget(self.radio_tab_recap)
    v_layout.addWidget(self.radio_ana_det)
    v_layout.addWidget(self.radio_classmt)
    v_layout.addStretch(1)
    
    widget=QWidget()
    widget.setLayout(v_layout)
    #
    dockWidget=QDockWidget(self)
    #dockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
    #dockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable)
    dockWidget.setTitleBarWidget(QLabel( '<p style="font-size:10pt;font-weight:bold">Analyses</p>' ))
    dockWidget.setWidget(widget)
    dockWidget.setMaximumWidth(200)
    self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,dockWidget)
    #