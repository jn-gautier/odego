from PyQt6.QtCore import QObject, pyqtSignal as Signal

from models.cours import Cours
from models.criteres import Criteres
import xml.etree.ElementTree as ET
import traceback
import copy
import json

class Classe(QObject):
    messagebox = Signal(str, str, str)

    def __init__(self,parent=None):
        super().__init__(parent)

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
        self.analyse['fct_selfment_cours']=0
        self.analyse['fct_selfment_cours_app']=0
        self.analyse['fct_age']=0
        self.analyse['fct_sciences6']=0
        self.analyse['fct_sciences6_mars']=0
        self.analyse['fct_prop_echec']=0
        self.analyse['fct_daca']=0
        self.analyse['fct_daca_mars']=0
        self.analyse['fct_moyenne_ponderee_cg']=0
        self.analyse['fct_daca_ep_3tq']=0
        self.analyse['fct_daca_ep_4tq']=0
        self.analyse['fct_daca_ep_5tq']=0
        self.analyse['fct_daca_ep_6tq']=0
        self.ctg=False
        self.ddn=False
        self.pia=False
        self.noel=False
        self.mars=False
     #   
    def set_param(self,niveau="",section="",delibe=""):
         """ """
         self.niveau=niveau
         self.section=section
         self.delibe=delibe
         self.niv_sec=self.niveau+self.section
         liste_carac_bool=['ccnc','verrou','pseudo','option']
         liste_carac_int=['heures']
         liste_carac_str=['abr','intitule']
         #
         try:
             tree = ET.parse('./config/cours.xml')
             for niveau in tree.iter('niveau'):
                 if niveau.get('name')==self.niv_sec:
                     tree_niveau=niveau
                     break
             #
             for node_cours in tree_niveau:
                 cours=Cours()
                 for carac in liste_carac_bool:
                     setattr(cours, carac, bool(int(node_cours.find(carac).text)))
                 for carac in liste_carac_int:
                     setattr(cours, carac, float(node_cours.find(carac).text))
                 for carac in liste_carac_str:
                     valeure=node_cours.find(carac).text
                     setattr(cours, carac, valeure)
                 # fusion de cours venant d'être créé avec celui présent dans la grille horaire de chaque élève de la self
                 for eleve in self.carnet_cotes.values():
                     if cours.abr.lower() not in eleve.grille_horaire.keys():
                         eleve.grille_horaire[cours.abr.lower()]=Cours()
                     for carac in liste_carac_bool+liste_carac_int+liste_carac_str:
                         setattr(eleve.grille_horaire[cours.abr.lower()],carac,getattr(cours,carac))
                     
             print ("Création d'une self de", self.niv_sec)

         except Exception as e:
             self.messagebox.emit('Echec', "Erreur dans la lecture du fichier de description des cours.","critical")
             print ('Erreur dans la lecture du fichier de description des cours')
             print ('Erreur : %s' % e)
             print (traceback.format_exc())
         #
         try:
             tree = ET.parse('./config/criteres.xml')
             for niveau in tree.iter('niveau'):
                 if niveau.get('name')==self.niv_sec:
                     tree_niveau=niveau
                     break
             self.criteres=Criteres()
             for node_critere in tree_niveau:
                 setattr(self.criteres, node_critere.tag,int(node_critere.text))
         except Exception as e:
             self.messagebox.emit('Echec', "Erreur dans la lecture du fichier de description des critères.","critical")
             print ('Erreur dans la lecture du fichier de description des critères.')
             print ('Erreur : %s' % e)
             print (traceback.format_exc())
         #
         try:
             tree = ET.parse('./config/analyses.xml')
             for niveau in tree.iter('niveau'):
                 if niveau.get('name')==self.niv_sec:
                     tree_niveau=niveau
                     break
             for delibe in tree_niveau.iter('delibe'):
                 print(delibe.get('name'))
                 if delibe.get('name')==self.delibe:
                    tree_delibe=delibe
                    break
             for analyse in tree_delibe:
                 self.analyse[analyse.tag]=bool(int(analyse.text))
                 
         except Exception as e:
             self.messagebox.emit('Echec', "Erreur dans la lecture du fichier des analyses à effectuer.","critical")
             print ('Erreur dans la lecture du fichier des analyses à effectuer.')
             print ('Erreur : %s' % e)
             print (traceback.format_exc())
         #
    
    def stats_elv(self):
        for eleve in self.carnet_cotes.values():
            eleve.fct_dispense()
            
            if self.analyse['fct_daca_ep_3tq']==True:
                eleve.fct_daca_3tq()
            if self.analyse['fct_daca_ep_4tq']==True:
                eleve.fct_daca_4tq()
            if self.analyse['fct_daca_ep_5tq']==True:
                eleve.fct_daca_5tq()
            if self.analyse['fct_daca_ep_6tq']==True:
                eleve.fct_daca_6tq()
            if self.analyse['fct_sciences6']==True:
                eleve.fct_sciences6()
            if self.analyse['fct_points_sup_100']==True:
                eleve.fct_points_sup_100()
            if self.analyse['fct_moyenne_ponderee']==True:
                eleve.fct_moyenne_ponderee()
            if self.analyse['fct_echec_inf35']==True:
                eleve.fct_echec_inf35()
            if self.analyse['fct_nb_heures_horaire']==True:
                eleve.fct_nb_heures_horaire()
            if self.analyse['fct_total_heures_echec']==True:
                eleve.fct_total_heures_echec()
            if self.analyse['fct_cours_verrou_echec']==True:
                eleve.fct_cours_verrou_echec()
            if self.analyse['fct_nb_cours_echec']==True:
                eleve.fct_nb_cours_echec()
            if self.analyse['fct_echec_contrat']==True:
                eleve.fct_echec_contrat()
            if self.analyse['fct_certif_med']==True:
                eleve.fct_certif_med()
            if self.analyse['fct_oubli_cours']==True:
                eleve.fct_oubli_cours()
            if self.analyse['fct_credits_inf_50']==True:
                eleve.fct_credits_inf_50()
            if self.analyse['fct_echec_travail']==True:
                eleve.fct_echec_travail()
            if self.analyse['fct_selfment_cours']==True:
                eleve.fct_classement_cours()
            if self.analyse['fct_age']==True:
                eleve.fct_age()
            if self.analyse['fct_prop_echec']==True:
                eleve.fct_prop_echec()
            if self.analyse['fct_moyenne_ponderee_cg']==True:
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
                if eleve.liste_certif_med!='éducation physique':
                    eleve.situation_globale=4 # non délibérable
            
            #if eleve.liste_oubli_cours!='':
                #eleve.situation_globale=4 # non délibérable
     #
     #
    def prod_liste_eleves(self):
        self.liste_eleves=self.carnet_cotes.keys()
     #
    def update_liste_cours(self):
        """Cette fonction produit une liste des cours ne contenant que les cours évalués pour au moins un élève de la self"""
        with open('./UI/config/liste_cours.json') as json_file:
            dict_list_cours = json.load(json_file)    
        liste_cours_annee=dict_list_cours[self.niv_sec]
        
        self.liste_cours=[]
        
        for eleve in self.carnet_cotes.values():
            for cours in eleve.grille_horaire.keys():
                
                if eleve.grille_horaire[cours].evaluation!=0:
                    #if cours==('chim_1' or 'chim_2'): cours='chim'
                    #if cours==('phys_1' or 'phys_2'): cours='phys'
                    #if cours==('bio_1'  or 'bio_2' ): cours='bio'
                    if cours not in self.liste_cours :
                        self.liste_cours.append(cours)
        self.liste_cours=sorted(self.liste_cours, key=lambda cours : liste_cours_annee.index(cours))