#! /usr/bin/python
# -*- coding: utf-8 -*- 

#from xml.dom.minidom import parse
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
from datetime import date
from datetime import datetime
from functools import cmp_to_key
import copy
import xml.etree.ElementTree as ET


class Gui(QDialog):
     def __init__(self, parent=None):
         super(Gui, self).__init__(parent)
         #
         niveau=['1', '2', '3', '4', '5', '6']
         classes=['','a','b','c','d','e','f','g','h','i','j','k','l','m','z !?!?']
         sections=['GT','TQ']
         delibe=[u'Noël',u'Mars',u'Juin']
         now=date.today()
         
         annee=[str(now.year-2),str(now.year-1),str(now.year),str(now.year+1),str(now.year+2)]
         #
         layout=QHBoxLayout()
         grid=QGridLayout()
         self.fname=False
         self.fichier_valide=False
         self.combo_niveau=QComboBox()
         self.combo_niveau.addItems(niveau)
         self.combo_classes=QComboBox()
         self.combo_classes.addItems(classes)
         self.combo_section=QComboBox()
         self.combo_section.addItems(sections)
         self.combo_delib=QComboBox()
         self.combo_delib.addItems(delibe)
         self.combo_annee=QComboBox()
         self.combo_annee.addItems(annee)
         self.boutton_quit=QDialogButtonBox(QDialogButtonBox.Close)
         self.boutton_ok=QDialogButtonBox(QDialogButtonBox.Ok)
         self.file_to_open=QLineEdit(u"Sélectionnez le fichier.")
         self.open_file=QPushButton("Ouvrir...")
         self.radio1=QCheckBox(u"Tableau récapitulatif")
         self.radio2=QCheckBox(u"Analyse detaillée")
         self.radio3=QCheckBox("Classement")
         self.groupbox=QGroupBox("Analyses")
         self.groupbox.setFlat(True)
         line=QFrame()
         line.setFrameStyle(QFrame.VLine)
         #self.boutton_ok.setStatusTip('Open new File')
         #
         grid.addWidget(QLabel( u"Niveau :" ),0,0)
         grid.addWidget(QLabel( u"Classe :" ),1,0)
         grid.addWidget(QLabel( u"Section :" ),2,0)
         grid.addWidget(QLabel( u"Delibé :" ),3,0)
         grid.addWidget(QLabel( u"Fichier :" ),4,0)
         grid.addWidget(self.boutton_ok,6,0)
         #
         grid.addWidget(self.combo_niveau,0,1)
         grid.addWidget(self.combo_classes,1,1)
         grid.addWidget(self.combo_section,2,1)
         grid.addWidget(self.combo_delib,3,1)
         grid.addWidget(self.combo_annee,3,2)
         grid.addWidget(self.file_to_open,4,1)
         #v_layout2.addLayout(h_layout8)
         grid.addWidget(self.open_file,5,1)
         grid.addWidget(self.boutton_quit,6,1)
         
         layout.addLayout(grid)
         
         v_layout=QVBoxLayout()
         v_layout.addWidget(self.radio1)
         v_layout.addWidget(self.radio2)
         v_layout.addWidget(self.radio3)
         v_layout.addStretch(1)
         self.groupbox.setLayout(v_layout)
         # 
         #h_layout.addLayout(v_layout1)
         #h_layout.addLayout(v_layout2)
         layout.addWidget(line)
         layout.addWidget(self.groupbox)
         #
         self.setLayout(layout)
         self.setWindowTitle(u'Odego : un guide pour les délibérations')
         self.combo_annee.setCurrentIndex(2)
         if now.month in [10,11,12,1]:
             self.combo_delib.setCurrentIndex(0)
         if now.month in [2,3,4,5]:
             self.combo_delib.setCurrentIndex(1)
         if now.month in [6,7,8,9]:
             self.combo_delib.setCurrentIndex(2)
         self.connect(self.boutton_quit.button(QDialogButtonBox.Close), SIGNAL("clicked()"),self.appExit)
         self.connect(self.boutton_ok.button(QDialogButtonBox.Ok), SIGNAL("clicked()"),self.pre_traitmt)
         self.connect(self.open_file, SIGNAL("clicked()"),self.select_file)
     #
     def appExit(self):
         print "Au revoir!"
         app.quit()
     #
     def pre_traitmt(self):
         self.verif_fichier()
         if self.fichier_valide==True:
             self.fichier_a_traiter=self.fname
             self.creer_tableau_recap=self.radio1.isChecked()
             self.creer_analyse_eleve=self.radio2.isChecked()
             self.creer_classement=self.radio3.isChecked()
             self.niveau=unicode(self.combo_niveau.currentText(),'utf-8')
             self.section=unicode(self.combo_section.currentText(),'utf-8')
             self.classe=unicode(self.combo_classes.currentText(),'utf-8')
             self.annee=unicode(self.combo_annee.currentText(),'utf-8')
             self.delibe=unicode(self.combo_delib.currentText(),'utf-8')
             self.path=(split(str(self.fname)))[0]
             self.file_sauv=self.delibe+"_"+self.annee+"_"+self.niveau+self.section+self.classe
             self.titre='Conseil de classe '+self.niveau+self.section+self.classe+" - "+self.delibe+' '+self.annee
             #
             #global classe
             try:
                 classe.__init__(self.niveau,self.section,self.fichier_a_traiter)
                 classe.prod_carnet_cotes()
                 classe.stats_elv()
                 classe.prod_situation_globale()
                 classe.prod_liste_eleves()
                 if ((self.niveau=='1') or (self.niveau=='2')) & (self.section=='GT') & (self.delibe==u'Noël'):
                     self.traitement_1deg_gt_noel()
                 if ((self.niveau=='1') or (self.niveau=='2')) & (self.section=='GT') & (self.delibe==u'Mars'):
                     self.traitement_1deg_gt_mars()
                 if ((self.niveau=='1') or (self.niveau=='2')) & (self.section=='GT') & (self.delibe==u'Juin'):
                     self.traitement_1deg_gt_juin()
                 if ((self.niveau=='3') or (self.niveau=='4')) & (self.section=='GT') & (self.delibe==u'Noël'):
                     self.traitement_2deg_gt_noel()
                 if ((self.niveau=='3') or (self.niveau=='4')) & (self.section=='GT') & (self.delibe==u'Mars'):
                     self.traitement_2deg_gt_mars()
                 if ((self.niveau=='3') or (self.niveau=='4')) & (self.section=='GT') & (self.delibe==u'Juin'):
                     self.traitement_2deg_gt_juin()
             except Exception, e:
                 QMessageBox.warning(self,'Erreur',u"<div><p> Un problème a été rencontré lors du traitement de votre fichier</p>\
                 <ul><li>Vérifiez que le fichier sélectionné contienne bien des <b>points</b>.</li>\
                 <li>Vérifiez que le fichier sélectionné contienne bien le <b>nom des cours</b>.</li>\
                 <li>Vérifiez que vous avez sélectionné la bonne <b>classe </b>et la bonne <b>section </b>dans le menu d'acceuil.</li></ul>\
                 </div>")
                 print 'Erreur : %s' % e
                 print 'Ligne ', sys.exc_traceback.tb_lineno 
             
     #
     def select_file(self):
         self.fname = QFileDialog.getOpenFileName(self,'Tableau au format ods avec les points de la classe.','/home/gautier/dossier_ivf/odego/')
         self.file_to_open.setText(self.fname)
     #
     def verif_fichier(self):
         ext=self.fname.split('.')
         ext=ext[len(ext)-1]
         if (self.fname!=False) & (ext=='ods'):
             self.fichier_valide=True
         else:
             QMessageBox.warning(self,u'Fichier invalide',u'Veuillez renseigner un fichier ods valide.',)
     #
     def traitement_1deg_gt_noel(self):
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
     #
     def traitement_1deg_gt_mars(self):
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
     #
     def traitement_1deg_gt_juin(self):
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
     #
     def traitement_2deg_gt_noel(self):
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
     #
     def traitement_2deg_gt_mars(self):
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
     #
     def traitement_2deg_gt_juin(self):
         try:
             if self.creer_analyse_eleve==True:
                 analyse=Odf_file(doc_type="analyse",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 analyse.analyse_eleve()
                 del analyse
                 #
             if self.creer_tableau_recap==True:
                 tableau=Odf_file(doc_type="tableau_recap",titre=self.titre,path=self.path,file_name=self.file_sauv)
                 tableau.tableau_recap()
                 del tableau
             if (self.creer_analyse_eleve or self.creer_tableau_recap)==True:
                 QMessageBox.information(self,u'Terminé',u"Les données ont été traitées avec succès!")
         except Exception, e:
             QMessageBox.warning(self,u'Erreur',u"Un ou plusieurs documents demandés n'ont pas été produits")
             print 'Erreur : %s' % e
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


def nettoie_point(point):
     chaine = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','.',',']
     point = [val for val in point if val in chaine]
     point=''.join(point)
     if point=='':
         point=False
     if point!=False:
         point=float(point)
         if point!=int(point):
             point=round(point,1)
         else :
             point=int(point)
     return point


class Classe(object):
     #
     def __init__(self,niveau="",section="",fichier_a_traiter=""):
         self.niveau=niveau
         self.section=section
         self.niv_sec=self.niveau+self.section
         self.carnet_cotes={}
         self.liste_cours=[]
         self.grille_horaire={}
         self.fichier_a_traiter=fichier_a_traiter
         
         #
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
                 self.grille_horaire[cours.abr]=cours
             print "Création d'une classe de", self.niv_sec
         except Exception, e:
             QMessageBox.fatal(gui,u'Echec',u"Erreur dans la lecture du fichier de description des cours.")
             print'Erreur dans la lecture du fichier de description des cours'
             print 'Erreur : %s' % e
             print sys.exc_traceback.tb_lineno 
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
             QMessageBox.fatal(gui,u'Echec',u"Erreur dans la lecture du fichier de description des critères.")
             print'Erreur dans la lecture du fichier de description des critères.'
             print 'Erreur : %s' % e
             #print sys.exc_traceback.tb_lineno 
     #
     #
     def prod_carnet_cotes(self):
     #
         doc = odf_get_document(str(self.fichier_a_traiter))
         
         body=doc.get_body()
         table=body.get_tables()[0]
         table.rstrip()
         #
         try:
             ligne_cours=False
             for row in table.get_rows():
                 prem_cell=row.get_cell(0).get_value()
                 if prem_cell!=None:
                     if (prem_cell.lower()=='cours'):
                         ligne_cours=True
                         for cell in row.get_cells():
                             if cell.get_value()!=None: #il peut y avoir des cellules vides qui suivent celles avec les intitulés des cours ; on ne prend en compte que les cellules non vides.
                                 self.liste_cours.append(cell.get_value())
                         del self.liste_cours[0]
             if ligne_cours==False:
                 raise ExceptionPasCours
         except ExceptionPasCours :
             QMessageBox.fatal(gui,'Echec',u"<p>Il n'y a pas de ligne avec les cours dans votre fichier</p> <p>ou celle-ci n'est pas indiquée par le mot 'Cours'</p>")
             print "Il n'y a pas de ligne avec les cours dans votre fichier, ou celle-ci n'est pas indiquée par le mot 'Cours'"
         for row in table.get_rows():
             prem_cell=row.get_cell(0).get_value()
             if (prem_cell==None) or ( (prem_cell[0]=='&') & (prem_cell[1]=='&') or (prem_cell.lower()=='cours')):
                 pass
             else:
                 eleve=Eleve()
                 eleve.grille_horaire=copy.deepcopy(self.grille_horaire)
                 eleve.nom=row.get_cell(0).get_value().encode('utf-8')
                 ligne_points=row.get_cells()
                 del ligne_points[0]
                 for cours,cell in zip(self.liste_cours,ligne_points):
                     points_eleve=cell.get_value()
                     #
                     if (cours.lower()=='pia') & (points_eleve!=None):
                         eleve.pia=True
                         self.liste_cours.remove('PIA')
                     #
                     elif (cours.lower()=='ctg') & (points_eleve!=None):
                         eleve.ctg=True
                         self.liste_cours.remove('CTG')
                     #
                     elif (cours.lower()=='ddn') & (points_eleve!=None):
                         print 'DDN' , points_eleve
                         eleve.ddn=points_eleve
                     #
                     else:
                         try:
                             if points_eleve==None:
                                 points_eleve=False
                             eleve.grille_horaire[cours.lower()].analyse_points(str(points_eleve))
                             if eleve.grille_horaire[cours.lower()].points!=False:
                                 eleve.eval_certif=True
                         except Exception, e:
                             QMessageBox.warning(gui,'Erreur',u"<p>Une erreur a été rencontrée dans l'encodage d'une évaluation.</p> <p>Cette évaluation sera ignorée.</p>")
                             print ("Une erreur a été rencontrée dans l'encodage d'une évaluation.")
                             print ("Cette évaluation sera ignorée.")
                             print 'Erreur : %s' % e
                             print sys.exc_traceback.tb_lineno 
                     print eleve.nom , cours.lower(), points_eleve
                 self.carnet_cotes[eleve.nom]=eleve
                 #print eleve, ligne_points
                 del eleve
                 del ligne_points
         del doc
         del body
         del table
         if 'DDN' in self.liste_cours:
             self.liste_cours.remove('DDN')
         if 'CTG' in self.liste_cours:
             self.liste_cours.remove('CTG')
         if 'PIA' in self.liste_cours:
             self.liste_cours.remove('PIA')
         print 'Liste des cours : ' , self.liste_cours
     #
     #
     def stats_elv(self):
         for eleve in self.carnet_cotes.itervalues():
             eleve.moyenne_ponderee()
             eleve.nombre_heures_horaire()
             eleve.total_heures_echec()
             eleve.cours_verrou_echec()
             eleve.echec_inf35()
             eleve.nb_cours_echec()
             eleve.echec_contrat()
             eleve.certif_med()
             eleve.oubli_cours()
             eleve.calc_credits_inf_50()
             eleve.echec_travail()
             eleve.classement_cours()
             eleve.age()
     #
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


class Eleve(Classe):
     #
     def __init__(self):
         self.PIA=False
         self.CTG=False
         self.DDN=False
         self.eval_certif=False
         self.vol_horaire_cc=0
         self.vol_horaire_ccnc=0
         self.moy_pond_cc=0
         self.moy_pond_ccnc=0
         self.heures_echec_cc=0
         self.heures_echec_nc=0
         self.nb_cours_cc_echec=0
         self.nb_cours_nc_echec=0
         self.credits_inf_50=0
         self.situation_globale=0
     #
     #
     def nombre_heures_horaire(self):
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
     def moyenne_ponderee(self):
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
         self.moy_pond_cc=round((self.moy_pond_cc/total_heures_cc),1)
         self.moy_pond_ccnc=round((self.moy_pond_ccnc/total_heures_ccnc),1)
         del total_heures_cc, total_heures_ccnc
     #
     #
     def total_heures_echec(self): 
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
     def cours_verrou_echec(self):
         """Cette fonction calcule, pour un eleve:
           => le nom des cours verrou en échec,
           => le nombre de cours verrou en échec"""
         liste_cours_verrou=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.verrou==True) & (cours.evaluation==1):
                 liste_cours_verrou.append(cours.intitule)
         self.liste_cours_verrou_echec=", ".join(liste_cours_verrou)
         self.nb_cours_verrou_echec=len(liste_cours_verrou)
         del liste_cours_verrou
     #
     #
     def echec_inf35(self):
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
         del liste_cours_inf35
     #
     #
     def nb_cours_echec(self):
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
     def echec_contrat(self):
         liste_echec_contrat=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.contrat==True) & (cours.evaluation==1):
                 liste_echec_contrat.append(cours.intitule)
         self.liste_echec_contrat=", ".join(liste_echec_contrat)
         del liste_echec_contrat
     #
     #
     def certif_med(self):
         liste_certif_med=[]
         for cours in self.grille_horaire.itervalues():
             if cours.certif_med==True:
                 liste_certif_med.append(cours.intitule)
         self.liste_certif_med=", ".join(liste_certif_med)
         del liste_certif_med
     #
     #
     def oubli_cours(self):
         liste_oubli_cours=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.evaluation==0) & (cours.option==False) & (cours.certif_med==False):
                 liste_oubli_cours.append(cours.intitule)
         self.liste_oubli_cours=", ".join(liste_oubli_cours)
         del liste_oubli_cours
     #
     #
     def calc_credits_inf_50(self):
         ecart=0
         ecart_pondere=0
         for cours in self.grille_horaire.itervalues():
             if (cours.points!=False) & (cours.ccnc==True): 
                 if(int(cours.points)<50):
                     ecart=50-(int(cours.points))
                     ecart_pondere=ecart*(cours.heures)
                     self.credits_inf_50+=ecart_pondere
         del ecart, ecart_pondere
     #
     #
     def echec_travail(self):
         liste_echec_travail=[]
         for cours in self.grille_horaire.itervalues():
             if (cours.evaluation==1) & (cours.echec_travail==True) : 
                 liste_echec_travail.append(cours.intitule)
         self.liste_echec_travail=", ".join(liste_echec_travail)
         del liste_echec_travail
     #
     #
     def classement_cours(self):
         liste_35_50=[]
         liste_50_60=[] 
         liste_60_70=[]
         liste_70_80=[]
         liste_inf35=[] 
         liste_sup80=[]
         self.classement_cours={}
         for cours in self.grille_horaire.itervalues():
             if cours.points!=False:
                 if (cours.points<35):
                     liste_inf35.append(cours.abr+" : "+str(cours.points))
                 elif 35 <= cours.points < 50:
                     liste_35_50.append(cours.abr+" : "+str(cours.points))
                 elif 50 <= cours.points < 60:
                     if cours.echec_force==True:
                         liste_50_60.append(cours.abr+" : "+str(cours.points)+"!")
                     else:
                         liste_50_60.append(cours.abr+" : "+str(cours.points))
                 elif 60 <= cours.points < 70 :
                     if cours.echec_force==True:
                         liste_60_70.append(cours.abr+" : "+str(cours.points)+"!")
                     else:
                         liste_60_70.append(cours.abr+" : "+str(cours.points))
                 elif 70 <= cours.points <80 :
                         if cours.echec_force==True:
                             liste_70_80.append(cours.abr+" : "+str(cours.points)+"!")
                         else:
                             liste_70_80.append(cours.abr+" : "+str(cours.points))
                 elif cours.points>=80 :
                     if cours.echec_force==True:
                         liste_sup80.append(cours.abr+" : "+str(cours.points)+"!")
                     else:
                         liste_sup80.append(cours.abr+" : "+str(cours.points))
         self.classement_cours['0=>35[']=" ; ".join(liste_inf35)
         self.classement_cours['35=>50[']=" ; ".join(liste_35_50)
         self.classement_cours['50=>60[']=" ; ".join(liste_50_60)
         self.classement_cours['60=>70[']=" ; ".join(liste_60_70)
         self.classement_cours['70=>80[']=" ; ".join(liste_70_80)
         self.classement_cours['80=>100]']=" ; ".join(liste_sup80)
     #
     def age(self):
         try :
             self.ddn=datetime.strptime(self.ddn, '%d/%m/%Y').date()
         except TypeError :
             self.ddn=self.ddn.date()
         age=date.today()-self.ddn
         mois=age.days/30
         self.age_str=str(mois/12)+' ans '+str(mois % 12)+' mois'
         self.age=float(mois)/12
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
     #
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
             points=nettoie_point(points)# rappel: la fonction nettoie_point converti également les points en float
             self.points=points
             if points<50:
                 self.evaluation=1
             elif (points>=50) & (points<60) & (self.echec_force==False):
                 self.evaluation=2
             elif (points>=60) & (self.echec_force==False):
                 self.evaluation=3
             else:
                 pass

class Criteres(Classe):
     #
     def __init__(self):
         self.heures_echec_max=0
         self.cours_verrou_echec_max=0
         self.echec_sur_exclusion_max=0
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
             nom_table=unicode(nom_eleve.replace("'",''),'utf-8')
             table=odf_create_table(nom_table,style='style_table')
             remarque=' ('+str(eleve.vol_horaire_ccnc )+'p./sem)'
             if eleve.situation_globale==1 or 4:
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
             if (eleve.pia )!="":
                 table=self.creer_ligne_2cell(table,"Remarque","L'élève dispose d'un PIA" )
             if (eleve.ctg )!="":
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
                 ligne.append(odf_create_cell(unicode(eleve,'utf-8'),style='noms'))
                 for nom_cours in classe.liste_cours:
                     nom_cours=nom_cours.lower()
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





if __name__=="__main__":
     compfr=Compfr()
     classe=Classe.__new__(Classe)#la classe est créée avec new pour pouvoir être initialisée 
     # dans la class Gui et réutilisée dans la class Odf_file sans passer par une variable globale
     app = QApplication(sys.argv)
     gui=Gui()
     gui.show()
     app.exec_()
     

# completement dissocier l'analyse et la production du document, cad dans la prod du document, faire des tests du type if critere_cours_verrou_echec=0/1/2 et faire une fonction d'analyse générale if nb_cours_verrou_echec>nb_cours_verrou_echec_max alors 2
#ajouter la possibilité d'importer les points depuis un fichier xsl ou xslx
# dans le tableau recap, supprimer les colonnes pour lesquelles il n'y a pas de points
# mettre une ligne sur deux en gris clair
# 

# changer le gui : faire un système ave une grille à remplir type tableur avec la possibilité de la remplir à partir d'un fichier ods
# sur le côté mettre le panneau avec le chaoix classe, année, ...
# au dessus, les butons OK, quitter, nouveau, a propos

