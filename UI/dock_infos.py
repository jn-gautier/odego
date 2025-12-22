from PyQt6.QtWidgets import QGridLayout, QWidget, QComboBox, QDockWidget, QLabel
from PyQt6.QtCore import Qt
from datetime import date

def set_dock_infos(self):
    niveau=['','1', '2', '3', '4', '5', '6']
    classes=['','-','a','b','c','d','e','f','g','h','i','j','k','l','m','z !?!?']
    sections=['','GT','TQ']
    delibe=['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Décembre']
    now=date.today()
    annees=[str(now.year-2),str(now.year-1),str(now.year),str(now.year+1),str(now.year+2)]
    #
    grid=QGridLayout()
    widget=QWidget()
    widget.setLayout(grid)
    self.combo_niveau=QComboBox()
    self.combo_niveau.addItems(niveau)
    
    self.combo_classes=QComboBox()
    self.combo_classes.addItems(classes)
    
    self.combo_section=QComboBox()
    self.combo_section.addItems(sections)
    
    self.combo_delib=QComboBox()
    self.combo_delib.addItems(delibe)
    self.combo_delib.setCurrentIndex(now.month-1)
    
    self.combo_annees=QComboBox()
    self.combo_annees.addItems(annees)
    self.combo_annees.setCurrentIndex(2)
    #
    grid.addWidget(QLabel( "Niveau :" ),1,0)
    grid.addWidget(QLabel( "Classe :" ),2,0)
    grid.addWidget(QLabel( "Section :" ),3,0)
    grid.addWidget(QLabel( "Période :" ),4,0)
    #
    grid.addWidget(self.combo_niveau,1,1)
    grid.addWidget(self.combo_classes,2,1)
    grid.addWidget(self.combo_section,3,1)
    grid.addWidget(self.combo_delib,4,1)
    grid.addWidget(self.combo_annees,4,2)
    grid.setRowStretch(5,1)
    #grid.setColumnStretch(3,1)
    #
    dockWidget=QDockWidget(self)
    dockWidget.setTitleBarWidget(QLabel( '<p style="font-size:10pt;font-weight:bold">Informations</p>' ))
    #dockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
    #dockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable)
    dockWidget.setWidget(widget)
    dockWidget.setMaximumWidth(200)
    self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,dockWidget)