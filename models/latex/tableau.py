import jinja2
import subprocess
import os
import subprocess
from tools.compfr import Compfr
from functools import cmp_to_key  
compfr=Compfr()
from PyQt6.QtCore import QObject, pyqtSignal as Signal


class Tableau_jinja(QObject):
    signal_request_save = Signal(str,str,str,str)
    def __init__(self,parent=None):
        super().__init__(parent)

        self.latex_jinja_env = jinja2.Environment(
        block_start_string = '\\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\\VAR{',
        variable_end_string = '}',
        comment_start_string = '\\#{',
        comment_end_string = '}',
        line_statement_prefix = '%%',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        lstrip_blocks = True,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
        )
        parent = self.parent()
        classe=parent.classe
        titre=parent.titre 
        self.file_name=parent.file_name
        self.set_data(titre,classe)
        
    
    def set_data(self,titre,classe):
        liste_cours=[]
        for cours in classe.liste_cours:
            if cours not in ['chim_1','chim_2','phys_1','phys_2','bio_1','bio_2']:
                liste_cours.append(cours)
        
        en_tete=["COURS"]
        for nom_cours in liste_cours:
            en_tete.append(nom_cours.replace('_','~').upper())#les carac "_" posent problème lors de la compilation des fichiers tex, je les remplace par un espace insecable en latex
        en_tete.append("Échecs")
        en_tete.append("Moy.")
        en_tete.append("Global")
        
        larg_colonne=round((25.0/(len(en_tete)-1)),7)
        nb_colonnes=len(en_tete)-1

        grille=[]
        

        for eleve in sorted(classe.liste_eleves,key=cmp_to_key(compfr)):
            eleve=classe.carnet_cotes[eleve]
            ligne_eleve=[]
            if len(eleve.nom)>40:
                ligne_eleve.append(eleve.nom[0:20]+" \\dots "+eleve.nom[-20:])

            else:
                ligne_eleve.append(eleve.nom[0:40])
            
            for nom_cours in liste_cours:
                ligne_eleve.append(self.set_cours_style(eleve.grille_horaire.get(nom_cours,False)))
            
            
            
            txt_heures_echec=f"{eleve.heures_echec_tot} / {eleve.vol_horaire_ccnc}"
            ligne_eleve.append(txt_heures_echec)
            ligne_eleve.append(self.set_heures_echec_style(eleve.moy_pond_ccnc))
            ligne_eleve.append(self.set_situation_global_style(eleve))
            grille.append(ligne_eleve)
        #print(grille)
        self.render_data(titre,en_tete,grille,larg_colonne,nb_colonnes)
    
    
    def set_cours_style(self,cours):
        if cours:
            if cours.evaluation==1:
                return f"\\echec{{ {cours.points} }}"
            elif cours.evaluation==2:
                return f"\\faible{{ {cours.points} }}"
            elif cours.evaluation==3:
                return f"\\reussite{{ {cours.points} }}"
            elif cours.evaluation==4:
                if cours.certif_med:
                    return "cm"
                else:
                    return ""
            elif cours.evaluation==0:
                return ""
        else:
            return ""

    def set_heures_echec_style(self,moy_pond_ccnc):
        if moy_pond_ccnc <50:
            return f"\\echec{{ {moy_pond_ccnc} }} "
        elif moy_pond_ccnc <60:
            return f"\\faible{{ {moy_pond_ccnc} }} "
        else :
            return f"\\reussite{{ {moy_pond_ccnc} }} "

    def set_situation_global_style(self,eleve):
        if eleve.situation_globale==3:
            return '\\SetCell{bg=vert}{}'
        elif eleve.situation_globale ==1:
            return '\\SetCell{bg=rouge}{}'
        elif eleve.situation_globale ==2:
            return '\\SetCell{bg=orange}{}'
        elif eleve.situation_globale ==4:
            return '\\SetCell{bg=gris_fonce}{}'
        else:
            return '\\{}'
    
    def render_data(self,titre,en_tete,grille,larg_colonne,nb_colonnes):
        template = self.latex_jinja_env.get_template("./models/latex/templates/tableau.tex")
        output=template.render(titre=titre,en_tete=en_tete,classe=grille,larg_colonne=larg_colonne,nb_colonnes=nb_colonnes)
        doc_name=self.file_name+'_tableau.tex'
        self.signal_request_save.emit(output, 'Sauver tableau récapitulatif', doc_name, "Document TEX (*.tex)")