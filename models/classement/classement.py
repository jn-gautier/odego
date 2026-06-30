import jinja2
import subprocess
import os
import subprocess
from tools.compfr import Compfr
from functools import cmp_to_key  
compfr=Compfr()
from PyQt6.QtCore import QObject, pyqtSignal as Signal


class Classement_jinja(QObject):
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
        grille=[]
        for eleve in classe.liste_eleves:
            eleve=classe.carnet_cotes[eleve]
            ligne_eleve=[]
            ligne_eleve.append(eleve.nom)
            ligne_eleve.append(eleve.moy_pond_ccnc)

            if eleve.moy_pond_ccnc>=80:
                grade="grande distinction"
            elif eleve.moy_pond_ccnc>=70:
                grade="distinction"
            elif eleve.moy_pond_ccnc>=60:
                grade="satisfaction"
            else:
                grade="a réussit"
            ligne_eleve.append(grade)

            grille.append(ligne_eleve)
        #print(grille)
        self.render_data(grille)
    
    
    
    
    def render_data(self,grille):
        template = self.latex_jinja_env.get_template("./models/classement/classement.csv")
        output=template.render(classe=grille)
        doc_name=self.file_name+'_classement.csv'
        self.signal_request_save.emit(output, 'Sauver tableau récapitulatif', doc_name, "Document TXT (*.csv)")