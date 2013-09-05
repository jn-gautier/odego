#! /usr/bin/python
# -*- coding: utf-8 -*- 

from xml.dom.minidom import parse
import locale
from os.path import *
from lpod.document import odf_get_document, odf_new_document
from types import *
from lpod.table import *
from lpod.style import *
from lpod.paragraph import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import traceback
from datetime import date , datetime
#import datetime
import types
from functools import cmp_to_key 
import xml.etree.ElementTree as ET

class Gui(QMainWindow):
    
     def __init__(self):
         super(Gui, self).__init__()
         #self.initUI()
         self.file_to_open=QLineEdit(u"Sélectionnez le fichier.")
         self.tableau_valide=False
         
         new_from_fileAction = QAction(QIcon('./icons/import_file.svg'),u"&Importer les points à partir d'un fichier", self)
         new_from_fileAction.setShortcut('Ctrl+I')
         new_from_fileAction.setStatusTip(u"Importer les points directement à partir d'un fichier")
         new_from_fileAction.triggered.connect(self.select_file)
         
         new_from_clipboardAction = QAction(QIcon('./icons/editpaste.png'),u"Importer les points à partir du &presse papier", self)
         new_from_clipboardAction.setShortcut('Ctrl+V')
         new_from_clipboardAction.setStatusTip(u"Importer les points à partir de données copiées depuis un fichier")
         new_from_clipboardAction.triggered.connect(self.test)
         
         StartAction = QAction(QIcon('./icons/ok_apply.svg'),u"Démarrer l'analyse", self)
         StartAction.setShortcut('Ctrl+D')
         StartAction.setStatusTip(u"Démarrer")
         StartAction.triggered.connect(self.verif_avant_analyse)
         
         QuitAction = QAction(QIcon('./icons/quit.svg'),"Quitter", self)
         QuitAction.setShortcut('Ctrl+Q')
         QuitAction.setStatusTip(u"Quitter")
         QuitAction.triggered.connect(self.appExit)
         
         HelpAction = QAction(u"Obtenir de l'aide", self)
         HelpAction.setStatusTip(u"Obtenir de l'aide concernant l'utilisation de ce logiciel")
         HelpAction.triggered.connect(self.test)
         
         AboutAction = QAction(u"A propos", self)
         AboutAction.setStatusTip(u"A propos de ce logiciel")
         AboutAction.triggered.connect(self.test)
         
         menubar = self.menuBar()
         
         fileMenu = menubar.addMenu(u'&Application')
         fileMenu.addAction(StartAction)
         fileMenu.addAction(QuitAction)
         
         fileMenu = menubar.addMenu(u'&Importer')
         fileMenu.addAction(new_from_fileAction)
         fileMenu.addAction(new_from_clipboardAction)
         
         fileMenu = menubar.addMenu('&Aide')
         fileMenu.addAction(HelpAction)
         fileMenu.addAction(AboutAction)
         
         self.toolbar = self.addToolBar('Toolbar')
         self.toolbar.addAction(new_from_fileAction)
         self.toolbar.addAction(new_from_clipboardAction)
         self.toolbar.addAction(QuitAction)
         #self.toolbar.addAction(StartAction)
         
         self.statusBar()
         
         #self.setGeometry(300, 300, 300, 200)
         self.setWindowTitle('Odego')
         self.center()
         self.setWindowIcon(QIcon('./icons/odego.svg')) 
         
         niveau=['','1', '2', '3', '4', '5', '6']
         classes=['','a','b','c','d','e','f','g','h','i','j','k','l','m','z !?!?']
         sections=['','GT','TQ']
         delibe=[u'Noel',u'Mars',u'Juin']
         now=date.today()
         
         annees=[str(now.year-2),str(now.year-1),str(now.year),str(now.year+1),str(now.year+2)]
         #
         grid=QGridLayout()
         #self.fname=False
         #self.fichier_valide=False
         self.combo_niveau=QComboBox()
         self.combo_niveau.addItems(niveau)
         self.combo_classes=QComboBox()
         self.combo_classes.addItems(classes)
         self.combo_section=QComboBox()
         self.combo_section.addItems(sections)
         self.combo_delib=QComboBox()
         self.combo_delib.addItems(delibe)
         self.combo_annees=QComboBox()
         self.combo_annees.addItems(annees)
         #
         grid.addWidget(QLabel( u"Niveau :" ),1,0)
         grid.addWidget(QLabel( u"Classe :" ),2,0)
         grid.addWidget(QLabel( u"Section :" ),3,0)
         grid.addWidget(QLabel( u"Période :" ),4,0)
         #
         grid.addWidget(self.combo_niveau,1,1)
         grid.addWidget(self.combo_classes,2,1)
         grid.addWidget(self.combo_section,3,1)
         grid.addWidget(self.combo_delib,4,1)
         grid.addWidget(self.combo_annees,4,2)
         grid.setRowStretch(5,1)
         grid.setColumnStretch(3,1)
         #
         widget=QWidget()
         widget.setLayout(grid)
         #
         logDockWidget=QDockWidget(self)
         logDockWidget.setTitleBarWidget(QLabel( '<p style="font-size:10pt;font-weight:bold">Informations</p>' ))
         logDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
         logDockWidget.setFeatures(QDockWidget.DockWidgetFloatable)
         logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
         logDockWidget.setWidget(widget)
         logDockWidget.setMaximumWidth(200)
         self.addDockWidget(Qt.LeftDockWidgetArea,logDockWidget)
         #
         self.radio1=QCheckBox(u"Tableau récapitulatif")
         self.radio2=QCheckBox(u"Analyse detaillée")
         self.radio3=QCheckBox("Classement")
         #
         v_layout=QVBoxLayout()
         v_layout.addWidget(self.radio1)
         v_layout.addWidget(self.radio2)
         v_layout.addWidget(self.radio3)
         v_layout.addStretch(1)
         
         widget=QWidget()
         widget.setLayout(v_layout)
         #
         logDockWidget=QDockWidget(self)
         logDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
         logDockWidget.setFeatures(QDockWidget.DockWidgetFloatable)
         logDockWidget.setTitleBarWidget(QLabel( '<p style="font-size:10pt;font-weight:bold">Analyses</p>' ))
         logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
         logDockWidget.setWidget(widget)
         logDockWidget.setMaximumWidth(200)
         self.addDockWidget(Qt.LeftDockWidgetArea,logDockWidget)
         #
         self.boutton_ok=QPushButton(QIcon('./icons/ok_apply.svg'),u'Démarrer')
         self.boutton_ok.setMinimumHeight(40)
         self.connect(self.boutton_ok, SIGNAL("clicked()"),self.verif_avant_analyse)
         
         logDockWidget=QDockWidget(self)
         logDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
         logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
         logDockWidget.setWidget(self.boutton_ok)
         logDockWidget.setMaximumWidth(200)
         self.addDockWidget(Qt.LeftDockWidgetArea,logDockWidget)
         
         self.setWindowTitle(u'Odego : un guide pour les délibérations')
         self.combo_annees.setCurrentIndex(2)
         if now.month in [10,11,12,1]:
             self.combo_delib.setCurrentIndex(0)
         if now.month in [2,3,4,5]:
             self.combo_delib.setCurrentIndex(1)
         if now.month in [6,7,8,9]:
             self.combo_delib.setCurrentIndex(2)
     #
     def center(self):
         qr = self.frameGeometry()
         cp = QDesktopWidget().availableGeometry().center()
         qr.moveCenter(cp)
         self.move(qr.topLeft())
     #
     def test(self):
         print 'hello'
     #
     def appExit(self):
         print "Au revoir!"
         app.quit()
     #
     def select_file(self):
         self.file_name = QFileDialog.getOpenFileName(self,'Tableau avec les points de la classe.','/home/gautier/dossier_ivf/odego-projet/')
         self.get_file_ext()
         classe.__init__()
         # je réinitialise la classe au cas ou l'utilisateur tente d'importer un fichier de points alors que cela a déjà été fait
         if self.ext=='ods':
             self.import_ods()
         elif self.ext=='xls':
             self.import_xls()
         elif self.ext=='xslx':
             pass
         elif self.ext=='txt':
             self.import_txt()
         elif self.ext=='csv':
             self.import_txt()
         else:
             QMessageBox.warning(self,'Erreur',u"Veuillez renseigner un fichier avec l'extension 'ods', 'xls' ou 'xslx'.")
     #
     def get_file_ext(self):
         ext=self.file_name.split('.')
         self.ext=ext[len(ext)-1]
     #
     def import_ods(self):
         doc = odf_get_document(str(self.file_name))
         body=doc.get_body()
         table=body.get_tables()[0]
         table.rstrip()
         #
         try:
             ligne_cours=False
             for row in table.get_rows():
                 prem_cell=row.get_value(0)
                 if prem_cell!=None:
                     if (prem_cell.lower()=='cours'):
                         ligne_cours=True
                         for cell in row.get_values():
                             if cell!=None: #il peut y avoir des cellules vides qui suivent celles avec les intitulés des cours ; on ne prend en compte que les cellules non vides.
                                 classe.liste_cours.append(cell)
                         del classe.liste_cours[0]
             if ligne_cours==False:
                 raise ExceptionPasCours
         except ExceptionPasCours :
             QMessageBox.critical(self,'Echec',u"<p>Il n'y a pas de ligne avec les cours dans votre fichier</p> <p>ou celle-ci n'est pas indiquée par le mot 'Cours'</p>")
             print "Il n'y a pas de ligne avec les cours dans votre fichier, ou celle-ci n'est pas indiquée par le mot 'Cours'"
         try:    
             for row in table.get_rows():
                 prem_cell=row.get_value(0)
                 if (prem_cell==None) or ( (prem_cell[0]=='&') & (prem_cell[1]=='&') or (prem_cell.lower()=='cours')):
                     pass
                 else:
                     eleve=Eleve()
                     if type(row.get_value(0)) is not unicode:
                         eleve.nom=unicode(row.get_value(0),'utf-8')
                         # le nom de l'élève est supposé se trouver dans la première cellule
                     else:
                         eleve.nom=row.get_value(0)
                     ligne_points=row.get_values()
                     del ligne_points[0] # on supprime le nom de l'élève
                     for cours,points_eleve in zip(classe.liste_cours,ligne_points):
                         #on parcours simultanement la liste des cours et celle des points
                         
                         #
                         if (cours.lower()=='pia') & (points_eleve!=None):
                             eleve.pia=True
                         #
                         elif (cours.lower()=='ctg') & (points_eleve!=None):
                             eleve.ctg=True
                         #
                         elif (cours.lower()=='ddn') & (points_eleve!=None):
                             eleve.ddn=points_eleve
                         #
                         elif points_eleve!=None:
                             eleve.grille_horaire[cours]=Cours()
                             #if points_eleve==None : points_eleve=False
                             eleve.grille_horaire[cours].analyse_points(str(points_eleve))
                             if eleve.grille_horaire[cours].points!=False : eleve.eval_certif=True
                         else : pass
                         print eleve.nom , cours, points_eleve
                     classe.carnet_cotes[eleve.nom]=eleve
         except Exception, e:
             message=u"<p>Un problème majeur a été rencontré lors de l'importation de votre fichier.</p>"
             message+=u"<p>Essayez d'importer vos points par copier-coller.</p>"
             message+=u'<p>Veuillez signaler cette erreur au développeur.</p></div>'
             QMessageBox.critical(self,'Echec',message)
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc()
         if 'DDN' in classe.liste_cours:
             classe.liste_cours.remove('DDN')
         if 'CTG' in classe.liste_cours:
             classe.liste_cours.remove('CTG')
         if 'PIA' in classe.liste_cours:
             classe.liste_cours.remove('PIA')
         
         classe.prod_liste_eleves()
         classe.update_liste_cours()
         #print classe.liste_cours
         self.tableau_valide=True
         
         if self.tableau_valide==True:
             self.update_tableau_points_view()
     #
     def import_xls(self):
         import xlrd
         workbook = xlrd.open_workbook(str(self.file_name))
         worksheet = workbook.sheet_by_index(0)
         try:
             ligne_cours=False
             for rownum in range(worksheet.nrows):
                 ligne_points=worksheet.row_values(rownum)
                 prem_cell=ligne_points[0]
                 if prem_cell!=(None or ''):
                     if (prem_cell.lower()=='cours'):
                         ligne_cours=True
                         for cell in ligne_points:
                             if cell!=(''): #il peut y avoir des cellules vides qui suivent celles avec les intitulés des cours ; on ne prend en compte que les cellules non vides.
                                 classe.liste_cours.append(cell)
                         del classe.liste_cours[0]
             if ligne_cours==False:
                 raise ExceptionPasCours
         except ExceptionPasCours :
             QMessageBox.critical(self,'Echec',u"<p>Il n'y a pas de ligne avec les cours dans votre fichier</p> <p>ou celle-ci n'est pas indiquée par le mot 'Cours'</p>")
             print "Il n'y a pas de ligne avec les cours dans votre fichier, ou celle-ci n'est pas indiquée par le mot 'Cours'"
         #
         try:
             for rownum in range(worksheet.nrows):
                 ligne_points=worksheet.row_values(rownum)
                 prem_cell=ligne_points[0]
                 if (prem_cell=='') or ( (prem_cell[0]=='&') & (prem_cell[1]=='&')) or (prem_cell.lower()=='cours'):
                     pass
                 else:
                     eleve=Eleve()
                     #eleve.grille_horaire=copy.deepcopy(self.grille_horaire)
                     eleve.nom=ligne_points[0]
                     if type(eleve.nom) is not unicode:
                         eleve.nom=unicode(eleve.nom,'utf-8')
                     del ligne_points[0]
                     for cours,cell in zip(classe.liste_cours,ligne_points):
                         points_eleve=cell
                         if points_eleve=='':
                             points_eleve=None
                         #
                         if (cours.lower()=='pia') & (points_eleve!=''):
                             eleve.pia=True
                         #
                         elif (cours.lower()=='ctg') & (points_eleve!=''):
                             eleve.ctg=True
                         #
                         elif (cours.lower()=='ddn') & (points_eleve!=''):
                             eleve.ddn=points_eleve
                         #
                         elif points_eleve!='':
                             #if points_eleve==(''):
                                 #points_eleve=False
                             eleve.grille_horaire[cours]=Cours()
                             eleve.grille_horaire[cours].analyse_points(str(points_eleve))
                             if eleve.grille_horaire[cours].points!=False:
                                 eleve.eval_certif=True
                         else: pass
                         print eleve.nom , cours, points_eleve
                     classe.carnet_cotes[eleve.nom]=eleve
         except Exception, e:
             message=u"<p>Un problème majeur a été rencontré lors de l'importation de votre fichier.</p>"
             message+=u"<p>Essayez d'importer vos points par copier-coller.</p>"
             message+=u'<p>Veuillez signaler cette erreur au développeur.</p></div>'
             QMessageBox.critical(self,'Echec',message)
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc()
             #traceback.print_exc()
         if 'DDN' in classe.liste_cours:
             classe.liste_cours.remove('DDN')
         if 'CTG' in classe.liste_cours:
             classe.liste_cours.remove('CTG')
         if 'PIA' in classe.liste_cours:
             classe.liste_cours.remove('PIA')
         #print 'Liste des cours : ' , classe.liste_cours
         classe.prod_liste_eleves()
         classe.update_liste_cours()
         print classe.liste_cours
         self.tableau_valide=True
         
         if self.tableau_valide==True:
             self.update_tableau_points_view()
     #
     def import_txt(self):
         QMessageBox.information(self,'Information',u"<p>L'importation depuis un fichier txt ou csv nécessite </p><p>que les valeurs soient séparées par des tabulations.</p>")
         myfile= open(self.file_name, "r")
         
         try:
             ligne_cours=False
             for ligne in myfile:
                 #print ligne.rstrip('\n\r').split('\t')
                 #ligne=ligne.rstrip('\n\r')
                 ligne_points=ligne.rstrip('\n\r').split('\t')
                 #print ligne_points
                 prem_cell=ligne_points[0]
                 if prem_cell!=(None or ''):
                     if (prem_cell.lower()=='cours'):
                         ligne_cours=True
                         for cell in ligne_points:
                             if cell!=(None or ''): #il peut y avoir des cellules vides qui suivent celles avec les intitulés des cours ; on ne prend en compte que les cellules non vides.
                                 classe.liste_cours.append(cell)
                         del classe.liste_cours[0]
             if ligne_cours==False:
                 raise ExceptionPasCours
         except ExceptionPasCours :
             QMessageBox.critical(self,'Echec',u"<p>Il n'y a pas de ligne avec les cours dans votre fichier</p> <p>ou celle-ci n'est pas indiquée par le mot 'Cours'</p>")
             print "Il n'y a pas de ligne avec les cours dans votre fichier, ou celle-ci n'est pas indiquée par le mot 'Cours'"
         #
         try:
             myfile= open(self.file_name, "r")
             for ligne in myfile:
                 
                 ligne_points=ligne.rstrip('\n\r').split('\t')
                 prem_cell=ligne_points[0]
                 if (prem_cell=='') or ( (prem_cell[0]=='&') & (prem_cell[1]=='&')) or (prem_cell.lower()=='cours'):
                     pass
                 else:
                     eleve=Eleve()
                     #eleve.grille_horaire=copy.deepcopy(self.grille_horaire)
                     eleve.nom=ligne_points[0]
                     if type(eleve.nom) is not unicode:
                         eleve.nom=unicode(eleve.nom,'utf-8')
                     del ligne_points[0]
                     for cours,cell in zip(classe.liste_cours,ligne_points):
                         points_eleve=cell
                         if points_eleve=='':
                             points_eleve=False
                         #
                         if (cours.lower()=='pia') & (points_eleve!=False):
                             eleve.pia=True
                         #
                         elif (cours.lower()=='ctg') & (points_eleve!=False):
                             eleve.ctg=True
                         #
                         elif (cours.lower()=='ddn') & (points_eleve!=False):
                             pass#eleve.ddn=points_eleve
                         #
                         elif points_eleve!='':
                             eleve.grille_horaire[cours]=Cours()
                             eleve.grille_horaire[cours].analyse_points(str(points_eleve))
                             if eleve.grille_horaire[cours].points!=False:
                                 eleve.eval_certif=True
                         else : pass
                         print eleve.nom , cours, points_eleve
                     classe.carnet_cotes[eleve.nom]=eleve
         except Exception, e:
             message=u"<p>Un problème majeur a été rencontré lors de l'importation de votre fichier.</p>"
             message+=u"<p>Essayez d'importer vos points par copier-coller.</p>"
             message+=u'<p>Veuillez signaler cette erreur au développeur.</p></div>'
             QMessageBox.critical(self,'Echec',message)
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc()
             #traceback.print_exc()
         if 'DDN' in classe.liste_cours:
             classe.liste_cours.remove('DDN')
         if 'CTG' in classe.liste_cours:
             classe.liste_cours.remove('CTG')
         if 'PIA' in classe.liste_cours:
             classe.liste_cours.remove('PIA')
         #print 'Liste des cours : ' , classe.liste_cours
         classe.prod_liste_eleves()
         classe.update_liste_cours()
         print classe.liste_cours
         self.tableau_valide=True
         
         if self.tableau_valide==True:
             self.update_tableau_points_view()
     #
     def update_tableau_points_view(self):
         self.table=QTableWidget()
         self.table.setEditTriggers(QTableWidget.NoEditTriggers)
         premier_elv=True
         for eleve in sorted(classe.liste_eleves,key=cmp_to_key(compfr)):
                 self.table.insertRow(self.table.rowCount())
                 j=0
                 for nom_cours in classe.liste_cours:
                     if premier_elv==True:
                         self.table.insertColumn(self.table.columnCount())
                     #nom_cours=nom_cours.lower()
                     if nom_cours in classe.carnet_cotes[eleve].grille_horaire.keys():
                         item=QString(unicode(str(classe.carnet_cotes[eleve].grille_horaire[nom_cours].points),'utf-8'))
                     else :
                         item=QString('')
                     newitem = QTableWidgetItem(item)
                     self.table.setItem(self.table.rowCount()-1,j, newitem)
                     j+=1
                 premier_elv=False
         labels=QStringList(classe.liste_cours)
         self.table.setHorizontalHeaderLabels(labels)
         labels=sorted(classe.liste_eleves,key=cmp_to_key(compfr))
         labels=QStringList(labels)
         self.table.setVerticalHeaderLabels(labels)
         self.setCentralWidget(self.table)
         
         new_bottom=int(0.75*(QDesktopWidget().availableGeometry().bottom()) )
         new_right=int(0.75*(QDesktopWidget().availableGeometry().right()))
         
         new_height=int(0.1*(QDesktopWidget().availableGeometry().bottom()) )
         new_left=int(0.1*(QDesktopWidget().availableGeometry().right()))
         
         self.setGeometry(new_height,new_left,new_right,new_bottom)
         self.showMaximized()
     
     def verif_avant_analyse(self):
         verif_param=True
         alert=u"<div><p> Veuillez renseigner :</p> <ul>"
         if self.combo_niveau.currentText()=='':
             verif_param=False
             alert+=u'<li>Le <b> niveau </b> de la classe.</li>'
         
         if self.combo_section.currentText()=='':
             verif_param=False
             alert+=u'<li>La <b> section </b> de la classe.</li>'
         if self.combo_classes.currentText()=='':
             verif_param=False
             alert+=u'<li>Le <b> nom </b> de la classe.</li>'
         
         if verif_param==False:
             alert+=u'</ul> </div>'
             QMessageBox.warning(self,'Informations manquantes',alert)
         
         if (self.radio1.isChecked()==False) & (self.radio2.isChecked()==False) & (self.radio3.isChecked()==False):
             message=u"<div><p>Aucune analyse n'a été demandée pour cette classe.</p>"
             message+=u"<p>N'oubliez pas de cocher les analyses souhaitées <b>avant de pousser sur démarrage</b>.</p> </div>"
             QMessageBox.information(self,u"Aucune analyse demandée",message)
         
         if self.tableau_valide==False:
             alert=u"<div><p>Aucun point n'a encore été importé.</p>"
             alert+=u"<p> Veuillez importer des points <b>avant de pousser sur démarrage</b>.</p> </div>"
             QMessageBox.warning(self,'Points manquants',alert)
         if (self.tableau_valide==True) & (verif_param==True):
             self.pre_traitement()
         
     #
     def pre_traitement(self):
         print u"Pré-traitement des données"
         #self.fichier_a_traiter=self.fname
         self.creer_tableau_recap=self.radio1.isChecked()
         self.creer_analyse_eleve=self.radio2.isChecked()
         self.creer_classement=self.radio3.isChecked()
         self.niveau=unicode(self.combo_niveau.currentText(),'utf-8')
         self.section=unicode(self.combo_section.currentText(),'utf-8')
         self.classe=unicode(self.combo_classes.currentText(),'utf-8')
         self.annee=unicode(self.combo_annees.currentText(),'utf-8')
         self.delibe=unicode(self.combo_delib.currentText(),'utf-8')
         self.path=(split(str(self.file_name)))[0]
         self.file2save=self.delibe+"_"+self.annee+"_"+self.niveau+self.section+self.classe
         self.titre='Conseil de classe '+self.niveau+self.section+self.classe+" - "+self.delibe+' '+self.annee
         #
         try:
             classe.set_param(self.niveau,self.section,self.delibe)
             if ((self.niveau=='1') or (self.niveau=='2')) & (self.section=='GT') & (self.delibe==u'Noël'):
                 self.traitement_1deg_gt_noel()
             if ((self.niveau=='1') or (self.niveau=='2')) & (self.section=='GT') & (self.delibe==u'Mars'):
                 self.traitement_1deg_gt_mars()
             if ((self.niveau=='1') or (self.niveau=='2')) & (self.section=='GT') & (self.delibe==u'Juin'):
                 self.traitement_1deg_gt_juin()
             if ((self.niveau=='3') or (self.niveau=='4')) & (self.section=='GT') & (self.delibe==u'Noël'):
                 self.traitement_345_gt_noel()
             if ((self.niveau=='3') or (self.niveau=='4')) & (self.section=='GT') & (self.delibe==u'Mars'):
                 self.traitement_345_gt_mars()
             if ((self.niveau=='3') or (self.niveau=='4')) & (self.section=='GT') & (self.delibe==u'Juin'):
                 self.traitement_345_gt_juin()
         except Exception, e:
             QMessageBox.warning(self,'Erreur',u"<div><p> Un problème a été rencontré lors du traitement de votre fichier</p>\
             <ul><li>Vérifiez que le fichier sélectionné contienne bien des <b>points</b>.</li>\
             <li>Vérifiez que le fichier sélectionné contienne bien le <b>nom des cours</b>.</li>\
             <li>Vérifiez que vous avez sélectionné la bonne <b>classe </b>et la bonne <b>section </b>dans le menu d'acceuil.</li></ul>\
             </div>")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
     #
     def traitement_1deg_gt_noel(self):
         try:
             classe.stats_elv()
             classe.prod_situation_globale()
             #classe.prod_liste_eleves()
         except Exception, e:
             QMessageBox.critical(self,u'Echec',u"Une erreur a été rencontrée dans l'analyse des points")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file2save)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file2save)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
     #
     def traitement_1deg_gt_mars(self):
         try:
             classe.stats_elv()
             classe.prod_situation_globale()
             #classe.prod_liste_eleves()
         except Exception, e:
             QMessageBox.critical(self,u'Echec',u"Une erreur a été rencontrée dans l'analyse des points")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file2save)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file2save)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
     #
     def traitement_1deg_gt_juin(self):
         try:
             classe.stats_elv()
             classe.prod_situation_globale()
             #classe.prod_liste_eleves()
         except Exception, e:
             QMessageBox.critical(self,u'Echec',u"Une erreur a été rencontrée dans l'analyse des points")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file2save)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file2save)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
     #
     def traitement_345_gt_noel(self):
         try:
             classe.stats_elv()
             classe.prod_situation_globale()
             #classe.prod_liste_eleves()
         except Exception, e:
             QMessageBox.critical(self,u'Echec',u"Une erreur a été rencontrée dans l'analyse des points")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file2save)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file2save)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
     #
     def traitement_345_gt_mars(self):
         try:
             classe.stats_elv()
             classe.prod_situation_globale()
             #classe.prod_liste_eleves()
         except Exception, e:
             QMessageBox.critical(self,u'Echec',u"Une erreur a été rencontrée dans l'analyse des points")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file2save)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file2save)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
     #
     def traitement_345_gt_juin(self):
         try:
             classe.stats_elv()
             classe.prod_situation_globale()
             #classe.prod_liste_eleves()
         except Exception, e:
             QMessageBox.critical(self,u'Echec',u"Une erreur a été rencontrée dans l'analyse des points")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file2save)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file2save)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
             print 'Message : ', traceback.format_exc() 
     #
     #
     
class ExceptionPasCours(Exception): pass
#
#
class Compfr(object):
     """Cette classe contient une unique fonction servant à comparer des chaines de caractères pour créer une classement alphabétique français"""
     # Solution prise sur : http://python.jpvweb.com/mesrecettespython/doku.php?id=tris_dictionnaire_francais
     def __init__(self):
         self.decod ='utf-8'
         locale.setlocale(locale.LC_ALL, '')
         self.espinsec = u'\xA0' # espace insécable
     #
     def __call__(self, v1, v2):
         # on convertit en unicode si nécessaire
         if isinstance(v1, str):
             v1 = v1.decode(self.decod)
         if isinstance(v2, str):
             v2 = v2.decode(self.decod)
         # on retire les tirets, les blancs insécables et les apostrophes
         v1 = v1.replace(u'-','')
         v1 = v1.replace(self.espinsec,'')
         v1 = v1.replace(u"'",'')
         #
         v2 = v2.replace(u'-','')
         v2 = v2.replace(self.espinsec,'')
         v2 = v2.replace(u"'",'')
         # on retourne le résultat de la comparaison
         return locale.strcoll(v1, v2)
#
#
class Classe(object):
     #
     def __init__(self):
         self.niveau=''
         self.section=''
         self.niv_sec=self.niveau+self.section
         self.carnet_cotes={}
         self.liste_cours=[]
         self.grille_horaire={}
         self.fichier_a_traiter=''
         self.analyses={}
     #    
     def set_param(self,niveau="",section="",delibe=""):
         self.niveau=niveau
         self.section=section
         self.delibe=delibe
         self.niv_sec=self.niveau+self.section
         liste_carac_bool=['ccnc','verrou','pseudo','option']
         liste_carac_int=['heures']
         liste_carac_str=['abr','intitule']
         #
         try:
             tree = ET.parse('./cours.xml')
             for niveau in tree.iter('niveau'):
                 if niveau.get('name')==self.niv_sec:
                     tree_niveau=niveau
             #
             for node_cours in tree_niveau:
                 cours=Cours()
                 for carac in liste_carac_bool:
                     setattr(cours, carac, bool(int(node_cours.find(carac).text)))
                 for carac in liste_carac_int:
                     setattr(cours, carac, int(node_cours.find(carac).text))
                 for carac in liste_carac_str:
                     valeure=node_cours.find(carac).text
                     if type(valeure) is not unicode:
                         valeure=unicode(valeure,'utf-8')
                     setattr(cours, carac, valeure)
                 # fusion de cours venant d'être créé avec celui présent dans la grille horaire de chaque élève de la classe
                 for eleve in self.carnet_cotes.itervalues():
                     list_cours_elv=[nom_cours.lower() for nom_cours in eleve.grille_horaire.keys()]
                     if cours.abr.lower() in list_cours_elv:
                         for carac in liste_carac_bool:
                             setattr(eleve.grille_horaire[cours.abr],carac,getattr(cours,carac))
                         for carac in liste_carac_int:
                             setattr(eleve.grille_horaire[cours.abr],carac,getattr(cours,carac))
                         for carac in liste_carac_str:
                             setattr(eleve.grille_horaire[cours.abr],carac,getattr(cours,carac))
                     else:
                         eleve.grille_horaire[cours.abr]=cours
                 #self.grille_horaire[cours.abr]=cours
             print "Création d'une classe de", self.niv_sec
         except Exception, e:
             QMessageBox.critical(gui,u'Echec',u"Erreur dans la lecture du fichier de description des cours.")
             print'Erreur dans la lecture du fichier de description des cours'
             print 'Erreur : %s' % e
             print traceback.format_exc()
         #
         try:
             tree = ET.parse('./criteres.xml')
             for niveau in tree.iter('niveau'):
                 if niveau.get('name')==self.niv_sec:
                     tree_niveau=niveau
             self.criteres=Criteres()
             for node_critere in tree_niveau:
                 setattr(self.criteres, node_critere.tag,int(node_critere.text))
         except Exception, e:
             QMessageBox.critical(gui,u'Echec',u"Erreur dans la lecture du fichier de description des critères.")
             print'Erreur dans la lecture du fichier de description des critères.'
             print 'Erreur : %s' % e
             print traceback.format_exc()
         #
         try:
             tree = ET.parse('./analyses.xml')
             for niveau in tree.iter('niveau'):
                 if niveau.get('name')==self.niv_sec:
                     tree_niveau=niveau
             for delibe in tree_niveau.iter('delibe'):
                 if delibe.get('name')==self.delibe:
                     tree_delibe=delibe
             for analyse in tree_delibe:
                 
                 self.analyses[analyse.tag]=bool(int(analyse.text))
             #print self.analyses
                 #setattr(self.analyses, analyse.tag,bool(analyse.text))
                 
         except Exception, e:
             QMessageBox.critical(gui,u'Echec',u"Erreur dans la lecture du fichier des analyses à effectuer.")
             print'Erreur dans la lecture du fichier des analyses à effectuer.'
             print 'Erreur : %s' % e
             print traceback.format_exc()
         #
     
     def stats_elv(self):
         for eleve in self.carnet_cotes.itervalues():
             if classe.analyses['fct_moyenne_ponderee']==True:
                 eleve.fct_moyenne_ponderee()
             if classe.analyses['fct_echec_inf35']==True:
                 eleve.fct_echec_inf35()
             if classe.analyses['fct_nb_heures_horaire']==True:
                 eleve.fct_nb_heures_horaire()
             if classe.analyses['fct_total_heures_echec']==True:
                 eleve.fct_total_heures_echec()
             if classe.analyses['fct_cours_verrou_echec']==True:
                 eleve.fct_cours_verrou_echec()
             if classe.analyses['fct_nb_cours_echec']==True:
                 eleve.fct_nb_cours_echec()
             if classe.analyses['fct_echec_contrat']==True:
                 eleve.fct_echec_contrat()
             if classe.analyses['fct_certif_med']==True:
                 eleve.fct_certif_med()
             if classe.analyses['fct_oubli_cours']==True:
                 eleve.fct_oubli_cours()
             if classe.analyses['fct_credits_inf_50']==True:
                 eleve.fct_credits_inf_50()
             if classe.analyses['fct_echec_travail']==True:
                 eleve.fct_echec_travail()
             if classe.analyses['fct_classement_cours']==True:
                 eleve.fct_classement_cours()
             if classe.analyses['fct_age']==True:
                 eleve.fct_age()
             if classe.analyses['fct_sciences6']==True:
                 eleve.fct_sciences6()
     #
     def prod_situation_globale(self):
         for eleve in self.carnet_cotes.itervalues():
             if eleve.heures_echec_cc==0 :
                 eleve.situation_globale=3 #aucun probleme
             #
             elif (eleve.heures_echec_cc>8) or (eleve.nb_cours_verrou_echec>=2) \
             or ((eleve.nb_cours_inf35>0) & (eleve.nb_cours_cc_echec>=2)):
                 eleve.situation_globale=1 #redoublement
             else:
                 eleve.situation_globale=2 # certains cours en echec mais réussite de l'année
             if (eleve.liste_certif_med!='') or (eleve.liste_oubli_cours!=''):
                 eleve.situation_globale=4 # non délibérable
     #
     #
     def prod_liste_eleves(self):
         self.liste_eleves=self.carnet_cotes.keys()
     #
     def update_liste_cours(self):
         self.liste_cours=[]
         for eleve in self.carnet_cotes.itervalues():
             for cours in eleve.grille_horaire.keys():
                 if cours not in self.liste_cours:
                     self.liste_cours.append(cours)
#
#
class Eleve(Classe):
     """Un élève est un membre d'une classe, il possède un nom, une grille horaire avec des points et un ensemble de
     statistiques relatives à ces points."""
     def __init__(self):
         self.pia=False
         self.ctg=False
         self.ddn=False
         self.eval_certif=False
         self.vol_horaire_cc=0
         self.vol_horaire_ccnc=0
         self.grille_horaire={}
         self.moy_pond_cc=0
         self.moy_pond_ccnc=0
         self.heures_echec_cc=0
         self.heures_echec_nc=0
         self.heures_echec_tot='0'
         self.nb_cours_verrou_echec=0
         self.liste_cours_verrou_echec=''
         self.nb_cours_cc_echec=0
         self.nb_cours_nc_echec=0
         self.liste_echec_contrat=''
         self.liste_certif_med=''
         self.liste_oubli_cours=''
         self.liste_echec_travail=''
         self.credits_inf_50=0
         self.situation_globale=0
         self.nb_cours_inf35=0
         self.liste_cours_inf35=''
         self.age=False
         self.age_str=False
     #
     #
     def fct_nb_heures_horaire(self):
         """Cette fonction calcule pour un eleve :
           => le nombre d'heures de cours certificatives dans son horaire,
           => le nombre total d'heures de cours dans son horaire.
         Les heures dans l'horaires peuvent être calculées
         dés qu'il y a une évaluation, cad s'il y a une appréciation ou des points."""
         for cours in self.grille_horaire.itervalues():
             if (cours.evaluation!=0) & (cours.pseudo==False):
                 self.vol_horaire_ccnc+=cours.heures
             if (cours.evaluation!=0) & (cours.ccnc==True):
                 self.vol_horaire_cc+=cours.heures
     #
     #
     def fct_moyenne_ponderee(self):
         """Cette fonction calcule pour un eleve :
           => la moyenne pondérée des cours certificatifs
           => la moyenne pondérée de l'ensemble des cours.
         Les moyennes pondérées ne peuvent être calculées que s'il y a des points."""
         total_heures_cc=0
         total_heures_ccnc=0
         for cours in self.grille_horaire.itervalues():
             if (cours.ccnc==True) & (cours.points!=False):
                 self.moy_pond_cc+=cours.heures*cours.points
                 total_heures_cc+=cours.heures
             #
             if (cours.points!=False) & (cours.pseudo==False):
                 self.moy_pond_ccnc+=cours.heures*cours.points
                 total_heures_ccnc+=cours.heures
         #print self.moy_pond_cc, total_heures_cc
         self.moy_pond_cc=round((self.moy_pond_cc/total_heures_cc),1)
         self.moy_pond_ccnc=round((self.moy_pond_ccnc/total_heures_ccnc),1)
     #
     #
     def fct_total_heures_echec(self): 
         """Cette fonction calcule, pour un eleve:
          => le nombre d'heures de cours certificatifs en échec,
          => le nombre d'heures de cours non-certificatifs en échec,
          => le nombre total d'heures de cours en échec."""
         for cours in self.grille_horaire.itervalues():
             if (cours.ccnc==True) & (cours.evaluation==1):
                 self.heures_echec_cc+=cours.heures
             if (cours.ccnc==False) & (cours.evaluation==1):
                 self.heures_echec_nc+=cours.heures
         if (self.heures_echec_cc!=0) & (self.heures_echec_nc==0):
             self.heures_echec_tot=str(self.heures_echec_cc)
         elif (self.heures_echec_nc!=0):
             self.heures_echec_tot=str(self.heures_echec_cc)+' +('+str(self.heures_echec_nc)+')'
         elif (self.heures_echec_cc==0) & (self.heures_echec_nc==0) :
             self.heures_echec_tot='0'
     #
     #
     def fct_cours_verrou_echec(self):
         """Cette fonction calcule, pour un eleve:
           => le nom des cours verrou en échec,
           => le nombre de cours verrou en échec"""
         liste_cours_verrou=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.verrou==True) & (cours.evaluation==1):
                 liste_cours_verrou.append(cours.intitule)
         self.liste_cours_verrou_echec=", ".join(liste_cours_verrou)
         self.nb_cours_verrou_echec=len(liste_cours_verrou)
     #
     #
     def fct_echec_inf35(self):
         """Cette fonction calcule, pour un eleve:
           => le nom des cours dont la cote est inférieure à 35,
           => le nombre de cours dont la cote est inférieure à 35."""
         liste_cours_inf35=[]
         for cours in self.grille_horaire.itervalues():
             if cours.points!=False:
                 if (cours.points<35) & (cours.ccnc==True):
                     liste_cours_inf35.append(cours.intitule)
         self.liste_cours_inf35=", ".join(liste_cours_inf35)
         self.nb_cours_inf35=len(liste_cours_inf35)
     #
     #
     def fct_nb_cours_echec(self):
         """Cette fonction calcule, pour un eleve:
           => le nombre de cours certificatifs en échec,
           => le nombre de cours non-certificatifs en échec."""
         for cours in self.grille_horaire.itervalues():
             if (cours.evaluation==1) & (cours.ccnc==True):
                 self.nb_cours_cc_echec+=1
             if (cours.evaluation==1) & (cours.ccnc==False) & (cours.pseudo==False):
                 self.nb_cours_nc_echec+=1
     #
     #
     def fct_echec_contrat(self):
         liste_echec_contrat=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.contrat==True) & (cours.evaluation==1):
                 liste_echec_contrat.append(cours.intitule)
         self.liste_echec_contrat=", ".join(liste_echec_contrat)
     #
     #
     def fct_certif_med(self):
         liste_certif_med=[]
         for cours in self.grille_horaire.itervalues():
             if cours.certif_med==True:
                 liste_certif_med.append(cours.intitule)
         self.liste_certif_med=", ".join(liste_certif_med)
     #
     #
     def fct_oubli_cours(self):
         liste_oubli_cours=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.evaluation==0) & (cours.option==False) & (cours.certif_med==False):
                 liste_oubli_cours.append(cours.intitule)
         self.liste_oubli_cours=", ".join(liste_oubli_cours)
     #
     #
     def fct_credits_inf_50(self):
         ecart=0
         ecart_pondere=0
         for cours in self.grille_horaire.itervalues():
             if (cours.points!=False) & (cours.ccnc==True): 
                 if(int(cours.points)<50):
                     ecart=50-(int(cours.points))
                     ecart_pondere=ecart*(cours.heures)
                     self.credits_inf_50+=ecart_pondere
     #
     #
     def fct_echec_travail(self):
         liste_echec_travail=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.evaluation==1) & (cours.echec_travail==True) : 
                 liste_echec_travail.append(cours.intitule)
         self.liste_echec_travail=", ".join(liste_echec_travail)
     #
     #
     def fct_classement_cours(self):
         self.classement_cours={}
         liste_35_50=[]
         liste_50_60=[] 
         liste_60_70=[]
         liste_70_80=[]
         liste_inf35=[] 
         liste_sup80=[]
         for cours in self.grille_horaire.itervalues():
             if cours.points!=False:
                 if (cours.points<35):
                     liste_inf35.append(cours.abr.lower()+" : "+str(cours.points))
                 elif 35 <= cours.points < 50:
                     liste_35_50.append(cours.abr.lower()+" : "+str(cours.points))
                 elif 50 <= cours.points < 60:
                     if cours.echec_force==True:
                         liste_50_60.append(cours.abr.lower()+" : "+str(cours.points)+"!")
                     else:
                         liste_50_60.append(cours.abr.lower()+" : "+str(cours.points))
                 elif 60 <= cours.points < 70 :
                     if cours.echec_force==True:
                         liste_60_70.append(cours.abr.lower()+" : "+str(cours.points)+"!")
                     else:
                         liste_60_70.append(cours.abr.lower()+" : "+str(cours.points))
                 elif 70 <= cours.points <80 :
                         if cours.echec_force==True:
                             liste_70_80.append(cours.abr.lower()+" : "+str(cours.points)+"!")
                         else:
                             liste_70_80.append(cours.abr.lower()+" : "+str(cours.points))
                 elif cours.points>=80 :
                     if cours.echec_force==True:
                         liste_sup80.append(cours.abr.lower()+" : "+str(cours.points)+"!")
                     else:
                         liste_sup80.append(cours.abr.lower()+" : "+str(cours.points))
         self.classement_cours['0=>35[']=" ; ".join(liste_inf35)
         self.classement_cours['35=>50[']=" ; ".join(liste_35_50)
         self.classement_cours['50=>60[']=" ; ".join(liste_50_60)
         self.classement_cours['60=>70[']=" ; ".join(liste_60_70)
         self.classement_cours['70=>80[']=" ; ".join(liste_70_80)
         self.classement_cours['80=>100]']=" ; ".join(liste_sup80)
     #
     def fct_age(self):
         
         if isinstance(self.ddn, datetime):
             self.ddn=self.ddn.date()
             #self.ddn=datetime.strptime(self.ddn, '%d/%m/%Y').date()
             
         elif isinstance(self.ddn, date):
                 self.ddn=self.ddn.date()
         else:
             pass
         
         age=date.today()-self.ddn
         mois=age.days/30
         self.age_str=str(mois/12)+' ans '+str(mois % 12)+' mois'
         self.age=float(mois)/12
     #    
     def fct_sciences6 (self):
         if self.grille_horaire['sc_6'].evaluation==4:
             #si le cours de sc6 est évalué de manière certificative
             nb_echecs=0
             nb_echecs_inf45=0
             self.grille_horaire['sc_6'].points=(self.grille_horaire['bio'].points+self.grille_horaire['chim'].points+self.grille_horaire['phys'].points)/3 # calcul de la moyenne pour sc6 
             
             if self.grille_horaire['bio'].points<50 : nb_echecs+=1
             if self.grille_horaire['chim'].points<50 : nb_echecs+=1
             if self.grille_horaire['phys'].points<50 : nb_echecs+=1
             if self.grille_horaire['bio'].points<45 : nb_echecs_inf45+=1
             if self.grille_horaire['chim'].points<45 : nb_echecs_inf45+=1
             if self.grille_horaire['phys'].points<45 : nb_echecs_inf45+=1
             if self.grille_horaire['sc_6'].points<50:
                 self.grille_horaire['bio'].echec_force=True
                 self.grille_horaire['chim'].echec_force=True
                 self.grille_horaire['phys'].echec_force=True
             if nb_echecs_sc>1 :
                 self.grille_horaire['bio'].echec_force=True
                 self.grille_horaire['chim'].echec_force=True
                 self.grille_horaire['phys'].echec_force=True
             if nb_echecs_inf45>0 :
                 self.grille_horaire['bio'].echec_force=True
                 self.grille_horaire['chim'].echec_force=True
                 self.grille_horaire['phys'].echec_force=True
    
#
#
class Cours(Eleve):
     #
     def __init__(self):
         self.points=False
         self.appreciation=False
         self.certif_med=False
         self.evaluation=0
         self.contrat=False
         self.echec_force=False
         self.echec_travail=False
         self.pseudo=False
         self.ccnc=False
         self.heures=0
         self.intitule=''
         self.abr=''
         self.verrou=False
         self.option=False
     #
     def analyse_points(self,points):
         if "#" in points:
             self.contrat=True
             points_eleve=points.replace('#','')
         if "!" in points:  
             self.echec_force=True
             self.evaluation=1
             points=points.replace('!','')
         if "@" in points:
             self.echec_travail=True
             points=points.replace('@','')
         if  points=='False': #les points ont été convertis en str avant d'être passés à cette fonction
             pass
         elif points.lower()=='cm':
             self.evaluation=4
             self.certif_med=True
         elif points.lower()=='x':#utile nottament pour les sc6 en 5°et6°
             self.evaluation=4
         elif points.lower()=='r':
             self.appreciation='r'
             self.evaluation=3
         elif points.lower()=='f':
             self.appreciation='f'
             self.evaluation=2
         elif points.lower()=='e':
             self.appreciation='e'
             self.evaluation=1
         else:
             points=points.replace(',','.')
             points=NettoiePoints(points).points# rappel: la fonction nettoie_point converti également les points en float
             self.points=points
             if points<50:
                 self.evaluation=1
             elif (points>=50) & (points<60) & (self.echec_force==False):
                 self.evaluation=2
             elif (points>=60) & (self.echec_force==False):
                 self.evaluation=3
             else:
                 pass
#
#
class Odf_file():
     """Cet objet permet de gérer tout ce qui concerne la production des documents odf : analyse détaillée, tableau récapitulatif et classement des élèves."""
     def __init__(self, doc_type="",titre="",path="",file_name=""):
         self.doc_type=doc_type
         
         if self.doc_type=='tableau_recap':
             self.document= odf_new_document('spreadsheet')
             self.insert_ods_styles()
             print "Création du tableau récapitulatif"
         #
         if self.doc_type=='analyse':
             self.document= odf_new_document('text')
             self.insert_odt_styles()
             print "Création du document d'analyse"
         #
         if self.doc_type=='classement':
             pass
         #
         if (self.doc_type!='tableau_recap') & (self.doc_type!='analyse'):
             print "Le type de document demandé n'est pas valide."
         #
         self.body = self.document.get_body()
         self.titre=titre
         self.path=path
         self.file_name=file_name
     #
     #
     def insert_odt_styles(self):
         #
         border = make_table_cell_border_string(thick = '0.5pt', color = 'black')
         style_ligne_inserer=odf_create_style('table-row', name='style_ligne', display_name='style_ligne')
         style_ligne_inserer.set_properties(properties={'style:min-row-height':'0.7cm'})
         self.document.insert_style(style_ligne_inserer,automatic=True)
         #
         self.document.insert_style(odf_create_style\
         ('table-cell',name='style_cell',display_name='style_cell', border=border),automatic=True)
         #
         tit_doc=odf_create_style('paragraph',name='tit_doc',display_name='tit_doc', area='text',size='24pt',weight='bold')
         tit_doc.set_properties(properties={'fo:text-align':'center'})
         self.document.insert_style(tit_doc,automatic=True)
         #
         self.document.insert_style(odf_create_style\
         ('paragraph',name='tit_table',display_name='tit_table', area='text',size='12pt',weight='bold'))
         #
         self.document.insert_style(odf_create_style\
         ('paragraph',name='tit_ligne',display_name='tit_ligne', area='text',size='11pt',style='italic'))
         #
         self.document.insert_style(odf_create_style\
         ('paragraph',name='echec_admis',display_name='echec_admis', area='text',size='11pt',color='#ff7e0e'))
         #
         self.document.insert_style(odf_create_style\
         ('paragraph',name='echec_non_admis',display_name='echec_non_admis', area='text', size='11pt',color='#ff000e'))
         #
         self.document.insert_style(odf_create_style\
         ('paragraph',name='non_echec',display_name='non_echec', area='text',size='11pt',color='#078018'))
         #
         self.document.insert_style(odf_create_style\
         ('paragraph',name='remarque',display_name='remarque', area='text',size='11pt'))
         #
         self.document.insert_style(odf_create_style\
         ('paragraph',name='petit',display_name='petit', area='text',size='9pt'))
         #
         style_table_inserer=odf_create_style\
         ('table',name='style_table',display_name='style_table',together='always')
         style_table_inserer.set_properties(properties={'style:may-break-between-rows':'false'})
         self.document.insert_style(style_table_inserer,automatic=True)
     #
     #
     def insert_ods_styles(self): 
         style=odf_create_style('table-row', name='style_ligne',height='1cm')
         self.document.insert_style(style,automatic=True)
         #
         style_cell = odf_create_element(u'<style:style style:name="titre" style:display-name="titre" style:family="table-cell"><style:table-cell-properties  fo:border="0.05pt solid #000000" style:vertical-align="middle"/><style:paragraph-properties fo:text-align="center"/><style:text-properties style:font-name="Sans" fo:font-size ="18pt"/></style:style>')
         self.document.insert_style(style_cell, automatic = True)
         #
         style_cell = odf_create_element(u'<style:style style:name="neutre" style:display-name="neutre" style:family="table-cell"><style:table-cell-properties  fo:border="0.05pt solid #000000" style:vertical-align="middle"/><style:paragraph-properties fo:text-align="center"/><style:text-properties style:font-name="Sans" fo:font-size ="12pt"/></style:style>')
         self.document.insert_style(style_cell, automatic = True)
         #
         style_cell = odf_create_element(u'<style:style style:name="reussite" style:display-name="reussite" style:family="table-cell"><style:table-cell-properties  fo:border="0.05pt solid #000000" style:vertical-align="middle"/><style:paragraph-properties fo:text-align="center"/><style:text-properties fo:color="#078018" style:font-name="Sans" fo:font-size ="12pt"/></style:style>')
         self.document.insert_style(style_cell, automatic = True)
         #
         style_cell = odf_create_element(u'<style:style style:name="faible" style:display-name="faible" style:family="table-cell"><style:table-cell-properties fo:border="0.05pt solid #000000" style:vertical-align="middle" /><style:paragraph-properties fo:text-align="center" /><style:text-properties fo:color="#ff7e0e" style:font-name="Sans" fo:font-size="12pt"/></style:style>')
         self.document.insert_style(style_cell, automatic = True)
         #
         style_cell = odf_create_element(u'<style:style style:name="echec" style:display-name="echec" style:family="table-cell"><style:table-cell-properties fo:border="0.05pt solid #000000" style:vertical-align="middle"/><style:paragraph-properties fo:text-align="center"/><style:text-properties fo:color="#ff000e" style:font-name="Sans" fo:font-size ="12pt"/></style:style>')
         self.document.insert_style(style_cell, automatic = True)
         #
         style_cell = odf_create_element(u'<style:style style:name="noms" style:display-name="noms" style:family="table-cell" ><style:table-cell-properties fo:border="0.05pt solid #000000" style:vertical-align="middle" /><style:paragraph-properties fo:text-align="start"/><style:text-properties fo:color="#000000" style:font-name="Sans" fo:font-size="11pt" fo:hyphenate="true" fo:wrap-option="wrap"/></style:style>')
         self.document.insert_style(style_cell, automatic = True)
         #
         style_cell = odf_create_element(u'<style:style style:name="titre" style:display-name="titre" style:family="table-cell"><style:table-cell-properties fo:border="0.05pt solid #000000" style:vertical-align="middle"/><style:paragraph-properties fo:text-align="center"/><style:text-properties style:font-name="Sans" fo:font-size ="18pt"/></style:style>')
         self.document.insert_style(style_cell, automatic = True)
         #
         style= odf_create_element(u'<style:page-layout style:name="mon_layout"><style:page-layout-properties fo:page-width="29.7cm" fo:page-height="21.001cm" style:print-orientation="landscape" fo:margin="1cm"></style:page-layout-properties></style:page-layout>')
         self.document.insert_style(style, automatic = True)
         #
         style= odf_create_element(u'<style:master-page style:name="paysage" style:display-name="paysage" style:page-layout-name="mon_layout"></style:master-page>')
         self.document.insert_style(style, automatic = True)
         #
         self.document.insert_style(odf_create_style\
         ('table-cell',name='cell_echec_non_admis',display_name='cell_echec_non_admis',\
         background_color='#ff000e'),automatic=True)
         #
         self.document.insert_style(odf_create_style\
         ('table-cell',name='cell_echec_admis',display_name='cell_echec_admis',\
         background_color='#ff7e0e'),automatic=True)
         #
         self.document.insert_style(odf_create_style\
         ('table-cell',name='cell_non_echec',display_name='cell_non_echec',\
         background_color='#078018',width='3cm'),automatic=True)
         #
         self.document.insert_style(odf_create_style\
         ('table-cell',name='cell_non_delib',display_name='cell_non_delib',\
         background_color='#919191'),automatic=True)
         #
         style=odf_create_style('table',name='ma_table')
         style.set_attribute('style:master-page-name','paysage')
         self.document.insert_style(style,automatic=True)
     #
     #
     def creer_ligne(self,table, entete, cellule, remarque, style):
         #
         if type(remarque) is not unicode:
             remarque=unicode(remarque,'utf-8')
         if type(entete) is not unicode:
             entete=unicode(entete,'utf-8')
         ligne=odf_create_row(style='style_ligne')
         cellule_entete=odf_create_cell(style='style_cell')
         cellule_entete.set_attribute('table:number-columns-spanned','2')
         cellule_sans_rem=odf_create_cell(style='style_cell')
         cellule_sans_rem.set_attribute('table:number-columns-spanned','2')
         cellule_rem=odf_create_cell(style='style_cell')
         cellule_rem.set_attribute('table:number-columns-spanned','2')
         text_entete=odf_create_paragraph(entete,style='tit_ligne')
         text_remarque=odf_create_paragraph(remarque,style=None)
         cellule_entete.append(text_entete)
         ligne.append(cellule_entete)
         #
         if cellule==1:
             if style!=None:
                 text_remarque.set_style('non_echec')
             else:
                 text_remarque.set_style('echec_admis')
             cellule_rem.append(text_remarque)
             ligne.append(cellule_rem)
             ligne.append(cellule_sans_rem)
         
         if cellule==2:
             ligne.append(cellule_sans_rem)
             text_remarque.set_style('echec_non_admis')
             cellule_rem.append(text_remarque)
             ligne.append(cellule_rem)
         
         table.append(ligne)
         return table
     #
     #
     def creer_ligne_2cell(self,table, entete, remarque):
         #
         if type(remarque) is not unicode:
             remarque=unicode(remarque,'utf-8')
         if type(entete) is not unicode:
             entete=unicode(entete,'utf-8')
         #
         ligne=odf_create_row(style='style_ligne')
         cellule_entete=odf_create_cell(style='style_cell')
         cellule_entete.set_attribute('table:number-columns-spanned','2')
         #
         cellule_rem=odf_create_cell(style='style_cell')
         cellule_rem.set_attribute('table:number-columns-spanned','4')
         #
         text_entete=odf_create_paragraph(entete,style='tit_ligne')
         text_remarque=odf_create_paragraph(remarque,style='remarque')
         #
         cellule_entete.append(text_entete)
         ligne.append(cellule_entete)
         cellule_rem.append(text_remarque)
         ligne.append(cellule_rem)
         table.append(ligne)
         return table
     #
     #
     def creer_resume_points(self,table, dico):
     #
         ligne_niv2_entetes=odf_create_row()
         ligne_niv2_points=odf_create_row()
         cellule_vide=odf_create_cell(style='style_cell')
         liste_categorie = dico.keys()
         liste_categorie.sort()
         #
         for categorie in liste_categorie:
             if type (categorie) is not unicode:
                 categorie=unicode(categorie,'utf-8')
             if type (dico[categorie]) is not unicode:
                 dico[categorie]=unicode(dico[categorie],'utf-8')
             cell_niv2_entete=odf_create_cell(style='style_cell')
             cell_niv2_points=odf_create_cell(style='style_cell')
             #
             #print categorie, type (categorie),unicode(categorie,'utf-8')
             #print unicode(categorie,'utf-8')
             txt_cell_niv2_entete=odf_create_paragraph(categorie,style='petit')
             txt_cell_niv2_points=odf_create_paragraph(dico[categorie],style='petit')
             #
             cell_niv2_entete.append(txt_cell_niv2_entete)
             cell_niv2_points.append(txt_cell_niv2_points)
             #
             ligne_niv2_entetes.append(cell_niv2_entete)
             ligne_niv2_points.append(cell_niv2_points)
         #
         table.append(ligne_niv2_entetes)
         table.append(ligne_niv2_points)
         return table
     #
     #
     def creer_ligne_entete(self,table, remarque):
         if type(remarque) is not unicode:
             remarque=unicode(remarque,'utf-8')
         #
         ligne=odf_create_row(style='style_ligne')
         cellule_entete=odf_create_cell(style='style_cell')
         cellule_vide=odf_create_cell()
         cellule_entete.set_attribute('table:number-columns-spanned','6')
         text_entete=odf_create_paragraph(remarque,style='tit_table')
         cellule_entete.append(text_entete)
         ligne.append(cellule_entete)
         #
         for i in xrange(5):
             ligne.append(cellule_vide)
         table.append(ligne)
         return table
     #
     #
     def analyse_eleve(self):
         #
         self.body.append(odf_create_paragraph(self.titre,style='tit_doc'))
         for nom_eleve in sorted(classe.liste_eleves,key=cmp_to_key(compfr)):
             eleve=classe.carnet_cotes[nom_eleve]
             nom_table=nom_eleve.replace("'",'')
             table=odf_create_table(nom_table,style='style_table')
             remarque=' ('+str(eleve.vol_horaire_ccnc )+'p./sem)'
             if ((eleve.situation_globale==1) or (eleve.situation_globale==4)) & (eleve.age_str!=False):
                 remarque+=' '+eleve.age_str
             table=self.creer_ligne_entete(table,nom_eleve+remarque)
             #
             if eleve.eval_certif ==True:
                 table=self.creer_resume_points(table,eleve.classement_cours )
             #
             if eleve.heures_echec_cc > classe.criteres.heures_echec_max:
                 table=self.creer_ligne(table, 'Total heures échec',2,eleve.heures_echec_tot ,None)
             if (eleve.heures_echec_cc <=classe.criteres.heures_echec_max) & (eleve.heures_echec_tot !='0'): 
                 #heures_echec_tot est une chaine de caractères
                 table=self.creer_ligne(table, 'Total heures échec',1,eleve.heures_echec_tot ,None)
             #
             if eleve.nb_cours_verrou_echec > classe.criteres.cours_verrou_echec_max:
                 table=self.creer_ligne(table,"Nb cours verrou échec", 2,eleve.liste_cours_verrou_echec ,None)
             if (eleve.nb_cours_verrou_echec >0) & (eleve.nb_cours_verrou_echec < classe.criteres.cours_verrou_echec_max):
                 table=self.creer_ligne(table, "Nb cours verrou échec", 1,eleve.liste_cours_verrou_echec ,None)
             #
             if (eleve.nb_cours_inf35 >0) & (eleve.nb_cours_cc_echec >classe.criteres.echec_sur_exclusion_max):
                 table=self.creer_ligne(table, "Cours inf. 35", 2,eleve.liste_cours_inf35 ,None)
             if (eleve.nb_cours_inf35 ==1) & (eleve.nb_cours_cc_echec ==1):
                 table=self.creer_ligne(table, "Cours inf. 35", 1,eleve.liste_cours_inf35 ,None)
             #
             if (eleve.moy_pond_cc <50) & (eleve.moy_pond_cc !=0):
                 table=self.creer_ligne(table, "Moyenne pond.", 2,str(eleve.moy_pond_cc ),None)
             elif (eleve.moy_pond_cc >=50) & (eleve.moy_pond_cc <60 ):
                 table=self.creer_ligne(table,"Moyenne pond.", 1,str(eleve.moy_pond_cc ),None)
             elif (eleve.moy_pond_cc >60):
                 table=self.creer_ligne(table,"Moyenne pond.", 1,str(eleve.moy_pond_cc ),'non_echec')
             else:
                 pass
             #
             if (eleve.liste_echec_contrat )!="":
                 table=self.creer_ligne_2cell(table,"Echec sur contrat",eleve.liste_echec_contrat )
             #
             if (eleve.pia )!=False:
                 table=self.creer_ligne_2cell(table,"Remarque","L'élève dispose d'un PIA" )
             if (eleve.ctg )!=False:
                 table=self.creer_ligne_2cell(table,"Remarque","L'élève dispose d'un contrat de travail global" )
             #
             if (eleve.liste_echec_travail )!="":
                 table=self.creer_ligne_2cell(table,"Prévoir contrat",eleve.liste_echec_travail )
             #
             if eleve.liste_certif_med != '':
                 table=self.creer_ligne_2cell(table,"Certificat médical", eleve.liste_certif_med)
             #
             if (eleve.liste_oubli_cours )!="":
                 table=self.creer_ligne_2cell(table,"Remarque", 'Pas de points en '+eleve.liste_oubli_cours )
             #
             #if (eleve.credit_pond_inf_50 )!="":
                 #table=creer_ligne_2cell(table,"Echec pondéré", str(eleve.credit_pond_inf_50 ))
             #
             self.body.append(odf_create_paragraph())
             self.body.append(table)
         #
         self.document.save(self.path+"/"+self.file_name+'_analyse.odt', pretty=True)
     #
     #
     def tableau_recap(self):
             table=odf_create_table(name='tableau_recap',style='ma_table')
             ligne=odf_create_row(style='style_ligne')
             cell=odf_create_cell(self.titre,style='titre')
             cell.set_attribute('table:number-columns-spanned',str(len(classe.liste_cours)+4))
             ligne.append(cell)
             table.append(ligne)
             #
             ligne=odf_create_row(style='style_ligne')
             #
             ligne.append(odf_create_cell("Cours",style='noms'))
             #
             for nom_cours in classe.liste_cours:
                 ligne.append(odf_create_cell(nom_cours,style='noms'))
             #
             ligne.append(odf_create_cell("Echecs",style='noms'))
             #
             ligne.append(odf_create_cell("Moy.",style='noms'))
             #
             ligne.append(odf_create_cell("Global",style='noms'))
             #
             table.append(ligne)
             #
             for eleve in sorted(classe.liste_eleves,key=cmp_to_key(compfr)):
                 ligne=odf_create_row(style='style_ligne')
                 ligne.append(odf_create_cell(eleve,style='noms'))
                 for nom_cours in classe.liste_cours:
                     #nom_cours=nom_cours.lower()
                     #points=classe.carnet_cotes[eleve].grille_horaire[nom_cours].points
                     if classe.carnet_cotes[eleve].grille_horaire[nom_cours].points!=False:
                         points=unicode(str(classe.carnet_cotes[eleve].grille_horaire[nom_cours].points),'utf-8')
                     elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].appreciation!=False:
                         points=unicode(classe.carnet_cotes[eleve].grille_horaire[nom_cours].appreciation,'utf-8')
                     elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].certif_med==True:
                         points='cm'
                     else:
                         points=unicode('','utf-8')
                     #print points, type(points)
                     if classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==0:
                         cell_points=odf_create_cell(points,style='neutre')
                     elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==1:
                         cell_points=odf_create_cell(points,style='echec')
                     elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==2:
                         cell_points=odf_create_cell(points,style='faible')
                     elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==3:
                         cell_points=odf_create_cell(points,style='reussite')
                     elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==4:
                         cell_points=odf_create_cell(points,style='neutre')
                     ligne.append(cell_points)
                 #
                 txt_heures_echec=unicode(str(classe.carnet_cotes[eleve].heures_echec_tot),'utf-8')+unicode(' / ','utf-8')\
                 +unicode(str(classe.carnet_cotes[eleve].vol_horaire_ccnc),'utf-8' )
                 ligne.append(odf_create_cell(txt_heures_echec,style='noms'))
                 #
                 txt=unicode(str(classe.carnet_cotes[eleve].moy_pond_cc ),'utf-8')
                 if classe.carnet_cotes[eleve].moy_pond_cc <50:
                     cell=odf_create_cell(txt,style='echec')
                 elif classe.carnet_cotes[eleve].moy_pond_cc <60:
                     cell=odf_create_cell(txt,style='faible')
                 else:
                     cell=odf_create_cell(txt,style='reussite')
                 ligne.append(cell)
                 #
                 cell_situation_globale=odf_create_cell()
                 if classe.carnet_cotes[eleve].situation_globale ==3:
                     cell_situation_globale.set_style('cell_non_echec')
                 elif classe.carnet_cotes[eleve].situation_globale ==1:
                     cell_situation_globale.set_style('cell_echec_non_admis')
                 elif classe.carnet_cotes[eleve].situation_globale ==2:
                     cell_situation_globale.set_style('cell_echec_admis')
                 elif classe.carnet_cotes[eleve].situation_globale ==4:
                     cell_situation_globale.set_style('cell_non_delib')
                 ligne.append(cell_situation_globale)
                 #
                 table.append(ligne)
             self.body.append(table)
             self.document.save(self.path+"/"+self.file_name+'_tableau.ods', pretty=True)
     #
     #def classement(body, dico_remarques_classe):
         #classement_moy_pond=[]
         #for eleve,remarques in dico_remarques_classe.items():
           #nom_moy_pond=[]
           #nom_moy_pond.append(remarques['moy_pond'])
           #nom_moy_pond.append(eleve)
           #classement_moy_pond.append(nom_moy_pond)
         #table=odf_create_table(name='classement')
         #classement_moy_pond.sort()
         #for eleve in classement_moy_pond:
           #ligne=odf_create_row()
           #cell_moy=odf_create_cell()
           #cell_nom=odf_create_cell()
           #text_moy=odf_create_paragraph(unicode(str(eleve[0])))
           #text_nom=odf_create_paragraph(eleve[1])
           #cell_moy.append(text_moy)
           #cell_nom.append(text_nom)
           #ligne.append(cell_nom)
           #ligne.append(cell_moy)
           #table.append(ligne)
         #body.append(odf_create_paragraph())
         #body.append(table)
         ##
         #table=odf_create_table(name='essai')
         #colonne=odf_create_column(repeated=(4),style='style_colonne')
         #table.append(colonne)
         #ligne=odf_create_row()
         #ligne.append(odf_create_cell(style="cell_non_echec"))
         ##
         #table.append(ligne)
         #body.append(table)
         ##
         #return(body)

#
#
class Criteres(Classe):
     #
     def __init__(self):
         self.heures_echec_max=0
         self.cours_verrou_echec_max=0
         self.echec_sur_exclusion_max=0
#
class NettoiePoints(object):
     def __init__(self,points=''):
         self.points=points
         
         chaine = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','.',',']
         self.points = [val for val in self.points if val in chaine]
         self.points=''.join(self.points)
         if self.points=='':
             self.points=False
         if self.points!=False:
             self.points=float(self.points)
             if self.points!=int(self.points):
                 self.points=round(self.points,1)
             else :
                 self.points=int(self.points)
#
#
class OldGui(QDialog):
     def __init__(self, parent=None):
         super(Gui, self).__init__(parent)
         clipboard = QApplication.clipboard()
         text=clipboard.text()
         text=text.split('\n')
         for ligne in text:
             print ligne.toUtf8()
#
#
if __name__=="__main__":
     compfr=Compfr()
     classe=Classe()
     app = QApplication(sys.argv)
     gui=Gui()
     gui.show()
     app.exec_()
     
# vérifier comment les points sont encodés, cad : il ne faudra créer le cours chez l'élève que si il y a effectivement des points
# fait mais il faudrait revoir la cohérence des noms de cours entre le tableau et le fichier xml
