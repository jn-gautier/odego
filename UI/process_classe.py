from models.latex.tableau import Tableau_jinja
import traceback
from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt
from UI.set_thread_compile import set_thread_compile


def process_classe(self):
    """Traitement des données, réalisation des analyses et création des documents latex."""
    #self.fichier_a_traiter=self.fname
    creer_tableau_recap=self.radio_tab_recap.isChecked()
    creer_analyse_eleve=self.radio_ana_det.isChecked()
    creer_classement=self.radio_classmt.isChecked()
    #
    niveau=self.combo_niveau.currentText()
    section=self.combo_section.currentText()
    nom_classe=self.combo_classes.currentText()#a, b, c, ...
    annee=self.combo_annees.currentText()
    delibe=self.combo_delib.currentText()
    
    self.file_name = f"{delibe}_{annee}_{niveau}{section}{nom_classe}"
    self.titre = f"Conseil de classe {niveau}{section}{nom_classe} - {delibe} {annee}"
    #
    try:
        self.classe.set_param(niveau,section,delibe)
        
        try:
            self.classe.stats_elv()
            self.classe.prod_situation_globale()
            self.classe.update_liste_cours()
            
            try:
                if creer_analyse_eleve:
                    pass
                    #Latex_file(doc_type="analyse",titre=titre,file_name=file_name,self.classe)
                if creer_tableau_recap:
                    self.tableau_jinja=Tableau_jinja(parent=self)
                    self.my_slots.signal_doc_saved.connect(lambda : set_thread_compile(self))
                    self.tableau_jinja.signal_request_save.connect(self.my_slots.enregistrer_document_latex)
                    self.tableau_jinja.set_data(self.titre,self.classe)
                    
                    #Latex_file(doc_type="tableau_recap",titre=titre,file_name=file_name)
                if creer_classement:
                    Latex_file(doc_type="classement",titre=titre,file_name=file_name)
                #self.my_slots.show_messagebox('Terminé', "Les données ont été traitées avec succès!", "information")
            except Exception as e:
                self.my_slots.show_messagebox('Erreur', "Un ou plusieurs documents demandés n'ont pas été produits", "warning")
                print (f"Erreur : {e}")
                print ('Message : ', traceback.format_exc() )

        except Exception as e:
            self.my_slots.show_messagebox('Échec', "Une erreur a été rencontrée dans l'analyse des points", "critical")
            print (f"Erreur : {e}")
            print ('Message : ', traceback.format_exc() )

    except Exception as e:
        message="<div><p> Un problème a été rencontré lors du traitement de votre fichier</p>"
        message+="<ul><li>Vérifiez que le fichier sélectionné contienne bien des <b>points</b>.</li>"
        message+="<li>Vérifiez que le fichier sélectionné contienne bien le <b>nom des cours</b>.</li>"
        message+="<li>Vérifiez que vous avez sélectionné la bonne <b>classe </b>et la bonne <b>section </b>dans le menu d'acceuil.</li></ul>"
        message+="</div>"
        self.my_slots.show_messagebox('Échec', message, "warning")
        print (f"Erreur : {e}")
        print ('Message : ', traceback.format_exc() )
