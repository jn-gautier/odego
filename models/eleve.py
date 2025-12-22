from datetime import date , datetime
from PyQt6.QtCore import QObject, pyqtSignal as Signal

import copy
import traceback

class Eleve(QObject):
     messagebox = Signal(str, str, str)
     """Un élève est un membre d'une classe, il possède un nom, une grille horaire avec des points et un ensemble de
     statistiques relatives à ces points."""
     def __init__(self,parent=None):
         super().__init__(parent)
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
                     print("Erreur")
                     self.messagebox.emit('Erreur',f"<div><p>L'élève {self.nom} a une cote supérieure à 100.</p> <p> {cours.intitule} : {cours.points}</p></div>","warning" )
     #
     def fct_dispense(self):
         for cours in self.grille_horaire.values():
             if cours.evaluation==5:
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
         self.vol_horaire_ccnc=int(self.vol_horaire_ccnc)
         if self.vol_horaire_ccnc < 30:
             self.messagebox.emit("Erreur",f"<p>L'élève {self.nom} a un volume horaire inférieur à 30p./sem.</p> <p>Vérifiez s'il ne manque pas de points</p>","warning")
             print("Erreur horaire <30h")
         if self.vol_horaire_ccnc > 40:
            print("Erreur horaire >40")
            self.messagebox.emit("Erreur",f"<p>L'élève {self.nom} a un volume horaire supérieur à 40p./sem.</p> <p>Vérifiez si les points sont convenablement encodés.</p>","warning")
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
            
            if (cours.points!=False) & (cours.pseudo==False):
                self.moy_pond_ccnc+=cours.heures*cours.points
                total_heures_ccnc+=cours.heures
        try :
            self.moy_pond_cc=round((self.moy_pond_cc/total_heures_cc),1)
        except ZeroDivisionError :
            self.moy_pond_cc=0
        try:    
            self.moy_pond_ccnc=round((self.moy_pond_ccnc/total_heures_ccnc),1)
        except ZeroDivisionError :
            self.moy_pond_ccnc=0
            
        
     #
     #
     def fct_total_heures_echec(self): 
         """Cette fonction calcule, pour un eleve:
          => le nombre d'heures de cours certificatifs en échec,
          => le nombre d'heures de cours non-certificatifs en échec,
          => le nombre total d'heures de cours en échec."""
         for cours in self.grille_horaire.values():
             if (cours.ccnc==True) & (cours.pseudo==False) & (cours.evaluation==1) :
                 self.heures_echec_cc+=cours.heures
             if (cours.ccnc==False) & (cours.pseudo==False) &(cours.evaluation==1) :
                 self.heures_echec_nc+=cours.heures
         if (self.heures_echec_cc!=0) & (self.heures_echec_nc==0):
             self.heures_echec_tot=str(int(self.heures_echec_cc))
         elif (self.heures_echec_nc!=0):
             self.heures_echec_tot=str(int(self.heures_echec_cc))+' +('+str(int(self.heures_echec_nc))+')'
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
         print(self.liste_oubli_cours)
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
     def fct_age(self):
         """Cette fonction calcule l'age des élèves apd de leur date de naissance.
         à partir de la date reçues au format iso-8601 yyyy-mm-dd"""
         #self.ddn=self.ddn.replace('/','-')
         try:
            self.ddn=datetime.strptime(self.ddn, '%Y-%m-%d').date()
         except ValueError:   
            print ("Le format de la date de naissance de %s n'est pas pris en charge" %(self.nom))
            self.ddn=False
            self.age=False
            self.age_str=False
         except Exception as e:
            self.ddn=False
            self.age=False
            self.age_str=False
            print ("Erreur inconnue dans le traitement d'une date de naissance")
            print ('Erreur : %s' % e)
            print ('Message : ', traceback.format_exc() )
         
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
         if sc_6 & sc_3:
            print("Erreur : sc_3 et sc_6")
            self.messagebox.emit("Erreur",f"<p>L'élève {self.nom} a des points en sciences 6 et en sciences 3</p>","warning")
         elif (sc_6==False) & (sc_3==False):
            print("Erreur : ni sc_3 ; ni sc_6")
            self.messagebox.emit("Erreur",f"<p>L'élève {self.nom} n'a de points ni en sciences 6 ni en sciences 3</p>","warning")
         elif sc_6 and not sc_3 :
             nb_cours_evalues=0
             self.grille_horaire['sc_6'].points=0
             if self.grille_horaire['bio_2'].points!=False:
                 self.grille_horaire['sc_6'].points+=float(self.grille_horaire['bio_2'].points)
                 self.grille_horaire['bio']=copy.copy(self.grille_horaire['bio_2'])
                 nb_cours_evalues+=1
             if self.grille_horaire['phys_2'].points!=False:
                 self.grille_horaire['sc_6'].points+=float(self.grille_horaire['phys_2'].points)
                 self.grille_horaire['phys']=copy.copy(self.grille_horaire['phys_2'])
                 nb_cours_evalues+=1
             if self.grille_horaire['chim_2'].points!=False:
                 self.grille_horaire['sc_6'].points+=float(self.grille_horaire['chim_2'].points)
                 self.grille_horaire['chim']=copy.copy(self.grille_horaire['chim_2'])
                 nb_cours_evalues+=1
             self.grille_horaire['sc_6'].points=(self.grille_horaire['sc_6'].points)/nb_cours_evalues
             self.grille_horaire['sc_6'].points=round(self.grille_horaire['sc_6'].points,1)
             
             
             self.grille_horaire['sc_3'].points=False
             self.grille_horaire['sc_3'].evaluation=0
             
            
             
             if self.grille_horaire['sc_6'].points<50:
                 self.grille_horaire['sc_6'].evaluation=1
             if (self.grille_horaire['sc_6'].points>=50) & (self.grille_horaire['sc_6'].points<60):
                 self.grille_horaire['sc_6'].evaluation=2
             if self.grille_horaire['sc_6'].points>=60:
                 self.grille_horaire['sc_6'].evaluation=3   
             
             
         
         if sc_3 and not sc_6 :
             nb_cours_evalues=0
             self.grille_horaire['sc_3'].points=0
             if self.grille_horaire['bio_1'].points!=False:
                 self.grille_horaire['sc_3'].points+=float(self.grille_horaire['bio_1'].points)
                 self.grille_horaire['bio']=copy.copy(self.grille_horaire['bio_1'])
                 nb_cours_evalues+=1
             if self.grille_horaire['phys_1'].points!=False:
                 self.grille_horaire['sc_3'].points+=float(self.grille_horaire['phys_1'].points)
                 self.grille_horaire['phys']=copy.copy(self.grille_horaire['phys_1'])
                 nb_cours_evalues+=1
             if self.grille_horaire['chim_1'].points!=False:
                 self.grille_horaire['sc_3'].points+=float(self.grille_horaire['chim_1'].points)
                 self.grille_horaire['chim']=copy.copy(self.grille_horaire['chim_1'])
                 nb_cours_evalues+=1
             self.grille_horaire['sc_3'].points=(self.grille_horaire['sc_3'].points)/nb_cours_evalues
             self.grille_horaire['sc_3'].points=round(self.grille_horaire['sc_3'].points,1)
             
             
             if self.grille_horaire['sc_3'].points<50:
                 self.grille_horaire['sc_3'].evaluation=1
             if (self.grille_horaire['sc_3'].points>=50) & (self.grille_horaire['sc_3'].points<60):
                 self.grille_horaire['sc_3'].evaluation=2
             if self.grille_horaire['sc_3'].points>=60:
                 self.grille_horaire['sc_3'].evaluation=3   
             
             self.grille_horaire['sc_6'].points=False
             self.grille_horaire['sc_6'].evaluation=0
             
     
     #
     def fct_prop_echec(self):
         self.prop_echec=(self.heures_echec_nc+self.heures_echec_cc)/float(self.vol_horaire_ccnc)
         self.prop_echec=round(self.prop_echec*100,2)
     #
     
             
     def fct_daca_3tq(self):
         """Cette fonction calcule la moyenne pondérée des cours DACA et ED_PLAS ensemble"""
         ed_plas=self.grille_horaire['ed_plas'].points*self.grille_horaire['ed_plas'].heures
         cr=self.grille_horaire['cr'].points*self.grille_horaire['cr'].heures
         fc=self.grille_horaire['fc'].points*self.grille_horaire['fc'].heures
         d3=self.grille_horaire['3d'].points*self.grille_horaire['3d'].heures
         total_heures=self.grille_horaire['ed_plas'].heures+self.grille_horaire['cr'].heures+self.grille_horaire['fc'].heures+self.grille_horaire['3d'].heures
         
         self.grille_horaire['daca+ep'].points=(ed_plas+cr+fc+d3)/total_heures
         self.synthese_daca_ep() 

     def fct_daca_4tq(self):
         """Cette fonction calcule la moyenne pondérée des cours DACA et ED_PLAS ensemble"""
         ed_plas=self.grille_horaire['ed_plas'].points*self.grille_horaire['ed_plas'].heures
         cr=self.grille_horaire['cr'].points*self.grille_horaire['cr'].heures
         fc=self.grille_horaire['fc'].points*self.grille_horaire['fc'].heures
         d3=self.grille_horaire['3d'].points*self.grille_horaire['3d'].heures
         total_heures=self.grille_horaire['ed_plas'].heures+self.grille_horaire['cr'].heures+self.grille_horaire['fc'].heures+self.grille_horaire['3d'].heures
         
         self.grille_horaire['daca+ep'].points=(ed_plas+cr+fc+d3)/total_heures
         self.synthese_daca_ep()
         
     def fct_daca_5tq(self):
         """Cette fonction calcule la moyenne pondérée des cours DACA et ED_PLAS ensemble"""
         ed_plas=self.grille_horaire['info'].points*self.grille_horaire['info'].heures
         cr=self.grille_horaire['cr'].points*self.grille_horaire['cr'].heures
         fc=self.grille_horaire['fc'].points*self.grille_horaire['fc'].heures
         d3=self.grille_horaire['3d'].points*self.grille_horaire['3d'].heures
         total_heures=self.grille_horaire['ed_plas'].heures+self.grille_horaire['cr'].heures+self.grille_horaire['fc'].heures+self.grille_horaire['3d'].heures
         
         self.grille_horaire['daca+ep'].points=(ed_plas+cr+fc+d3)/total_heures
         self.synthese_daca_ep() 
 
         
     def fct_daca_6tq(self):
         """Cette fonction calcule la moyenne pondérée des cours DACA et ED_PLAS ensemble"""
         ed_plas_1=self.grille_horaire['photo'].points*self.grille_horaire['photo'].heures
         ed_plas_2=self.grille_horaire['anim'].points*self.grille_horaire['anim'].heures
         ed_plas=ed_plas_1+ed_plas_2

         cr=self.grille_horaire['cr'].points*self.grille_horaire['cr'].heures
         fc=self.grille_horaire['fc'].points*self.grille_horaire['fc'].heures
         d3=self.grille_horaire['3d'].points*self.grille_horaire['3d'].heures
         total_heures=self.grille_horaire['photo'].heures+self.grille_horaire['anim'].heures+self.grille_horaire['cr'].heures+self.grille_horaire['fc'].heures+self.grille_horaire['3d'].heures
         
         self.grille_horaire['daca+ep'].points=(ed_plas+cr+fc+d3)/total_heures
         self.synthese_daca_ep()  
    
     def synthese_daca_ep(self):
         self.grille_horaire['daca+ep'].points=round(self.grille_horaire['daca+ep'].points,1)
         if self.grille_horaire['daca+ep'].points<50:
             self.grille_horaire['daca+ep'].evaluation=1
             self.echec_daca=True
         if (self.grille_horaire['daca+ep'].points>=50) & (self.grille_horaire['daca+ep'].points<60):
             self.grille_horaire['daca+ep'].evaluation=2
             self.echec_daca=False
         if self.grille_horaire['daca+ep'].points>=60:
             self.grille_horaire['daca+ep'].evaluation=3
             self.echec_daca=False
     
     def fct_moyenne_ponderee_cg(self):
         """Cette fonction calcule, pour un eleve,
         la moyenne pondérée des cours généraux certificatifs.
         Il s'agit d'une fonction s'adressant aux élèves d'art"""
         total_heures_cg=0
         for cours in self.grille_horaire.values():
             if (cours.ccnc==True) & (cours.points!=False) & (cours.abr not in ['cr','ed_plas','3d','fc','info','anim','audio','ha','exco','ds','ges_pro','photo','aud_vis']):
                 self.moy_pond_cg+=cours.heures*cours.points
                 total_heures_cg+=cours.heures
             #
         self.moy_pond_cg=round((self.moy_pond_cg/total_heures_cg),1)
         
#