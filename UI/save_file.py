from PyQt6.QtCore import pyqtSlot as Slot
# ...

class Gui(QMainWindow):
    # ... __init__ et autres méthodes ...

    @Slot(str)
    def sauvegarder_document_latex(self, chemin_fichier: str):
        # 1. 'self' ici est l'instance de Gui
        # 2. On accède aux données via l'attribut self.tableau_jinja de Gui
        if self.tableau_jinja.latex_output is not None:
            try:
                with open(chemin_fichier, 'w', encoding='utf-8') as f:
                    f.write(self.tableau_jinja.latex_output)
                
                # 3. On appelle le slot de messagebox via self.my_slots (attribut de Gui)
                self.my_slots.show_messagebox("Succès", f"Fichier sauvegardé dans : {chemin_fichier}", "information")
                
            except Exception as e:
                self.my_slots.show_messagebox("Erreur de sauvegarde", f"Impossible d'écrire le fichier : {e}", "critical")
        else:
            self.my_slots.show_messagebox("Erreur", "Le contenu LaTeX n'a pas été généré.", "critical")