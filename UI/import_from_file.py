from PyQt6.QtWidgets import QFileDialog
import os, traceback
from UI.set_classe import set_classe


def select_file(self):
    current_dir = os.path.expanduser("~/dossier_ivf/odego/app")
    file_name = QFileDialog.getOpenFileName(self,'Tableau avec les points de la classe.',current_dir)
    file_name=file_name[0]
    #self.current_dir=os.path.dirname(file_name)
    import_txt(self,file_name)
    #get_file_ext()
    #if self.ext=='txt':
    #    self.import_txt()
    #elif self.ext=='tsv':
    #    self.import_txt()
    #else:
    #    QMessageBox.warning(self,'Erreur',"Veuillez renseigner un fichier avec l'extension 'txt' ou 'tsv'.")
     #
def get_file_ext(self):
         ext=self.file_name.split('.')
         self.ext=ext[len(ext)-1]

def import_txt(self,file_name):
    try:
        self.my_slots.show_messagebox('Information', "<p>L'importation depuis un fichier txt ou tsv nécessite </p><p>que les valeurs soient séparées par des tabulations.</p>", "information")
        myfile= open(file_name, "r")
        self.tableau_points=[]
        for ligne in myfile:
            liste_ligne_points=ligne.split('\t')
            ligne_points=[]
            for elem in liste_ligne_points:
                elem=elem.rstrip('\n\r ')
                if not elem :
                    elem=False
                ligne_points.append(elem)
            self.tableau_points.append(ligne_points)
        set_classe(self)

    except Exception as e:
        message="<p>Un problème majeur a été rencontré lors de l'importation du fichier.</p>"
        message+='<p>Veuillez signaler cette erreur au développeur.</p></div>'
        self.my_slots.show_messagebox('Échec',message,"critical")
        print ('Erreur : %s' %e)
        print ('Message : ', traceback.format_exc())