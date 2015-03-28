#! /usr/bin/python3
# -*- coding: utf-8 -*- 

from xml.dom.minidom import parse
import locale
import os
import time
from os import path
from types import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSvg import *
from PyQt4.QtWebKit import QGraphicsWebView
import sys
import traceback
from datetime import date , datetime
#from datetime import *
#import types
from functools import cmp_to_key 
import xml.etree.ElementTree as ET
import subprocess
import platform 
from math import radians, sin, cos,floor
import urllib
import csv
import getpass
#import re, urllib
import urllib.request
import random

class Gui(QMainWindow):
    
     def __init__(self):
         super(Gui, self).__init__()
         #self.initUI()
         #self.file_to_open=QLineEdit("Sélectionnez le fichier.")
         self.tableau_valide=False
         
         new_from_fileAction = QAction(QIcon('./icons/import_file.svg'),"&Importer les points à partir d'un fichier", self)
         new_from_fileAction.setShortcut('Ctrl+I')
         new_from_fileAction.setStatusTip("Importer les points directement à partir d'un fichier")
         new_from_fileAction.triggered.connect(self.select_file)
         
         new_from_clipboardAction = QAction(QIcon('./icons/editpaste.png'),"Importer les points à partir du &presse papier", self)
         new_from_clipboardAction.setShortcut('Ctrl+V')
         new_from_clipboardAction.setStatusTip("Importer les points à partir de données copiées depuis un fichier")
         new_from_clipboardAction.triggered.connect(self.import_clipboard)
         
         new_from_downloadAction = QAction(QIcon('./icons/download_file.svg'),"Télécharger les points à partir de Google Drive", self)
         new_from_downloadAction.setShortcut('Ctrl+D')
         new_from_downloadAction.setStatusTip("Télécharger les points à partir de Google Drive")
         new_from_downloadAction.triggered.connect(self.dialog_import_download)
         
         StartAction = QAction(QIcon('./icons/ok_apply.svg'),"Démarrer l'analyse", self)
         StartAction.setShortcut('Ctrl+D')
         StartAction.setStatusTip("Démarrer")
         StartAction.triggered.connect(self.verif_avant_analyse)
         
         QuitAction = QAction(QIcon('./icons/quit.svg'),"Quitter", self)
         QuitAction.setShortcut('Ctrl+Q')
         QuitAction.setStatusTip("Quitter")
         QuitAction.triggered.connect(self.appExit)
         
         HelpAction = QAction(QIcon('./icons/help.svg'),"Obtenir de l'aide", self)
         HelpAction.setStatusTip("Obtenir de l'aide concernant l'utilisation de ce logiciel")
         HelpAction.triggered.connect(self.aide)
         
         AboutAction = QAction(QIcon('./icons/odego.svg'),"À propos", self)
         AboutAction.setStatusTip("A propos de ce logiciel")
         AboutAction.triggered.connect(self.about)
         
         menubar = self.menuBar()
         
         fileMenu = menubar.addMenu("&Application")
         fileMenu.addAction(StartAction)
         fileMenu.addAction(QuitAction)
         
         fileMenu = menubar.addMenu("&Importer")
         fileMenu.addAction(new_from_fileAction)
         fileMenu.addAction(new_from_clipboardAction)
         fileMenu.addAction(new_from_downloadAction)
         
         fileMenu = menubar.addMenu("&Aide")
         fileMenu.addAction(HelpAction)
         fileMenu.addAction(AboutAction)
         
         self.toolbar = self.addToolBar('Toolbar')
         self.toolbar.addAction(new_from_fileAction)
         self.toolbar.addAction(new_from_clipboardAction)
         self.toolbar.addAction(new_from_downloadAction)
         self.toolbar.addAction(QuitAction)
         #self.toolbar.addAction(StartAction)
         
         self.statusBar()
         
         #self.setGeometry(300, 300, 300, 200)
         self.setWindowTitle('Odego')
         self.center()
         self.setWindowIcon(QIcon('./icons/odego.svg')) 
         
         niveau=['','1', '2', '3', '4', '5', '6']
         classes=['','-','a','b','c','d','e','f','g','h','i','j','k','l','m','z !?!?']
         sections=['','GT','TQ']
         delibe=['Noel','Mars','Juin','Sept.']
         now=date.today()
         annees=[str(now.year-2),str(now.year-1),str(now.year),str(now.year+1),str(now.year+2)]
         #
         grid=QGridLayout()
         widget=QWidget()
         widget.setLayout(grid)
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
         logDockWidget=QDockWidget(self)
         logDockWidget.setTitleBarWidget(QLabel( '<p style="font-size:10pt;font-weight:bold">Informations</p>' ))
         logDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
         logDockWidget.setFeatures(QDockWidget.DockWidgetFloatable)
         #logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
         logDockWidget.setWidget(widget)
         logDockWidget.setMaximumWidth(200)
         self.addDockWidget(Qt.LeftDockWidgetArea,logDockWidget)
         #
         self.radio_tab_recap=QCheckBox("Tableau récapitulatif")
         self.radio_tab_recap.setToolTip ('<p>Produire un tableau récapitulatif "classique" avec la sitation globale, la moyenne pondérée et le nombre d\' heures d\'échec.</p>')
         self.radio_tab_recap.setCheckState(2)
         self.radio_ana_det=QCheckBox("Analyse detaillée")
         self.radio_ana_det.setToolTip (('<p>Produire un fichier présentant pour chaque élève les détails de ses résultats et les raisons d\' un éventuel échec.</p>'))
         self.radio_ana_det.setCheckState(2)
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
         logDockWidget=QDockWidget(self)
         logDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
         logDockWidget.setFeatures(QDockWidget.DockWidgetFloatable)
         logDockWidget.setTitleBarWidget(QLabel( '<p style="font-size:10pt;font-weight:bold">Analyses</p>' ))
         #logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
         logDockWidget.setWidget(widget)
         logDockWidget.setMaximumWidth(200)
         self.addDockWidget(Qt.LeftDockWidgetArea,logDockWidget)
         #
         self.boutton_ok=QPushButton(QIcon('./icons/ok_apply.svg'),'Démarrer')
         self.boutton_ok.setMinimumHeight(40)
         self.connect(self.boutton_ok, SIGNAL("clicked()"),self.verif_avant_analyse)
         
         logDockWidget=QDockWidget(self)
         logDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
         #logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
         logDockWidget.setWidget(self.boutton_ok)
         logDockWidget.setMaximumWidth(200)
         self.addDockWidget(Qt.LeftDockWidgetArea,logDockWidget)
         
         self.setWindowTitle('Odego : un guide pour les délibérations')
         self.combo_annees.setCurrentIndex(2)
         if now.month in [10,11,12,1]:
             self.combo_delib.setCurrentIndex(0)
         if now.month in [2,3,4]:
             self.combo_delib.setCurrentIndex(1)
         if now.month in [5,6,7,8,9]:
             self.combo_delib.setCurrentIndex(2)
         self.current_dir = path.expanduser("~")
     #
     def splashscreen(self):
         
         svg_rend = QSvgWidget()     
         svg_rend.setWindowFlags(Qt.SplashScreen)
         for i in range(101):
             blanc=str(int(255-float(i)/100*255))
             gris=str(int(181-float(i)/100*181))
             svg_txt='<svg width="550px" height="290px">'
             svg_txt+='<defs>'
             svg_txt+='<linearGradient id="grad1" x1="0" y1="0" x2="0" y2="100%">'
             svg_txt+='<stop style="stop-color:#ffffff;stop-opacity:1;" offset="0" />'
             svg_txt+='<stop style="stop-color:#b5b5b5;stop-opacity:1;" offset="1"/>'
             svg_txt+='</linearGradient>'
             svg_txt+='<linearGradient id="grad2" x1="0%" y1="-10%" x2="0" y2="300%">'
             svg_txt+='<stop style="stop-color:rgb(%s,%s,%s);stop-opacity:1" offset="0" />'%(blanc,blanc,blanc)
             svg_txt+='<stop style="stop-color:rgb(%s,%s,%s);stop-opacity:1" offset="1"/>'%(gris,gris,gris)
             svg_txt+='</linearGradient>'
             svg_txt+='</defs>'
             svg_txt+='<rect height="290" width="550" fill="url(#grad1)"/>'
              
             if i<=25:
                 height=float(i)/25*66
                 y1=str(210-height)
                 y2=str(210+height)
                 taille_rouge=str(float(i))
                 stroke_rouge=str(2*6.5*(float(i)/100  ))
                 
                 svg_txt+='<line x1="68" y1="%s" x2="68" y2="%s" stroke="#000000" stroke-width="12"/>' %(y1,y2)
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="%s" stroke="#ffffff" stroke-width="%s" fill="#D30000" />' %(taille_rouge,stroke_rouge)
                 
             if 25<i<=50:
                 alpha=(float(i)-25)/25*90
                 alpha_rad=radians(alpha)
                 l1_x1=str(68-44*sin(alpha_rad))
                 l1_x2=str(68+88*sin(alpha_rad))
                 l1_y1=str(188-44*cos(alpha_rad))
                 l1_y2=str(188+88*cos(alpha_rad))
                 taille_rouge=str(float(i))
                 stroke_rouge=str(2*6.5*(float(i)/100  ))
                 
                 svg_txt+='<line x1="68" y1="144" x2="68" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000000" stroke-width="12"/>' %(l1_x1,l1_y1,l1_x2,l1_y2)
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="%s" stroke="#ffffff" stroke-width="%s" fill="#D30000" />' %(taille_rouge,stroke_rouge)
                
             if 50<i<=75:
                 alpha=(float(i)-50)/25*90
                 alpha_rad=radians(alpha)
                 l2_x1=str(112-88*cos(alpha_rad))
                 l2_x2=str(112+44*cos(alpha_rad))
                 l2_y1=str(188+88*sin(alpha_rad))
                 l2_y2=str(188-44*sin(alpha_rad))
                 centre_x_orange=str(220+((float(i)-50)/25*125))
                    
                 svg_txt+='<line x1="68" y1="144" x2="68" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="24" y1="188" x2="156" y2="188" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000000" stroke-width="12"/>'%(l2_x1,l2_y1,l2_x2,l2_y2)
                 svg_txt+='<circle id="rond_orange" cx="%s" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#FF6E00" />'%(centre_x_orange)
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#D30000" />'
                 
             if i>75:
                 alpha=(float(i)-75)/25*90
                 alpha_rad=radians(alpha)
                 l3_x1=str(112-88*sin(alpha_rad))
                 l3_x2=str(112+44*sin(alpha_rad))
                 l3_y1=str(232-88*cos(alpha_rad))
                 l3_y2=str(232+44*cos(alpha_rad))
                 centre_x_vert=str(345+((float(i)-75)/25*125))
                    
                 svg_txt+='<line x1="68" y1="144" x2="68" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="24" y1="188" x2="156" y2="188" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="112" y1="144" x2="112" y2="276" stroke="#000000" stroke-width="12"/>'
                 svg_txt+='<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000000" stroke-width="12"/>' %(l3_x1,l3_y1,l3_x2,l3_y2)
                 svg_txt+='<circle id="rond_vert" cx="%s" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#078018" />' %(centre_x_vert)
                 svg_txt+='<circle id="rond_orange" cx="345" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#FF6E00" />'
                 svg_txt+='<circle id="rond_rouge" cx="220" cy="210" r="50" stroke="#ffffff" stroke-width="6.5" fill="#D30000" />'
         
             svg_txt+='<text style="font-size:130px;font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;text-align:center;text-anchor:middle;fill:url(#grad2);stroke:none;font-family:Sans" x="275" y="110" > ODEGO</text>'
             svg_txt+='</svg>'
             
             array=QByteArray(svg_txt)
             svg_rend.load(array)
             svg_rend.show()
             QApplication.processEvents()
             time.sleep(0.07)
         time.sleep(0.5)
         svg_rend.close()
     #
     def center(self):
         qr = self.frameGeometry()
         cp = QDesktopWidget().availableGeometry().center()
         qr.moveCenter(cp)
         self.move(qr.topLeft())
     #
     def test(self):
         print ('Hello World')
     #
     def aide(self):
         message=''
         message+="<div><p>Pour obtenir de l'aide conçernant l'emploi de ce logiciel "
         message+="vous pouvez contacter J.N. Gautier par téléphone à n'importe quelle heure "
         message+="décente.</p>"
         message+="<p>J.N. Gautier : <b>0494/84.14.59</b></p></div>"
         message+="<p>Ce service vous coûtera généralement un café.</p>"
         message+="<p>En cas d'utilisation du service d'aide en dehors des heures prévues, vous me serez redevable d'un bon sandwich pendant les délibés.</p>"
         message+="</div>"
         QMessageBox.information(self,'Aide',message)
     #
     def about(self):
         message='<div><p><b>Odego</b>, inspiré du grec <i>οδηγω : "je guide"</i>, est un outil '
         message+="d'aide à la décision pour les délibés. <br/>  Il permet de produire des tableaux récapitulatifs, des tableaux de classement et de situer chaque élève par rapport aux critères de réussite.</p> <p>Les fichiers sont produits aux formats tex et pdf.</p><p> <b>Auteur : </b> J.N. Gautier</p>  <p> <b>Language : </b> Python %s</p>  <p> <b>Interface : </b> Qt %s</p> <p> Merci à Noëlle qui a baptisé ce logiciel ainsi qu'à tous ceux dont les conseils ont permis d'en améliorer la qualité.</p> <p> Pour signaler un bug ou proposer une amélioration : <br/><a" %(platform.python_version(),QT_VERSION_STR)
         message+='href="mailto:gautier.sciences@gmail.com">gautier.sciences@gmail.com</a></p></div>'
         QMessageBox.about(self,"A propos d'odego",message)
         #self.dial_about=QTextBrowser()
         #self.dial_about.append(message)
         #self.dial_about.show()
     #
     def appExit(self):
         print ("Au revoir!")
         app.quit()
     #
     def select_file(self):
         self.file_name = QFileDialog.getOpenFileName(self,'Tableau avec les points de la classe.',self.current_dir)
         self.current_dir=os.path.dirname(self.file_name)
         self.get_file_ext()
         classe.__init__()
         # je réinitialise la classe au cas ou l'utilisateur tente d'importer un fichier de points alors que cela a déjà été fait
         #if self.ext=='ods':
             #self.import_ods()
         #elif self.ext=='xls':
             #self.import_xls()
         #elif self.ext=='xlsx':
             #self.import_xls()
         if self.ext=='txt':
             self.import_txt()
         elif self.ext=='tsv':
             self.import_txt()
         else:
             QMessageBox.warning(self,'Erreur',"Veuillez renseigner un fichier avec l'extension 'txt' ou 'tsv'.")
     #
     def get_file_ext(self):
         ext=self.file_name.split('.')
         self.ext=ext[len(ext)-1]
     #
     def import_txt(self):
         try:
             #QMessageBox.information(self,'Information',"<p>L'importation depuis un fichier txt ou tsv nécessite </p><p>que les valeurs soient séparées par des tabulations.</p>")
             myfile= open(self.file_name, "r")
             self.tableau_points=[]
             for ligne in myfile:
                 liste_ligne_points=ligne.rstrip('\n\r').split('\t')
                 ligne_points=[]
                 for elem in liste_ligne_points:
                     if (elem==('' or 'None')) or (len(elem)==0):
                         elem=False
                     ligne_points.append(elem)
                 self.tableau_points.append(ligne_points)
             self.fct_carnet_cote(self.tableau_points)
         except Exception as e:
             message="<p>Un problème majeur a été rencontré lors de l'importation du fichier.</p>"
             message+='<p>Veuillez signaler cette erreur au développeur.</p></div>'
             QMessageBox.critical(self,'Echec',message)
             print ('Erreur : %s' % e)
             print ('Message : ', traceback.format_exc())
     #
     def import_clipboard(self):
         pass
         
     #
     def dialog_import_download(self):
         
         classe,ok = QInputDialog.getItem(self,('Télécharger les points depuis Google Drive'),("Choisissez une classe"),['1 C a','1 C b','1 C c','1 C d','1 C e','1 C f','2 C a','2 C b','2 C c','2 C d','2 C e','3 GT a','3 GT b','3 GT c','3 GT d','3 GT e','3 TQ','4 GT a','4 GT b','4 GT c','4 TQ','5 GT a','5 GT b','5 GT c','5 TQ','6 GT a','6 GT b','6 GT c','6 TQ'],editable = False)
         classe=str(classe)
         niveau_classe=classe.split(' ')
         if niveau_classe[1]=='TQ':
             self.combo_section.setCurrentIndex(2)
             self.combo_classes.setCurrentIndex(1)
             self.combo_niveau.setCurrentIndex(int(niveau_classe[0]))
         else:
             self.combo_section.setCurrentIndex(1)
             self.combo_niveau.setCurrentIndex(int(niveau_classe[0]))
             liste=['a','b','c','d','e','f']
             pos=liste.index(niveau_classe[2])+2
             self.combo_classes.setCurrentIndex(pos)
         #
         #classe=niveau_classe[0]+niveau_classe[1]
         liste_liens={}
         myfile=open('./liens_tableaux_delibes.tsv', "r")
         #
         for ligne in myfile:
             liste_infos=ligne.rstrip('\n\r').split('\t')
             infos=Infos()
             infos.classe=liste_infos[0]
             infos.prof=liste_infos[1]
             infos.id_tab=liste_infos[2]
             liste_liens[infos.classe]= infos
         
         infos=liste_liens[classe]
         
         self.download(infos.id_tab,infos.classe)
             
     
     
     def download(self,spread_id,classe):
         #url_format = "https://docs.google.com/spreadsheets/export?id=%s&exportFormat=tsv " %(spread_id)
         #req = urllib2.Request(url_format)
         #directory='./decembre_2014/%s'%classe
         #if not os.path.exists(directory):
             #os.makedirs(directory)
         link='https://docs.google.com/spreadsheets/export?id=%s&exportFormat=tsv'%spread_id
         tsv=urllib.request.urlopen(link)
         reader=tsv.read().decode('utf-8')
         tableau=reader.split('\n')
         
         self.tableau_points=[]
         for ligne in tableau:
             liste_ligne_points=ligne.split('\t')
             ligne_points=[]
             for elem in liste_ligne_points:
                 if (elem==('' or 'None')) or (len(elem)==0):
                     elem=False
                 ligne_points.append(elem)
             self.tableau_points.append(ligne_points)
         self.fct_carnet_cote(self.tableau_points)
     #
     def fct_carnet_cote(self,tableau_points):
         classe.carnet_cotes={}
         classe.liste_cours=[]
         try:
             ligne_cours=False
             for ligne_points in tableau_points:
                 prem_cell=ligne_points[0]
                 if (prem_cell.lower()=='cours'):
                     ligne_cours=True
                     for cell in ligne_points:
                         if cell!=(False): #il peut y avoir des cellules vides qui suivent celles avec les intitulés des cours ; on ne prend en compte que les cellules non vides.
                             classe.liste_cours.append(cell.lower())
                     del classe.liste_cours[0]
             if ligne_cours==False:
                 raise ExceptionPasCours
         except ExceptionPasCours :
             QMessageBox.critical(self,'Echec',"<p>Il n'y a pas de ligne avec les cours dans votre fichier</p> <p>ou celle-ci n'est pas indiquée par le mot 'Cours'</p>")
         ##
         try:
             for ligne_points in tableau_points:
                 
                 prem_cell=ligne_points[0]
                 if (prem_cell==False) or ( (prem_cell[0]=='&') & (prem_cell[1]=='&')) or (prem_cell.lower()=='cours'):
                     # il peut y avoir des lignes vides en bas de tableau, cela justifie le test prem_cell==False
                     pass
                 else:
                     eleve=Eleve()
                     eleve.nom=ligne_points[0]
                     del ligne_points[0]
                     for cours,points_eleve in zip(classe.liste_cours,ligne_points):
                         #
                         if (cours.lower()=='pia') & (points_eleve!=False):
                             eleve.pia=True
                         #
                         elif (cours.lower()=='ctg') & (points_eleve!=False):
                             eleve.ctg=True
                         #
                         elif (cours.lower()=='ddn') & (points_eleve!=False):
                             eleve.ddn=points_eleve
                         #
                         elif (cours.lower()=='noel') & (points_eleve!=False):
                             eleve.noel=points_eleve
                         #
                         elif (cours.lower()=='mars') & (points_eleve!=False):
                             eleve.mars=points_eleve
                         #
                         elif points_eleve!=False:
                             eleve.grille_horaire[cours]=Cours()
                             eleve.grille_horaire[cours].analyse_points(str(points_eleve))
                             if eleve.grille_horaire[cours].points!=False:
                                 eleve.eval_certif=True
                         else : pass
                         print (eleve.nom , cours, points_eleve)
                     classe.carnet_cotes[eleve.nom]=eleve
         except Exception as e:
             message="<p>Un problème majeur a été rencontré lors de la création du modèle de tableau.</p>"
             message+='<p>Veuillez signaler cette erreur au développeur.</p></div>'
             QMessageBox.critical(self,'Echec',message)
             print ('Erreur : %s' % e)
             print ('Message : ', traceback.format_exc())
             #traceback.print_exc()
         if 'ddn' in classe.liste_cours:
             classe.liste_cours.remove('ddn')
             classe.ddn=True
         if 'ctg' in classe.liste_cours:
             classe.liste_cours.remove('ctg')
             classe.ctg=True
         if 'pia' in classe.liste_cours:
             classe.liste_cours.remove('pia')
             classe.pia=True
         if 'noel' in classe.liste_cours:
             classe.liste_cours.remove('noel')
             classe.noel=True
         if 'mars' in classe.liste_cours:
             classe.liste_cours.remove('mars')
             classe.mars=True
         classe.prod_liste_eleves()
         self.tableau_valide=True
         
         if self.tableau_valide==True:
             self.update_tableau_points_view()
     #
     #
     def update_tableau_points_view(self):
         try :
             self.table.setParent(None)
         except:
             pass
         self.table=QTableWidget()
         self.table.setEditTriggers(QTableWidget.NoEditTriggers)
         premier_elv=True
         for eleve in sorted(classe.liste_eleves,key=cmp_to_key(compfr)):
                 self.table.insertRow(self.table.rowCount())
                 j=0
                 for nom_cours in classe.liste_cours:
                     if premier_elv==True:
                         self.table.insertColumn(self.table.columnCount())
                     if nom_cours in classe.carnet_cotes[eleve].grille_horaire.keys():
                         points=classe.carnet_cotes[eleve].grille_horaire[nom_cours].points
                         appreciation=classe.carnet_cotes[eleve].grille_horaire[nom_cours].appreciation
                         if points!=False:
                             item= str(points)
                         elif appreciation!=False:
                             item= str(appreciation)
                         else:
                             item= ''
                     else :
                         item= ''
                     newitem = QTableWidgetItem(item)
                     self.table.setItem(self.table.rowCount()-1,j, newitem)
                     j+=1
                 premier_elv=False
         labels=classe.liste_cours
         self.table.setHorizontalHeaderLabels(labels)
         labels=sorted(classe.liste_eleves,key=cmp_to_key(compfr))
         self.table.setVerticalHeaderLabels(labels)
         self.setCentralWidget(self.table)
         self.showMaximized()
     
     def verif_avant_analyse(self):
         verif_param=True
         alert="<div><p> Veuillez renseigner :</p> <ul>"
         if self.combo_niveau.currentText()=='':
             verif_param=False
             alert+='<li>Le <b> niveau </b> de la classe.</li>'
         
         if self.combo_section.currentText()=='':
             verif_param=False
             alert+='<li>La <b> section </b> de la classe.</li>'
         if self.combo_classes.currentText()=='':
             verif_param=False
             alert+='<li>Le <b> nom </b> de la classe.</li>'
         
         if verif_param==False:
             alert+='</ul> </div>'
             QMessageBox.warning(self,'Informations manquantes',alert)
         
         if (self.radio_tab_recap.isChecked()==False) & (self.radio_ana_det.isChecked()==False) & (self.radio_classmt.isChecked()==False):
             message="<div><p>Aucune analyse n'a été demandée pour cette classe.</p>"
             message+="<p>N'oubliez pas de cocher les analyses souhaitées <b>avant de pousser sur démarrage</b>.</p> </div>"
             QMessageBox.information(self,"Aucune analyse demandée",message)
         
         if self.tableau_valide==False:
             alert="<div><p>Aucun point n'a encore été importé.</p>"
             alert+="<p> Veuillez importer des points <b>avant de pousser sur démarrage</b>.</p> </div>"
             QMessageBox.warning(self,'Points manquants',alert)
         if (self.tableau_valide==True) & (verif_param==True):
             self.pre_traitement()
         
     #
     def pre_traitement(self):
         print ("Pré-traitement des données")
         #self.fichier_a_traiter=self.fname
         self.creer_tableau_recap=self.radio_tab_recap.isChecked()
         self.creer_analyse_eleve=self.radio_ana_det.isChecked()
         self.creer_classement=self.radio_classmt.isChecked()
         #
         self.niveau=self.combo_niveau.currentText()
         self.section=self.combo_section.currentText()
         self.classe=self.combo_classes.currentText()
         self.annee=self.combo_annees.currentText()
         self.delibe=self.combo_delib.currentText()
         self.file2save=self.delibe+"_"+self.annee+"_"+self.niveau+self.section+self.classe
         self.titre='Conseil de classe '+self.niveau+self.section+self.classe+" - "+self.delibe+' '+self.annee
         #
         try:
             classe.set_param(self.niveau,self.section,self.delibe)
             classe.update_liste_cours()
         except Exception as e:
             QMessageBox.warning(self,'Erreur',"<div><p> Un problème a été rencontré lors du traitement de votre fichier</p>\
             <ul><li>Vérifiez que le fichier sélectionné contienne bien des <b>points</b>.</li>\
             <li>Vérifiez que le fichier sélectionné contienne bien le <b>nom des cours</b>.</li>\
             <li>Vérifiez que vous avez sélectionné la bonne <b>classe </b>et la bonne <b>section </b>dans le menu d'acceuil.</li></ul>\
             </div>")
             print ('Erreur : %s' % e)
             print ('Message : ', traceback.format_exc() )
         try:
             classe.stats_elv()
             classe.prod_situation_globale()
         except Exception as e:
             QMessageBox.critical(self,'Echec',"Une erreur a été rencontrée dans l'analyse des points")
             print ('Erreur : %s' % e)
             print ('Message : ', traceback.format_exc() )
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Latex_file(doc_type="analyse",titre=self.titre,file_name=self.file2save)
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Latex_file(doc_type="tableau_recap",titre=self.titre,file_name=self.file2save)
                 del tableau
             if self.creer_classement==True:
                 tableau=Latex_file(doc_type="classement",titre=self.titre,file_name=self.file2save)
                 del tableau
             QMessageBox.information(self,'Terminé',"Les données ont été traitées avec succès!")
         except Exception as e:
             QMessageBox.warning(self,'Erreur',"Un ou plusieurs documents demandés n'ont pas été produits")
             print ('Erreur : %s' % e)
             print ('Message : ', traceback.format_exc() )
     #
     #
     
class Infos():
     def __init__(self):
         self.classe=''
         self.prof=''
         self.id_tab=''
         
         
class ExceptionPasCours(Exception): pass
#
#
class Compfr(object):
     """Cette classe contient une unique fonction servant à comparer des chaines de caractères pour créer une classement alphabétique français"""
     # Solution prise sur : http://python.jpvweb.com/mesrecettespython/doku.php?id=tris_dictionnaire_francais
     def __init__(self):
         locale.setlocale(locale.LC_ALL, '')
         self.espinsec = '\xA0' # espace insécable
     #
     def __call__(self, v1, v2):
         # on retire les tirets, les blancs insécables et les apostrophes
         v1 = v1.replace('-','')
         v1 = v1.replace(self.espinsec,'')
         v1 = v1.replace("'",'')
         v1 = v1.replace(" ",'')
         #
         v2 = v2.replace('-','')
         v2 = v2.replace(self.espinsec,'')
         v2 = v2.replace("'",'')
         v2 = v2.replace(" ",'')
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
         self.analyse={}
         self.analyse['fct_points_sup_100']=0
         self.analyse['fct_moyenne_ponderee']=0
         self.analyse['fct_echec_inf35']=0
         self.analyse['fct_nb_heures_horaire']=0
         self.analyse['fct_total_heures_echec']=0
         self.analyse['fct_cours_verrou_echec']=0
         self.analyse['fct_nb_cours_echec']=0
         self.analyse['fct_echec_contrat']=0
         self.analyse['fct_certif_med']=0
         self.analyse['fct_oubli_cours']=0
         self.analyse['fct_credits_inf_50']=0
         self.analyse['fct_echec_travail']=0
         self.analyse['fct_classement_cours']=0
         self.analyse['fct_classement_cours_app']=0
         self.analyse['fct_age']=0
         self.analyse['fct_sciences6']=0
         self.analyse['fct_sciences6_mars']=0
         self.analyse['fct_prop_echec']=0
         self.analyse['fct_daca']=0
         self.analyse['fct_daca_mars']=0
         self.analyse['fct_moyenne_ponderee_cg']=0
         self.ctg=False
         self.ddn=False
         self.pia=False
         self.noel=False
         self.mars=False
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
                     setattr(cours, carac, valeure)
                 # fusion de cours venant d'être créé avec celui présent dans la grille horaire de chaque élève de la classe
                 for eleve in self.carnet_cotes.values():
                     if cours.abr.lower() not in eleve.grille_horaire.keys():
                         eleve.grille_horaire[cours.abr.lower()]=Cours()
                     for carac in liste_carac_bool:
                         setattr(eleve.grille_horaire[cours.abr.lower()],carac,getattr(cours,carac))
                     for carac in liste_carac_int:
                         setattr(eleve.grille_horaire[cours.abr.lower()],carac,getattr(cours,carac))
                     for carac in liste_carac_str:
                         setattr(eleve.grille_horaire[cours.abr.lower()],carac,getattr(cours,carac))
                     #else:
                         #eleve.grille_horaire[cours.abr.lower()]=cours
                     
             print ("Création d'une classe de", self.niv_sec)
         except Exception as e:
             QMessageBox.critical(gui,'Echec',"Erreur dans la lecture du fichier de description des cours.")
             print ('Erreur dans la lecture du fichier de description des cours')
             print ('Erreur : %s' % e)
             print (traceback.format_exc())
         #
         try:
             tree = ET.parse('./criteres.xml')
             for niveau in tree.iter('niveau'):
                 if niveau.get('name')==self.niv_sec:
                     tree_niveau=niveau
             self.criteres=Criteres()
             for node_critere in tree_niveau:
                 setattr(self.criteres, node_critere.tag,int(node_critere.text))
         except Exception as e:
             QMessageBox.critical(gui,'Echec',"Erreur dans la lecture du fichier de description des critères.")
             print ('Erreur dans la lecture du fichier de description des critères.')
             print ('Erreur : %s' % e)
             print (traceback.format_exc())
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
                 self.analyse[analyse.tag]=bool(int(analyse.text))
                 
         except Exception as e:
             QMessageBox.critical(gui,'Echec',"Erreur dans la lecture du fichier des analyses à effectuer.")
             print ('Erreur dans la lecture du fichier des analyses à effectuer.')
             print ('Erreur : %s' % e)
             print (traceback.format_exc())
         #
     
     def stats_elv(self):
         for eleve in self.carnet_cotes.values():
             eleve.fct_dispense()
             #
             if classe.analyse['fct_sciences6']==True:
                 eleve.fct_sciences6()
             if classe.analyse['fct_sciences6_mars']==True:
                 eleve.fct_sciences6_mars()
             if classe.analyse['fct_daca']==True:
                 eleve.fct_daca()
             if classe.analyse['fct_daca_mars']==True:
                 eleve.fct_daca_mars()
             if classe.analyse['fct_points_sup_100']==True:
                 eleve.fct_points_sup_100()
             if classe.analyse['fct_moyenne_ponderee']==True:
                 eleve.fct_moyenne_ponderee()
             if classe.analyse['fct_echec_inf35']==True:
                 eleve.fct_echec_inf35()
             if classe.analyse['fct_nb_heures_horaire']==True:
                 eleve.fct_nb_heures_horaire()
             if classe.analyse['fct_total_heures_echec']==True:
                 eleve.fct_total_heures_echec()
             if classe.analyse['fct_cours_verrou_echec']==True:
                 eleve.fct_cours_verrou_echec()
             if classe.analyse['fct_nb_cours_echec']==True:
                 eleve.fct_nb_cours_echec()
             if classe.analyse['fct_echec_contrat']==True:
                 eleve.fct_echec_contrat()
             if classe.analyse['fct_certif_med']==True:
                 eleve.fct_certif_med()
             if classe.analyse['fct_oubli_cours']==True:
                 eleve.fct_oubli_cours()
             if classe.analyse['fct_credits_inf_50']==True:
                 eleve.fct_credits_inf_50()
             if classe.analyse['fct_echec_travail']==True:
                 eleve.fct_echec_travail()
             if classe.analyse['fct_classement_cours']==True:
                 eleve.fct_classement_cours()
             if classe.analyse['fct_classement_cours_app']==True:
                 eleve.fct_classement_cours_app()
             if classe.analyse['fct_age']==True:
                 eleve.fct_age()
             if classe.analyse['fct_prop_echec']==True:
                 eleve.fct_prop_echec()
             
             if classe.analyse['fct_moyenne_ponderee_cg']==True:
                 eleve.fct_moyenne_ponderee_cg()
             
     #
     def prod_situation_globale(self):
         for eleve in self.carnet_cotes.values():
             
             situation_globale=False
             if eleve.heures_echec_cc==0 :
                 eleve.situation_globale=3 #aucun probleme
                 situation_globale=True #un critère a été rencontré
             #
             if eleve.heures_echec_cc>self.criteres.heures_echec_max:
                 eleve.situation_globale=1 #echec en fin d'année
                 situation_globale=True #un critère a été rencontré
                 
             if eleve.nb_cours_verrou_echec>self.criteres.cours_verrou_echec_max:
                 eleve.situation_globale=1
                 situation_globale=True #un critère a été rencontré
                 
             if ((eleve.nb_cours_inf35>=self.criteres.echec_sur_exclusion_max) & (eleve.nb_cours_cc_echec>=2)):
                 eleve.situation_globale=1
                 situation_globale=True #un critère a été rencontré
                 
             if eleve.echec_daca==True:
                 eleve.situation_globale=1 # en art uniquement
                 situation_globale=True #un critère a été rencontré
             
             #if (eleve.prop_echec<=33.33) & (eleve.prop_echec>0) :
                 #eleve.situation_globale=2 # en rétho uniquement, l'élève est admissible pour une 2°session
                 #situation_globale=True #un critère a été rencontré
             
             if eleve.prop_echec>33.33 :
                 eleve.situation_globale=1 # en rétho uniquement, l'élève n'est pas admissible pour une 2°session
                 situation_globale=True #un critère a été rencontré
             
             if situation_globale==False: #aucun critère n'a été rencontré:
                 eleve.situation_globale=2 # certains cours en echec mais réussite de l'année
             
             if (eleve.liste_certif_med!='') or (eleve.liste_oubli_cours!=''):
                 eleve.situation_globale=4 # non délibérable
     #
     #
     def prod_liste_eleves(self):
         self.liste_eleves=self.carnet_cotes.keys()
     #
     def update_liste_cours(self):
         """Cette fonction produit une liste des cours ne contenant que les cours évalués pour au moins un élève de la classe"""
         liste_cours_1gt=['rel','fran','ndls','ndls_f','math','math_f','edm','sc','sc_f','ed_phys','techno','mus','des','lat','ac_m','ac_f','ac_n','proj_f','proj_n','proj_m']
         liste_cours_2gt=['rel','fran','ndls','math','edm','sc','ed_phys','techno','des','lat','fse','tdf','ac_n','proj_f','proj_n','proj_m']
         liste_cours_3gt=['rel','fran','geo','hist','ndls','math','chim','phys','bio','sc_3','sc_5','ed_phys','angl_4','sc_eco','lat','grec','rf','angl_2']
         liste_cours_4gt=['rel','fran','geo','hist','ndls','math','chim','phys','bio','sc_3','sc_5','ed_phys','angl_4','sc_eco','lat','grec','rf','angl_2']
         liste_cours_5gt=['rel','fran','fgs','fh','ndls','math_4','math_6','chim','phys','bio','chim_1','phys_1','bio_1','chim_2','phys_2','bio_2','sc_3','sc_6','ed_phys','angl_4','sc_eco','lat','grec','angl_2','actu','esp','info','ha']
         liste_cours_6gt=['rel','fran','fgs','fh','ndls','math_4','math_6','chim','phys','bio','chim_1','phys_1','bio_1','chim_2','phys_2','bio_2','sc_3','sc_6','ed_phys','angl_4','sc_eco','lat','grec','angl_2','actu','esp','info','ha']
         liste_cours_3tq=['rel','fran','sh','sc_tech','ndls','math','ed_phys','cr','fc','3d','ed_plas','daca+ep','ha','meth']
         liste_cours_4tq=['rel','fran','sh','sc_tech','ndls','math','ed_phys','cr','fc','3d','ed_plas','daca+ep','ha','exco','grav','info']
         liste_cours_5tq=['rel','fran','sh','sc_tech','ndls','math','ed_phys','cr','fc','3d','info','daca+ep','mus','ha','ds','ac_n']
         liste_cours_6tq=['rel','fran','sh','sc_tech','ndls','math','ed_phys','cr','fc','3d','audio','daca+ep','anim','ha','ds','angl']
         if self.niv_sec=='1GT':liste_cours_annee=liste_cours_1gt
         if self.niv_sec=='2GT':liste_cours_annee=liste_cours_2gt
         if self.niv_sec=='3GT':liste_cours_annee=liste_cours_3gt
         if self.niv_sec=='4GT':liste_cours_annee=liste_cours_4gt
         if self.niv_sec=='5GT':liste_cours_annee=liste_cours_5gt
         if self.niv_sec=='6GT':liste_cours_annee=liste_cours_6gt
         if self.niv_sec=='3TQ':liste_cours_annee=liste_cours_3tq
         if self.niv_sec=='4TQ':liste_cours_annee=liste_cours_4tq
         if self.niv_sec=='5TQ':liste_cours_annee=liste_cours_5tq
         if self.niv_sec=='6TQ':liste_cours_annee=liste_cours_6tq
         self.liste_cours=[]
         for eleve in self.carnet_cotes.values():
             for cours in eleve.grille_horaire.keys():
                 
                 #les cours de chim_1,chim_2, ... n'apparaissent pas tels quels dans la liste des cours
                 #ils se retrouvent sous le nom de 'chim', 'phys', ... afin de les placer dans la même colonne du tableau récapitulatif
                 
                 if (cours not in self.liste_cours) & ((eleve.grille_horaire[cours].points!=False)or(eleve.grille_horaire[cours].appreciation!=False)):
                     if (cours=='chim_1') or (cours=='chim_2'): cours='chim'
                     if (cours=='phys_1') or (cours=='phys_2'): cours='phys'
                     if (cours=='bio_1') or (cours=='bio_2'): cours='bio'
                     if cours not in self.liste_cours:
                         self.liste_cours.append(cours)
         self.liste_cours=sorted(self.liste_cours, key=lambda cours : liste_cours_annee.index(cours))
#
#
class Eleve(Classe):
     """Un élève est un membre d'une classe, il possède un nom, une grille horaire avec des points et un ensemble de
     statistiques relatives à ces points."""
     def __init__(self):
         self.pia=False
         self.ctg=False
         self.ddn='01/01/1901'
         self.eval_certif=False
         self.vol_horaire_cc=0
         self.vol_horaire_ccnc=0
         self.grille_horaire={}
         self.moy_pond_cc=0
         self.moy_pond_cg=0
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
         self.classement_cours=False
         self.noel=''
         self.mars=''
         self.echec_daca=False
         self.prop_echec=0
     #
     def fct_points_sup_100(self):
         for cours in self.grille_horaire.values():
             if cours.points!=False:
                 if cours.points>100:
                     QMessageBox.warning(gui,'Erreur',"<div><p>L'élève %s a une cote supérieure à 100.</p> <p> %s : %s</p></div>"%(self.nom,cours.intitule,cours.points) )
     #
     def fct_dispense(self):
         for cours in self.grille_horaire.values():
             if (cours.evaluation==5):
                 cours.option=True
                 cours.evaluation=0
     #
     def fct_nb_heures_horaire(self):
         """Cette fonction calcule pour un eleve :
           => le nombre d'heures de cours certificatives dans son horaire,
           => le nombre total d'heures de cours dans son horaire.
         Les heures dans l'horaires peuvent être calculées
         dés qu'il y a une évaluation, cad s'il y a une appréciation ou des points."""
         for cours in self.grille_horaire.values():
             if (cours.evaluation!=0) & (cours.pseudo==False):
                 self.vol_horaire_ccnc+=cours.heures
             if (cours.evaluation!=0) & (cours.ccnc==True):
                 self.vol_horaire_cc+=cours.heures
         if self.vol_horaire_ccnc < 30:
             QMessageBox.warning(gui,'Erreur',"<p>L'élève %s a un volume horaire inférieur à 30p./sem.</p> <p>Vérifiez s'il ne manque pas de points</p>"%self.nom) 
     #
     #
     def fct_moyenne_ponderee(self):
         """Cette fonction calcule pour un eleve :
           => la moyenne pondérée des cours certificatifs
           => la moyenne pondérée de l'ensemble des cours.
         Les moyennes pondérées ne peuvent être calculées que s'il y a des points."""
         total_heures_cc=0
         total_heures_ccnc=0
         for cours in self.grille_horaire.values():
             if (cours.ccnc==True) & (cours.points!=False):
                 self.moy_pond_cc+=cours.heures*cours.points
                 total_heures_cc+=cours.heures
             #
             if (cours.points!=False) & (cours.pseudo==False):
                 self.moy_pond_ccnc+=cours.heures*cours.points
                 total_heures_ccnc+=cours.heures
         self.moy_pond_cc=round((self.moy_pond_cc/total_heures_cc),1)
         self.moy_pond_ccnc=round((self.moy_pond_ccnc/total_heures_ccnc),1)
     #
     #
     def fct_total_heures_echec(self): 
         """Cette fonction calcule, pour un eleve:
          => le nombre d'heures de cours certificatifs en échec,
          => le nombre d'heures de cours non-certificatifs en échec,
          => le nombre total d'heures de cours en échec."""
         for cours in self.grille_horaire.values():
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
         for cours in self.grille_horaire.values():
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
         for cours in self.grille_horaire.values():
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
         for cours in self.grille_horaire.values():
             if (cours.evaluation==1) & (cours.ccnc==True):
                 self.nb_cours_cc_echec+=1
             if (cours.evaluation==1) & (cours.ccnc==False) & (cours.pseudo==False):
                 self.nb_cours_nc_echec+=1
     #
     #
     def fct_echec_contrat(self):
         liste_echec_contrat=[]
         for cours in self.grille_horaire.values():
             if (cours.contrat==True) & (cours.evaluation==1):
                 liste_echec_contrat.append(cours.intitule)
         self.liste_echec_contrat=", ".join(liste_echec_contrat)
     #
     #
     def fct_certif_med(self):
         liste_certif_med=[]
         for cours in self.grille_horaire.values():
             if cours.certif_med==True:
                 liste_certif_med.append(cours.intitule)
         self.liste_certif_med=", ".join(liste_certif_med)
     #
     #
     def fct_oubli_cours(self):
         liste_oubli_cours=[]
         for cours in self.grille_horaire.values():
             if (cours.evaluation==0) & (cours.option==False) & (cours.certif_med==False):
                 liste_oubli_cours.append(cours.intitule)
         self.liste_oubli_cours=", ".join(liste_oubli_cours)
     #
     #
     def fct_credits_inf_50(self):
         ecart=0
         ecart_pondere=0
         for cours in self.grille_horaire.values():
             if (cours.points!=False) & (cours.ccnc==True): 
                 if(int(cours.points)<50):
                     ecart=50-(int(cours.points))
                     ecart_pondere=ecart*(cours.heures)
                     self.credits_inf_50+=ecart_pondere
     #
     #
     def fct_echec_travail(self):
         liste_echec_travail=[]
         for cours in self.grille_horaire.values():
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
         for cours in self.grille_horaire.values():
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
     def fct_classement_cours_app(self):
         self.classement_cours={}
         liste_e=[]
         liste_f=[]
         liste_r=[]
         for cours in self.grille_horaire.values():
             if cours.appreciation!=False:
                 if cours.appreciation=='e':
                     liste_e.append(cours.abr.lower())
                 elif cours.appreciation=='f':
                     liste_f.append(cours.abr.lower())
                 elif cours.appreciation=='r':
                     liste_r.append(cours.abr.lower())
         self.classement_cours['e']=" ; ".join(liste_e)
         self.classement_cours['f']=" ; ".join(liste_f)
         self.classement_cours['r']=" ; ".join(liste_r)
     #
     def fct_age(self):
         """Cette fonction calcule l'age des élèves apd de leur date de naissance.
         Cette fct doit tenir compte du fait que la date de naissance (ddn) est encodée 
         sous des formats différents selon le type de document (xls, ods, tsv, ...) et va tenter de convertir les dates reçues vers le 
         format iso-8601 yyyy-mm-dd"""
         self.ddn=self.ddn.replace('/','-')
         try:
             self.ddn=datetime.strptime(self.ddn, '%Y-%m-%d %H:%M:%S').date()
         except ValueError:
             try:
                 self.ddn=datetime.strptime(self.ddn, '%Y-%m-%d').date()
             except ValueError:
                 try:
                     self.ddn=datetime.strptime(self.ddn, '%y-%m-%d').date()
                 except ValueError:
                     try:
                         self.ddn=datetime.strptime(self.ddn, '%d-%m-%Y').date()
                     except ValueError:
                         try:
                             self.ddn=datetime.strptime(self.ddn, '%d-%m-%y').date()
                         except ValueError:
                             print ("Le format de la date de naissance de %s n'est pas pris en charge" %(self.nom))
                             #print 'Erreur : %s' % e
                             #print traceback.format_exc()
                             self.ddn=False
                             self.age=False
                             self.age_str=False
                         except Exception as e:
                             self.ddn=False
                             self.age=False
                             self.age_str=False
                             print ("Erreur inconnue dans le traitement d'une date de naissance")
                             print ('Erreur : %s' % e)
                             print (traceback.format_exc())
         
         if self.ddn!=False:
             age=date.today()-self.ddn
             ans=int(age.days//365.2425)
             mois=int(round((age.days%365.2425)/30.5))
             self.age_str=str(ans)+' ans '+str(mois)+' mois'
             self.age=age.days/365.2425
     #    
     def fct_sciences6 (self):
         sc_3=False
         sc_6=False
         if self.grille_horaire['phys_2'].points!=False:
             sc_6=True
         if self.grille_horaire['chim_2'].points!=False:
             sc_6=True
         if self.grille_horaire['bio_2'].points!=False:
             sc_6=True
         if self.grille_horaire['phys_1'].points!=False:
             sc_3=True
         if self.grille_horaire['chim_1'].points!=False:
             sc_3=True
         if self.grille_horaire['bio_1'].points!=False:
             sc_3=True
         if (sc_6==True) & (sc_3==True):
             QMessageBox.warning(gui,'Erreur',"L'élève %s a des points en sciences 6 et en sciences 3."%self.nom) 
         if (sc_6==False) & (sc_3==False):
             QMessageBox.warning(gui,'Erreur',"L'élève %s n'a de points ni en sciences 6 ni en sciences 3."%self.nom) 
         if (sc_6==True) & (sc_3==False):
             nb_echecs=0
             nb_echecs_inf45=0
             self.grille_horaire['sc_3'].points=False
             self.grille_horaire['sc_3'].evaluation=0
             
             if self.grille_horaire['bio_2'].points<50 : nb_echecs+=1
             if self.grille_horaire['chim_2'].points<50 : nb_echecs+=1
             if self.grille_horaire['phys_2'].points<50 : nb_echecs+=1
             if self.grille_horaire['bio_2'].points<45 : nb_echecs_inf45+=1
             if self.grille_horaire['chim_2'].points<45 : nb_echecs_inf45+=1
             if self.grille_horaire['phys_2'].points<45 : nb_echecs_inf45+=1
             
             self.grille_horaire['sc_6'].points=(self.grille_horaire['phys_2'].points+self.grille_horaire['bio_2'].points+self.grille_horaire['chim_2'].points)/3
             self.grille_horaire['sc_6'].points=round(self.grille_horaire['sc_6'].points,1)
             
             if 'sc_6' not in classe.liste_cours:
                 classe.liste_cours.append('sc_6')
             
             if self.grille_horaire['sc_6'].points<50:
                 self.grille_horaire['sc_6'].evaluation=1
             if (self.grille_horaire['sc_6'].points>=50) & (self.grille_horaire['sc_6'].points<60):
                 self.grille_horaire['sc_6'].evaluation=2
             if self.grille_horaire['sc_6'].points>=60:
                 self.grille_horaire['sc_6'].evaluation=3   
             
             if self.grille_horaire['sc_6'].points<50:
                 self.grille_horaire['bio_2'].echec_force=True
                 self.grille_horaire['chim_2'].echec_force=True
                 self.grille_horaire['phys_2'].echec_force=True
                 self.grille_horaire['bio_2'].evaluation=1
                 self.grille_horaire['chim_2'].evaluation=1
                 self.grille_horaire['phys_2'].evaluation=1
             if nb_echecs>1 :
                 self.grille_horaire['bio_2'].echec_force=True
                 self.grille_horaire['chim_2'].echec_force=True
                 self.grille_horaire['phys_2'].echec_force=True
                 self.grille_horaire['sc_6'].echec_force=True
                 self.grille_horaire['bio_2'].evaluation=1
                 self.grille_horaire['chim_2'].evaluation=1
                 self.grille_horaire['phys_2'].evaluation=1
             if nb_echecs_inf45>0 :
                 self.grille_horaire['bio_2'].echec_force=True
                 self.grille_horaire['chim_2'].echec_force=True
                 self.grille_horaire['phys_2'].echec_force=True
                 self.grille_horaire['sc_6'].echec_force=True
                 self.grille_horaire['bio_2'].evaluation=1
                 self.grille_horaire['chim_2'].evaluation=1
                 self.grille_horaire['phys_2'].evaluation=1
         if (sc_6==False) & (sc_3==True):
             nb_cours_evalues=0
             self.grille_horaire['sc_3'].points=0
             if self.grille_horaire['bio_1'].points!=False:
                 self.grille_horaire['sc_3'].points+=float(self.grille_horaire['bio_1'].points)
                 nb_cours_evalues+=1
             if self.grille_horaire['phys_1'].points!=False:
                 self.grille_horaire['sc_3'].points+=float(self.grille_horaire['phys_1'].points)
                 nb_cours_evalues+=1
             if self.grille_horaire['chim_1'].points!=False:
                 self.grille_horaire['sc_3'].points+=float(self.grille_horaire['chim_1'].points)
                 nb_cours_evalues+=1
             self.grille_horaire['sc_3'].points=(self.grille_horaire['sc_3'].points)/nb_cours_evalues
             self.grille_horaire['sc_3'].points=round(self.grille_horaire['sc_3'].points,1)
             if 'sc_3' not in classe.liste_cours:
                 classe.liste_cours.append('sc_3')
             
             if self.grille_horaire['sc_3'].points<50:
                 self.grille_horaire['sc_3'].evaluation=1
             if (self.grille_horaire['sc_3'].points>=50) & (self.grille_horaire['sc_3'].points<60):
                 self.grille_horaire['sc_3'].evaluation=2
             if self.grille_horaire['sc_3'].points>=60:
                 self.grille_horaire['sc_3'].evaluation=3   
             
             self.grille_horaire['sc_6'].points=False
             self.grille_horaire['sc_6'].evaluation=0
             if self.grille_horaire['sc_3'].points<50:
                 self.grille_horaire['bio_1'].echec_force=True
                 self.grille_horaire['chim_1'].echec_force=True
                 self.grille_horaire['phys_1'].echec_force=True
                 self.grille_horaire['bio_1'].evaluation=1
                 self.grille_horaire['chim_1'].evaluation=1
                 self.grille_horaire['phys_1'].evaluation=1
     #
     def fct_sciences6_mars (self):
         sc_3=False
         sc_6=False
         if self.grille_horaire['phys_2'].appreciation!=False:
             sc_6=True
         if self.grille_horaire['chim_2'].appreciation!=False:
             sc_6=True
         if self.grille_horaire['bio_2'].appreciation!=False:
             sc_6=True
         if self.grille_horaire['phys_1'].appreciation!=False:
             sc_3=True
         if self.grille_horaire['chim_1'].appreciation!=False:
             sc_3=True
         if self.grille_horaire['bio_1'].appreciation!=False:
             sc_3=True
         if (sc_6==True) & (sc_3==True):
             QMessageBox.warning(gui,'Erreur',"L'élève %s a une appréciation en sciences 6 et en sciences 3."%self.nom) 
         if (sc_6==False) & (sc_3==False):
             QMessageBox.warning(gui,'Erreur',"L'élève %s n'a d'appréciation ni en sciences 6 ni en sciences 3."%self.nom) 
         
         
         if (sc_6==True) & (sc_3==False):
             if 'sc_6' not in classe.liste_cours:
                 classe.liste_cours.append('sc_6')
                 classe.update_liste_cours()
             nb_echecs=0
             nb_faible=0
             nb_reussi=0
             
             if self.grille_horaire['bio_2'].appreciation=='e' : nb_echecs+=1
             if self.grille_horaire['chim_2'].appreciation=='e' : nb_echecs+=1
             if self.grille_horaire['phys_2'].appreciation=='e' : nb_echecs+=1
             
             if self.grille_horaire['bio_2'].appreciation=='f' : nb_faible+=1
             if self.grille_horaire['chim_2'].appreciation=='f' : nb_faible+=1
             if self.grille_horaire['phys_2'].appreciation=='f' : nb_faible+=1
             
             if self.grille_horaire['bio_2'].appreciation=='r' : nb_reussi+=1
             if self.grille_horaire['chim_2'].appreciation=='r' : nb_reussi+=1
             if self.grille_horaire['phys_2'].appreciation=='r' : nb_reussi+=1
             
             if nb_echecs>=1 :
                 self.grille_horaire['bio_2'].echec_force=True
                 self.grille_horaire['chim_2'].echec_force=True
                 self.grille_horaire['phys_2'].echec_force=True
                 self.grille_horaire['sc_6'].echec_force=True
                 self.grille_horaire['sc_6'].evaluation=1
                 self.grille_horaire['sc_6'].appreciation='e'
                 self.grille_horaire['bio_2'].evaluation=1
                 self.grille_horaire['chim_2'].evaluation=1
                 self.grille_horaire['phys_2'].evaluation=1
             elif (nb_faible>=2) & (nb_echecs==0):
                 self.grille_horaire['sc_6'].evaluation=2
                 self.grille_horaire['sc_6'].appreciation='f'
             elif (nb_reussi>=2) & (nb_echecs==0) :
                 self.grille_horaire['sc_6'].evaluation=3
                 self.grille_horaire['sc_6'].appreciation='r'
             
             
         if (sc_6==False) & (sc_3==True):
             if 'sc_3' not in classe.liste_cours:
                 classe.liste_cours.append('sc_3')
                 classe.update_liste_cours()
             self.grille_horaire['sc_3'].appreciation='x'
             self.grille_horaire['sc_3'].evaluation=4
             nb_echecs=0
             nb_faible=0
             nb_reussi=0
             
             if self.grille_horaire['bio_1'].appreciation=='e' : nb_echecs+=1
             if self.grille_horaire['chim_1'].appreciation=='e' : nb_echecs+=1
             if self.grille_horaire['phys_1'].appreciation=='e' : nb_echecs+=1
             
             if self.grille_horaire['bio_1'].appreciation=='f' : nb_faible+=1
             if self.grille_horaire['chim_1'].appreciation=='f' : nb_faible+=1
             if self.grille_horaire['phys_1'].appreciation=='f' : nb_faible+=1
             
             if self.grille_horaire['bio_1'].appreciation=='r' : nb_reussi+=1
             if self.grille_horaire['chim_1'].appreciation=='r' : nb_reussi+=1
             if self.grille_horaire['phys_1'].appreciation=='r' : nb_reussi+=1
             
             if nb_echecs>=2 :
                 self.grille_horaire['bio_1'].echec_force=True
                 self.grille_horaire['chim_1'].echec_force=True
                 self.grille_horaire['phys_1'].echec_force=True
                 self.grille_horaire['sc_3'].echec_force=True
                 self.grille_horaire['sc_3'].evaluation=1
                 self.grille_horaire['sc_3'].appreciation='e'
                 self.grille_horaire['bio_1'].evaluation=1
                 self.grille_horaire['chim_1'].evaluation=1
                 self.grille_horaire['phys_1'].evaluation=1
             elif nb_faible>=2:
                 self.grille_horaire['sc_3'].evaluation=2
                 self.grille_horaire['sc_3'].appreciation='f'
             elif nb_reussi==2 & nb_echecs==1 :
                 self.grille_horaire['sc_3'].evaluation=2
                 self.grille_horaire['sc_3'].appreciation='f'
             elif nb_reussi==1 & nb_echecs==1 & nb_faible==1:
                 self.grille_horaire['sc_3'].evaluation=2
                 self.grille_horaire['sc_3'].appreciation='f'
             elif nb_reussi>=2 & (nb_echecs==1 or nb_faible==1):
                 self.grille_horaire['sc_3'].evaluation=3
                 self.grille_horaire['sc_3'].appreciation='r'
     #
     def fct_prop_echec(self):
         self.prop_echec=(self.heures_echec_nc+self.heures_echec_cc)/float(self.vol_horaire_ccnc)
         self.prop_echec=round(self.prop_echec*100,2)
     #
     def fct_daca_mars(self):
         """Cette fonction calcule la moyenne pondérée des cours DACA, la moyenne pondérée des cours ED_PLAS et la moyenne pondérée de DACA et ED_PLAS ensemble"""
         
         if 'daca+ep' not in classe.liste_cours:
             classe.liste_cours.append('daca+ep')
             classe.update_liste_cours()
         
         nb_echecs=0
         nb_faible=0
         nb_reussi=0
             
         if self.grille_horaire['cr'].appreciation=='e' : nb_echecs+=1
         if self.grille_horaire['fc'].appreciation=='e' : nb_echecs+=1
         if self.grille_horaire['3d'].appreciation=='e' : nb_echecs+=1
             
         if self.grille_horaire['cr'].appreciation=='f' : nb_faible+=1
         if self.grille_horaire['fc'].appreciation=='f' : nb_faible+=1
         if self.grille_horaire['3d'].appreciation=='f' : nb_faible+=1
             
         if self.grille_horaire['cr'].appreciation=='r' : nb_reussi+=1
         if self.grille_horaire['fc'].appreciation=='r' : nb_reussi+=1
         if self.grille_horaire['3d'].appreciation=='r' : nb_reussi+=1
         
         if classe.niv_sec=='3TQ' :
             #en 3TQ, ed_plas existe tel quel et daca correspond à CR+FC+3D
             if self.grille_horaire['ed_plas'].appreciation=='e' : nb_echecs+=1
             if self.grille_horaire['ed_plas'].appreciation=='f' : nb_faible+=1
             if self.grille_horaire['ed_plas'].appreciation=='r' : nb_reussi+=1
         #
         if classe.niv_sec=='4TQ':
             #en 4TQ, ed_plas=INFO+GRAV  ; DACA=CR+FC+3D
             nb_reussi_ed_plas=0
             nb_faible_ed_plas=0
             nb_echec_ed_plas=0
             if self.grille_horaire['grav'].appreciation=='r' : nb_reussi_ed_plas+=1
             if self.grille_horaire['info'].appreciation=='r' : nb_reussi_ed_plas+=1
             if self.grille_horaire['grav'].appreciation=='f' : nb_faible_ed_plas+=1
             if self.grille_horaire['info'].appreciation=='f' : nb_faible_ed_plas+=1
             if self.grille_horaire['grav'].appreciation=='e' : nb_echec_ed_plas+=1
             if self.grille_horaire['info'].appreciation=='e' : nb_echec_ed_plas+=1
             
             #ee=>e,ef=>e,er=>f,ff=>f,fr=>f,rr=>r
             if nb_echec_ed_plas==2 : 
                 self.grille_horaire['ed_plas'].appreciation='e'
                 nb_echecs+=1
             elif (nb_echec_ed_plas==1) & (nb_faible_ed_plas==1) :  
                 self.grille_horaire['ed_plas'].appreciation='e'
                 nb_echecs+=1
                 self.grille_horaire['ed_plas'].evaluation=1
             elif nb_reussi_ed_plas==2 : 
                 self.grille_horaire['ed_plas'].appreciation='r'
                 nb_reussi+=1
                 self.grille_horaire['ed_plas'].evaluation=3
             else: 
                 self.grille_horaire['ed_plas'].appreciation='f'
                 self.grille_horaire['ed_plas'].evaluation=2
                 nb_faible+=1
                 
         
         if classe.niv_sec=='5TQ':
             if self.grille_horaire['info'].appreciation=='e' : nb_echecs+=1
             if self.grille_horaire['info'].appreciation=='f' : nb_faible+=1
             if self.grille_horaire['info'].appreciation=='r' : nb_reussi+=1
             
         if classe.niv_sec=='6TQ':
             if self.grille_horaire['audio'].appreciation=='e' : nb_echecs+=1
             if self.grille_horaire['audio'].appreciation=='f' : nb_faible+=1
             if self.grille_horaire['audio'].appreciation=='r' : nb_reussi+=1
             #self.grille_horaire['ed_plas'].appreciation=self.grille_horaire['audio'].appreciation
         
         #if self.grille_horaire['ed_plas'].appreciation=='r' : nb_reussi+=1
         #if self.grille_horaire['ed_plas'].appreciation=='f' : nb_faible+=1
         #if self.grille_horaire['ed_plas'].appreciation=='e' : nb_echecs+=1
         
         if nb_echecs>=2 : 
             self.grille_horaire['daca+ep'].appreciation='e'
             self.grille_horaire['daca+ep'].evaluation=1
             self.echec_daca=True
         elif (nb_echecs>=1) & (nb_faible>=1) : 
             self.grille_horaire['daca+ep'].appreciation='e'
             self.grille_horaire['daca+ep'].evaluation=1
             self.echec_daca=True
         elif nb_reussi==4 : 
             self.grille_horaire['daca+ep'].appreciation='r'
             self.grille_horaire['daca+ep'].evaluation=3
         elif (nb_reussi==3) & (nb_faible==1) : 
             self.grille_horaire['daca+ep'].appreciation='r'
             self.grille_horaire['daca+ep'].evaluation=3
         else : 
             self.grille_horaire['daca+ep'].appreciation='f'
             self.grille_horaire['daca+ep'].evaluation=2
             
     def fct_daca(self):
         """Cette fonction calcule la moyenne pondérée des cours DACA et ED_PLAS ensemble"""
         if 'daca+ep' not in classe.liste_cours:
             classe.liste_cours.append('daca+ep')
             classe.update_liste_cours()
         if classe.niv_sec=='3TQ_':
             self.grille_horaire['daca+ep']=(self.grille_horaire['ed_plas']*4+self.grille_horaire['cr']*4+self.grille_horaire['fc']*3+self.grille_horaire['3d']*3)/14
         if classe.niv_sec=='4TQ_':
             #en 4TQ, ed_plas=INFO+GRAV  ; DACA=CR+FC+3D
             if 'ed_plas' not in classe.liste_cours:
                 classe.liste_cours.append('ed_plas')
                 classe.update_liste_cours()
             self.grille_horaire['ed_plas']=(self.grille_horaire['info']+self.grille_horaire['grav'])/2
             self.grille_horaire['daca+ep']=(self.grille_horaire['ed_plas']*4+self.grille_horaire['cr']*4+self.grille_horaire['fc']*3+self.grille_horaire['3d']*3)/14
         if classe.niv_sec=='5TQ_':
             #en 5TQ ed_plas=Info
             self.grille_horaire['daca+ep']=(self.grille_horaire['info']*2+self.grille_horaire['cr']*4+self.grille_horaire['fc']*2+self.grille_horaire['3d']*2)/10
         if classe.niv_sec=='6TQ_':
             #en 6TQ ed_plas=audio
             self.grille_horaire['daca+ep']=(self.grille_horaire['audio']*2+self.grille_horaire['cr']*3+self.grille_horaire['fc']*3+self.grille_horaire['3d']*2)/10
         
         if self.grille_horaire['daca+ep'].points<50:
             self.echec_daca=True
     #
     def fct_moyenne_ponderee_cg(self):
         """Cette fonction calcule, pour un eleve,
         la moyenne pondérée des cours généraux certificatifs.
         Il s'agit d'une fonction s'adressant aux élèves d'art"""
         total_heures_cg=0
         for cours in self.grille_horaire.values():
             if (cours.ccnc==True) & (cours.points!=False) & (cours.abr not in ['cr','ed_plas','3d','fc','info','grav','anim','audio','ha','exco','ds','mus']):
                 self.moy_pond_cg+=cours.heures*cours.points
                 total_heures_cg+=cours.heures
             #
         self.moy_pond_cg=round((self.moy_pond_cg/total_heures_cg),1)
         
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
         self.disp_ndls=False
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
         elif points.lower()=='disp':
             self.evaluation=5
         elif points.lower()=='x':#le cours n'est pas évalué (ex: meth en 3TQ)
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
class Latex_file():
     #
     
     def __init__(self, doc_type="",titre="",file_name=""):
         self.encoding=sys.stdout.encoding
         if self.encoding=='cp850':self.encoding='cp1252'
         if self.encoding=='UTF-8':self.encoding='utf8'
         self.doc_type=doc_type
         self.titre=titre
         self.file_name=file_name
         
         if self.doc_type=='tableau_recap':
             print ("Création du tableau récapitulatif.")
             self.tableau_recap()
         #
         if self.doc_type=='analyse':
             print ("Création du document d'analyse.")
             self.analyse()
         #
         if self.doc_type=='classement':
             print ("Création du tableau de classement.")
             self.classement()
     #
     def ligne_3cell (self, titre, valeur, couleur):
         if (couleur=='vert') or (couleur=='orange'):
             ligne="\\multicolumn {2} {|m{0.33\\textwidth}|} {%s} & " %titre
             ligne+="\\multicolumn {2} {m{0.33\\textwidth}|} {\\textcolor{%s} { %s }} & " %(couleur,valeur)
             ligne+="\\multicolumn {2} {m{0.33\\textwidth}|} {} \\\\"
         else:
             ligne="\\multicolumn {2} {|m{0.33\\textwidth}|} {%s} & " %titre
             ligne+="\\multicolumn {2} {m{0.33\\textwidth}|} {} & "
             ligne+="\\multicolumn {2} {m{0.33\\textwidth}|} {\\textcolor{%s} { %s}} \\\\" %(couleur,valeur)
         return ligne
     #
     def ligne_2cell (self, titre, valeur):
         ligne="\\multicolumn {2} {|m{0.33\\textwidth}|} {%s} & " %titre
         ligne+="\\multicolumn {4} {m{0.66\\textwidth}|} {%s} \\\\" %(valeur)
         return ligne
     #
     def analyse (self):
         list_file=[]
         list_file.append('\documentclass[12pt]{article}')
         list_file.append("\\usepackage[%s]{inputenc}" %self.encoding) #active la gestion des carac en utf-8
         list_file.append("\\usepackage[a4paper,margin=1.5cm]{geometry} ")
         list_file.append("\\usepackage{array}") #améliore le rendu des tableaux
         list_file.append("\\usepackage[frenchb]{babel}")
         list_file.append("\\usepackage[table]{xcolor}") #gestion des couleurs dans le tableau
         list_file.append("\\definecolor{gris}{rgb}{0.82,0.82,0.82}") #définition des couleurs utilisées dans le document
         list_file.append("\\definecolor{gris_fonce}{rgb}{0.57,0.57,0.57}")
         list_file.append("\\definecolor{vert}{rgb}{0.03,0.5,0.1}")
         list_file.append("\\definecolor{orange}{rgb}{1,0.43,0}")
         list_file.append("\\definecolor{rouge}{rgb}{0.9,0,0}")
         list_file.append("\\begin{document}")
         list_file.append("\\sffamily")
         list_file.append("\\setlength{\\tabcolsep}{0pt}")
         list_file.append("\\begin{center} \huge "+ self.titre +" \\end {center}") 
         for nom_eleve in sorted(classe.liste_eleves,key=cmp_to_key(compfr)):
             eleve=classe.carnet_cotes[nom_eleve]
             list_tab_elv=[]
             list_tab_elv.append("\\begin {tabular} {|m{3cm}|m{3cm}|m{3cm}|m{3cm}|m{3cm}|m{3cm}|}")
             #affichage nom, volume horaire et age si échec
             if (eleve.situation_globale ==1) or (eleve.situation_globale ==4):
                 list_tab_elv.append(("\\multicolumn {6} {|m{\\textwidth}|} {\\large %s (%s p./sem) %s} \\\\") %(eleve.nom,eleve.vol_horaire_ccnc,eleve.age_str))
             else:
                 list_tab_elv.append(("\\multicolumn {6} {|m{\\textwidth}|} {\\large %s (%s p./sem)} \\\\")%(eleve.nom,eleve.vol_horaire_ccnc))
             #affichage classement des cours
             if eleve.classement_cours !=False:
                 liste_categorie = list(eleve.classement_cours.keys())
                 liste_categorie.sort(reverse=True)
                 if len(liste_categorie)==3: #gestion des RFE
                     ligne=[]
                     for categorie in liste_categorie:
                         ligne.append('\\multicolumn {2} {|m{0.33 \\textwidth}|} {'+categorie+'}')
                     list_tab_elv.append(' & '.join(ligne)+" \\\\")
                     ligne=[]
                     for categorie in liste_categorie:
                         ligne.append('\\multicolumn {2} {|m{0.33 \\textwidth}|} {\\footnotesize  '+eleve.classement_cours[categorie]+'}')
                     list_tab_elv.append(' & '.join(ligne)+" \\\\")
                 else: #gestion normale du classement
                     list_tab_elv.append(' & '.join(liste_categorie)+"\\\\")
                     ligne=[]
                     for categorie in liste_categorie:
                         ligne.append('\\footnotesize '+eleve.classement_cours[categorie])
                     list_tab_elv.append(' & '.join(ligne)+" \\\\")
             #affichage moyenne
             if (eleve.moy_pond_ccnc<50) & (classe.analyse['fct_moyenne_ponderee']==True):
                 list_tab_elv.append(self.ligne_3cell('Moyenne pondérée',eleve.moy_pond_ccnc,'rouge'))
             elif (eleve.moy_pond_ccnc>=50) & (eleve.moy_pond_ccnc<60):
                 list_tab_elv.append(self.ligne_3cell('Moyenne pondérée',eleve.moy_pond_ccnc,'orange'))
             elif eleve.moy_pond_ccnc>60:
                 list_tab_elv.append(self.ligne_3cell('Moyenne pondérée',eleve.moy_pond_ccnc,'vert'))
             else: pass
             #affichage total heures échec, heures_echec_tot est une chaine de caractères
             if eleve.heures_echec_cc > classe.criteres.heures_echec_max:
                 list_tab_elv.append(self.ligne_3cell('Total heures échec',eleve.heures_echec_tot,'rouge'))
             elif (eleve.heures_echec_cc <=classe.criteres.heures_echec_max) & (eleve.heures_echec_tot !='0'): 
                 list_tab_elv.append(self.ligne_3cell('Total heures échec',eleve.heures_echec_tot,'orange'))
             else :pass
             #affichage cours verrou echec
             if (eleve.nb_cours_verrou_echec > classe.criteres.cours_verrou_echec_max):
                 list_tab_elv.append(self.ligne_3cell('Cours verrou échec',eleve.liste_cours_verrou_echec,'rouge'))
             elif (eleve.nb_cours_verrou_echec >0) & (eleve.nb_cours_verrou_echec <= classe.criteres.cours_verrou_echec_max):
                 list_tab_elv.append(self.ligne_3cell('Cours verrou échec',eleve.liste_cours_verrou_echec,'orange'))
             else :pass
             #affichage cours inf 35
             if (eleve.nb_cours_inf35 >0) & (eleve.nb_cours_cc_echec >classe.criteres.echec_sur_exclusion_max):
                 list_tab_elv.append(self.ligne_3cell('Cours inf. 35',eleve.liste_cours_inf35,'rouge'))
             elif (eleve.nb_cours_inf35 ==1) & (eleve.nb_cours_cc_echec ==1):
                 list_tab_elv.append(self.ligne_3cell('Cours inf. 35',eleve.liste_cours_inf35,'orange'))
             else :pass
             #affichage de la proportion des échecs pour les rhétos
             if (eleve.prop_echec>0) & (eleve.prop_echec<=33.33):
                 list_tab_elv.append(self.ligne_3cell('Prop. échecs',eleve.prop_echec,'orange'))
                 #list_tab_elv.append(self.ligne_3cell('Prop. échecs',eleve.prop_echec,'orange'))
                 #table=self.creer_ligne(table,"Prop. échecs", 1,(str(eleve.prop_echec)+'%'),None)
             elif eleve.prop_echec>33.33:
                 list_tab_elv.append(self.ligne_3cell('Prop. échecs',eleve.prop_echec,'rouge'))
             #affichage des points de DACA et ed_plas en TQ
             if 'daca+ep' in eleve.grille_horaire.keys():
                 if eleve.grille_horaire['daca+ep'].points<50:
                     list_tab_elv.append(self.ligne_3cell("DACA et éducation plastique",eleve.grille_horaire['daca+ep'].points,'rouge'))
                 elif (eleve.grille_horaire['daca+ep'].points>50) & (eleve.grille_horaire['daca+ep'].points<60):
                     list_tab_elv.append(self.ligne_3cell("DACA et éducation plastique",eleve.grille_horaire['daca+ep'].points,'orange'))
                 else:
                     list_tab_elv.append(self.ligne_3cell("DACA et éducation plastique",eleve.grille_horaire['daca+ep'].points,'vert'))
             #affichage de la moyenne des cours généraux
             if eleve.moy_pond_cg!=0:
                 if eleve.moy_pond_cg<50:
                     list_tab_elv.append(self.ligne_3cell("Moyenne cours généraux",eleve.moy_pond_cg,'rouge'))
                 elif (eleve.moy_pond_cg>50) & (eleve.moy_pond_cg<60):
                     list_tab_elv.append(self.ligne_3cell("Moyenne cours généraux",eleve.moy_pond_cg,'orange'))
                 else:
                     list_tab_elv.append(self.ligne_3cell("Moyenne cours généraux",eleve.moy_pond_cg,'vert'))
             #affichage des résultats antérieurs de l'année en cours
             if (eleve.noel!="") or (eleve.mars!=""):
                 resultats_anterieurs=''
                 if eleve.noel!="":
                     resultats_anterieurs+='Noël : '
                     resultats_anterieurs+=eleve.noel
                 if eleve.mars!="":
                     resultats_anterieurs+=' ; Mars : '
                     resultats_anterieurs+=eleve.mars
                 list_tab_elv.append(self.ligne_3cell("Résultats antérieurs",resultats_anterieurs ))
             #affichage des autres infos
             if (eleve.liste_echec_contrat )!="":
                 list_tab_elv.append(self.ligne_2cell("Echec sur contrat",eleve.liste_echec_contrat ))
             #
             if (eleve.pia )!=False:
                 list_tab_elv.append(self.ligne_2cell("Remarque","L'élève dispose d'un PIA" ))
             if (eleve.ctg )!=False:
                 list_tab_elv.append(self.ligne_2cell("Remarque","L'élève dispose d'un contrat de travail global" ))
             if (eleve.liste_echec_travail )!="":
                 list_tab_elv.append(self.ligne_2cell("Envisager contrat",eleve.liste_echec_travail ))
             if eleve.liste_certif_med != '':
                 list_tab_elv.append(self.ligne_2cell("Certificat médical", eleve.liste_certif_med))
             if (eleve.liste_oubli_cours )!="":
                 list_tab_elv.append(self.ligne_2cell("Remarque", 'Pas de points en '+eleve.liste_oubli_cours ))
             for elem in list_tab_elv:
                 list_file.append(elem)
                 list_file.append("\\hline")
             list_file.append("\\end {tabular}")
             list_file.append("\\vspace{0.5cm}")
         list_file.append("\\end{document}")
         doc_name=self.file_name+'_analyse.tex'
         doc_name=QFileDialog.getSaveFileName(gui,"Sauver document d'analyse",doc_name,"Document TEX (*.tex)")
         #self.document.save(target=doc_name, pretty=True)
         gui.current_dir=os.path.dirname(doc_name)
         f = open(doc_name,'w')
         for elem in list_file:
             ligne=elem.replace('_','~')
             ligne=ligne.replace('=>','$ \\Rightarrow $')
             f.write(ligne+' \n')
         f.close()
         if platform.system()=='Linux':
             try:
                 prog=QProgressDialog()
                 prog.setWindowFlags(Qt.SplashScreen)
                 prog.setCancelButton(None)
                 prog.setLabelText ('Analyse => pdf')
                 for i in range(50):
                     prog.setValue(i)
                     prog.show()
                     QApplication.processEvents()
                     #time.sleep(0.1)
                 proc=subprocess.Popen(['pdflatex','-output-directory',os.path.dirname(doc_name),doc_name])
                 proc.wait()
                 for i in range(51):
                     prog.setValue(50+i)
                     prog.show()
                     QApplication.processEvents()
                     #time.sleep(0.1)
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_analyse.aux')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_analyse.log')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_analyse.tex')
             except Exception as e:
                 QMessageBox.critical(gui,'Echec',"La création du document pdf a échoué, vérifiez que pdflatex est bien installé sur cet ordinateur.")
                 print ('Erreur : %s' % e)
                 print (traceback.format_exc())
         if platform.system()=='Windows':
             try:
                 prog=QProgressDialog()
                 prog.setWindowFlags(Qt.SplashScreen)
                 prog.setCancelButton(None)
                 prog.setLabelText ('Analyse => pdf')
                 for i in range(50):
                     prog.setValue(i)
                     prog.show()
                     QApplication.processEvents()
                     #time.sleep(0.1)
                 proc=subprocess.Popen(['pdflatex','-output-directory',os.path.dirname(doc_name),doc_name])
                 proc.wait()
                 for i in range(51):
                     prog.setValue(50+i)
                     prog.show()
                     QApplication.processEvents()
                     #time.sleep(0.1)
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_analyse.aux')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_analyse.log')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_analyse.tex')
             except Exception as e:
                 QMessageBox.critical(gui,'Echec',"La création du document pdf a échoué, vérifiez que pdflatex est bien installé sur cet ordinateur.")
                 print ('Erreur : %s' % e)
                 print (traceback.format_exc())
         
     #
     def classement (self):
         classement_moy_pond=[]
         for eleve in classe.carnet_cotes.values():
             tuple_moy_nom=(eleve.moy_pond_ccnc,eleve.nom)
             classement_moy_pond.append(tuple_moy_nom)
         classement_moy_pond=sorted(classement_moy_pond)
         doc_name=self.file_name+'_classement.txt'
         doc_name=QFileDialog.getSaveFileName(gui,"Sauver classement",doc_name,"Document TXT (*.txt)")
         gui.current_dir=os.path.dirname(doc_name)
         f = open(doc_name,'w')
         f.write('Nom \t Moyenne \n')
         for eleve in classement_moy_pond:
             f.write(eleve[1]+'\t'+str(eleve[0]))
             f.write('\n')
         f.close()
     #
     def tableau_recap (self):
         list_file=[]
         list_file.append("\documentclass[12pt]{article}")
         
         list_file.append("\\usepackage[%s]{inputenc}"%self.encoding) #active la gestion des carac en utf-8
         list_file.append("\\usepackage[a4paper,margin=1cm,landscape]{geometry} ")
         list_file.append("\\usepackage{array}") #améliore le rendu des tableaux
         list_file.append("\\usepackage[frenchb]{babel}")
         #list_file.append("\\usepackage[T1]{fontenc}")
         list_file.append("\\usepackage[table]{xcolor}") #gestion des couleurs dans le tableau
         list_file.append("\\definecolor{gris}{rgb}{0.82,0.82,0.82}") #définition des couleurs utilisées dans le document
         list_file.append("\\definecolor{gris_fonce}{rgb}{0.57,0.57,0.57}")
         list_file.append("\\definecolor{vert}{rgb}{0.03,0.5,0.1}")
         list_file.append("\\definecolor{orange}{rgb}{1,0.43,0}")
         list_file.append("\\definecolor{rouge}{rgb}{0.9,0,0}")
         list_file.append("\\begin{document}")
         list_file.append("\\sffamily")
         list_file.append("\\thispagestyle{empty} ") #pour éviter le numéro en bas de page
         list_file.append("\\begin{center} \large "+ self.titre +" \\end {center}") 
         list_file.append("\\tiny ") #pour diminuer la taille des caractères dans le tableau
         list_file.append("\\rowcolors{1}{}{gris}") #pour mettre une ligne sur deux en gris dans le tableau
         list_file.append("\\setlength{\\tabcolsep}{0pt}")
         #
         en_tete=["COURS"]
         for nom_cours in classe.liste_cours:
             en_tete.append(nom_cours.replace('_','~').upper())#les carac "_" posent problème lors de la compilation des fichiers tex, je les remplace par un espace insecable en latex 
         if classe.noel==True:
             en_tete.append("Noël")
         if classe.mars==True:
             en_tete.append("Mars")
         en_tete.append("Échecs")
         if classe.analyse['fct_moyenne_ponderee']==True: #n'existe pas en mars
             en_tete.append("Moy.")
         en_tete.append("Global")
         
         larg_colonne=round((25.0/(len(en_tete)-1)),5)
         
         declaration_tab="\\begin{tabular}{|m{2.5cm}|"
         
         i=False
         for nom in en_tete:
             if i!=False: #puisqu'il y a ue colonne crée avec m{2.5cm}, je dois créer une colonne de moins, j'ignore donc le premier élément de la liste en_tete
                 declaration_tab+="m{%scm}|"% larg_colonne
             i=True
         declaration_tab+="}"
         #
         list_file.append(declaration_tab)
         list_file.append("\\hline")
         list_file.append((' & '.join(en_tete))+"\\\\[1.5em]")
         list_file.append("\\hline")
         for eleve in sorted(classe.liste_eleves,key=cmp_to_key(compfr)):
             ligne=[]
             ligne.append('\\tiny '+eleve[0:30])
             for nom_cours in classe.liste_cours:
                 #ce passage sert à afficher les pts de chim_1 et chim_2 sous le nom commun de chim
                 # et de faire de même pour phys et bio, ceci n'est nécessaire qu'en 5° et 6°
                 if nom_cours=='chim' :
                     try: 
                         classe.carnet_cotes[eleve].grille_horaire['chim_1'].points
                         classe.carnet_cotes[eleve].grille_horaire['chim_2'].points
                         classe.carnet_cotes[eleve].grille_horaire['chim_1'].appreciation
                         classe.carnet_cotes[eleve].grille_horaire['chim_2'].appreciation
                         if classe.carnet_cotes[eleve].grille_horaire['chim_1'].points!=False:
                             nom_cours='chim_1'
                         if classe.carnet_cotes[eleve].grille_horaire['chim_1'].appreciation!=False:
                             nom_cours='chim_1'
                         if classe.carnet_cotes[eleve].grille_horaire['chim_1'].evaluation==4:
                             nom_cours='chim_1'
                         if classe.carnet_cotes[eleve].grille_horaire['chim_1'].evaluation==1:#je rajoute cette ligne car en cas d'échec forcé via la fct_sciences6 l'évaluation passe à 1
                             nom_cours='chim_1'
                         if classe.carnet_cotes[eleve].grille_horaire['chim_2'].points!=False:
                             nom_cours='chim_2'
                         if classe.carnet_cotes[eleve].grille_horaire['chim_2'].appreciation!=False:
                             nom_cours='chim_2'
                         if nom_cours=='chim':
                             QMessageBox.warning(gui,'Erreur',"<div><p> L'élève %s n'a de points ni en chimie 1 ni en chimie 2.</p></div>"%eleve)
                     except KeyError :
                         pass
                 if nom_cours=='bio' :
                     try: 
                         classe.carnet_cotes[eleve].grille_horaire['bio_1'].points
                         classe.carnet_cotes[eleve].grille_horaire['bio_2'].points
                         classe.carnet_cotes[eleve].grille_horaire['bio_1'].appreciation
                         classe.carnet_cotes[eleve].grille_horaire['bio_2'].appreciation
                         if classe.carnet_cotes[eleve].grille_horaire['bio_1'].appreciation!=False:
                             nom_cours='bio_1'
                         if classe.carnet_cotes[eleve].grille_horaire['bio_2'].appreciation!=False:
                             nom_cours='bio_2'
                         if classe.carnet_cotes[eleve].grille_horaire['bio_1'].points!=False:
                             nom_cours='bio_1'
                         if classe.carnet_cotes[eleve].grille_horaire['bio_1'].evaluation==4:
                             nom_cours='bio_1'
                         if classe.carnet_cotes[eleve].grille_horaire['bio_1'].evaluation==1:#je rajoute cette ligne car en cas d'échec forcé via la fct_sciences6 l'évaluation passe à 1
                             nom_cours='bio_1'
                         if classe.carnet_cotes[eleve].grille_horaire['bio_2'].points!=False:
                             nom_cours='bio_2'
                         if nom_cours=='bio':
                             QMessageBox.warning(gui,'Erreur',"<div><p> L'élève %s n'a de points ni en bio 1 ni en bio 2.</p></div>"%eleve)
                     except KeyError :
                         pass
                 if nom_cours=='phys' :
                     try: 
                         classe.carnet_cotes[eleve].grille_horaire['phys_1'].points
                         classe.carnet_cotes[eleve].grille_horaire['phys_2'].points
                         classe.carnet_cotes[eleve].grille_horaire['phys_1'].appreciation
                         classe.carnet_cotes[eleve].grille_horaire['phys_2'].appreciation
                         if classe.carnet_cotes[eleve].grille_horaire['phys_1'].appreciation!=False:
                             nom_cours='phys_1'
                         if classe.carnet_cotes[eleve].grille_horaire['phys_2'].appreciation!=False:
                             nom_cours='phys_2'
                         if classe.carnet_cotes[eleve].grille_horaire['phys_1'].points!=False:
                             nom_cours='phys_1'
                         if classe.carnet_cotes[eleve].grille_horaire['phys_1'].evaluation==4:
                             nom_cours='phys_1'
                         if classe.carnet_cotes[eleve].grille_horaire['phys_1'].evaluation==1:#je rajoute cette ligne car en cas d'échec forcé via la fct_sciences6 l'évaluation passe à 1
                             nom_cours='phys_1'
                         if classe.carnet_cotes[eleve].grille_horaire['phys_2'].points!=False:
                             nom_cours='phys_2'
                         if nom_cours=='phys':
                             QMessageBox.warning(gui,'Erreur',"<div><p> L'élève %s n'a de points ni en phys 1 ni en phys 2.</p></div>"%eleve)
                     except KeyError :
                         pass
                 if classe.carnet_cotes[eleve].grille_horaire[nom_cours].points!=False:
                     points=str(classe.carnet_cotes[eleve].grille_horaire[nom_cours].points)
                 elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].appreciation!=False:
                     points=classe.carnet_cotes[eleve].grille_horaire[nom_cours].appreciation
                 elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].certif_med==True:
                     points='cm'
                 else:
                     points=''
                 if classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==0:
                     couleur='{{'
                 elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==1:
                     couleur='\\scriptsize \\centering \\textcolor{rouge} {\\underline{\\scshape '
                 elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==2:
                     couleur='\\scriptsize \\centering \\textcolor{orange} { { \\scshape '
                 elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==3:
                     couleur='\\scriptsize \\centering \\textcolor{vert} { { \\scshape '
                 elif classe.carnet_cotes[eleve].grille_horaire[nom_cours].evaluation==4:
                     couleur='\\scriptsize \\centering{{'
                 ligne.append(couleur+points+'}}')
             if classe.noel==True:
                 txt_noel=str(classe.carnet_cotes[eleve].noel)
                 ligne.append(txt_noel)
             #
             if classe.mars==True:
                 txt_mars=str(classe.carnet_cotes[eleve].mars)
                 ligne.append(txt_mars)
             #
             txt_heures_echec=str(classe.carnet_cotes[eleve].heures_echec_tot)+' / '\
                 +str(classe.carnet_cotes[eleve].vol_horaire_ccnc)
             ligne.append('\\tiny '+txt_heures_echec)
                 #
             txt=str(classe.carnet_cotes[eleve].moy_pond_ccnc )
             if classe.carnet_cotes[eleve].moy_pond_ccnc <50:
                 cell=('\\scriptsize \\textcolor{rouge}{'+txt+'}')
             elif classe.carnet_cotes[eleve].moy_pond_ccnc <60:
                 cell=('\\scriptsize \\textcolor{orange}{'+txt+'}')
             else:
                 cell=('\\scriptsize \\textcolor{vert}{'+txt+'}')
             if classe.analyse['fct_moyenne_ponderee']==True: #n'existe pas en mars
                 ligne.append(cell)
                 #
             if classe.carnet_cotes[eleve].situation_globale ==3:
                 cell_situation_globale='\\cellcolor{vert}{}'
             elif classe.carnet_cotes[eleve].situation_globale ==1:
                 cell_situation_globale='\\cellcolor{rouge}{}'
             elif classe.carnet_cotes[eleve].situation_globale ==2:
                 cell_situation_globale='\\cellcolor{orange}{}'
             elif classe.carnet_cotes[eleve].situation_globale ==4:
                 cell_situation_globale='\\cellcolor{gris_fonce}{}'
             else:
                 cell_situation_globale='\\{}'
             ligne.append(cell_situation_globale)    
             list_file.append((' & '.join(ligne))+"\\\\ [1.5em]")
             list_file.append("\\hline")
         
         list_file.append("\\end{tabular}")
         list_file.append("\\end{document}")
         
         doc_name=self.file_name+'_tableau.tex'
         doc_name=QFileDialog.getSaveFileName(gui,'Sauver tableau récapitulatif',doc_name,"Document TEX (*.tex)")
         #self.document.save(target=doc_name, pretty=True)
         gui.current_dir=os.path.dirname(doc_name)
         f = open(doc_name,'w')
         for ligne in list_file:
             f.write(ligne+' \n')
         f.close()
         if platform.system()=='Linux':
             try:
                 prog=QProgressDialog()
                 prog.setWindowFlags(Qt.SplashScreen)
                 prog.setCancelButton(None)
                 prog.setLabelText ('Tableau => pdf')
                 for i in range(50):
                     prog.setValue(i)
                     prog.show()
                     QApplication.processEvents()
                 proc=subprocess.Popen(['pdflatex','-output-directory',os.path.dirname(doc_name),doc_name])
                 proc.wait()
                 for i in range(51):
                     prog.setValue(50+i)
                     prog.show()
                     QApplication.processEvents()
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_tableau.aux')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_tableau.log')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_tableau.tex')
             except Exception as e:
                 QMessageBox.critical(gui,'Echec',"La création du document pdf a échoué, vérifiez que pdflatex est bien installé sur cet ordinateur.")
                 print ('Erreur : %s' % e)
                 print (traceback.format_exc())
         if platform.system()=='Windows':
             try:
                 prog=QProgressDialog()
                 prog.setWindowFlags(Qt.SplashScreen)
                 prog.setCancelButton(None)
                 prog.setLabelText ('Tableau => pdf')
                 for i in range(50):
                     prog.setValue(i)
                     prog.show()
                     QApplication.processEvents()
                 proc=subprocess.Popen(['pdflatex','-output-directory',os.path.dirname(doc_name),doc_name])
                 proc.wait()
                 for i in range(51):
                     prog.setValue(50+i)
                     prog.show()
                     QApplication.processEvents()
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_tableau.aux')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_tableau.log')
                 os.remove(os.path.dirname(doc_name)+'/'+self.file_name+'_tableau.tex')
             except Exception as e:
                 QMessageBox.critical(gui,'Echec',"La création du document pdf a échoué, vérifiez que pdflatex est bien installé sur cet ordinateur.")
                 print ('Erreur : %s' % e)
                 print (traceback.format_exc())
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
             if self.points==0.0 : self.points=0.1
             if self.points!=int(self.points):
                 self.points=round(self.points,1)
             else :
                 self.points=int(self.points)
#
#
if __name__=="__main__":
     #saveout = sys.stdout
     #fsock = open('out.log', 'w')
     #sys.stdout = fsock
     app = QApplication(sys.argv)
     
     compfr=Compfr()
     classe=Classe()
     
     gui=Gui()
     #gui.splashscreen()
     gui.show()
     app.exec_()
     #fsock.close()
     
