from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from tools.compfr import Compfr
from functools import cmp_to_key  
compfr=Compfr()

def update_tableau_points_view(self):
    """
    Met à jour la vue de la table des points pour une classe donnée.
    """
    # 1. Supprimer l'ancienne table
    if hasattr(self, 'table') and self.table:
        self.table.setParent(None)
        self.table.deleteLater() # S'assure que l'objet est bien supprimé

    # 2. Créer et configurer la nouvelle table
    self.table = QTableWidget()
    self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    # 3. Trier les élèves une seule fois
    eleves_tries = sorted(self.classe.liste_eleves, key=cmp_to_key(compfr))
    
    # 4. Préparer les en-têtes et la structure de la table
    noms_cours = self.classe.liste_cours
    self.table.setRowCount(len(eleves_tries))
    self.table.setColumnCount(len(noms_cours))
    self.table.setHorizontalHeaderLabels(noms_cours)
    self.table.setVerticalHeaderLabels(eleves_tries)

    # 5. Remplir la table avec les données
    for i, nom_eleve in enumerate(eleves_tries):
        eleve = self.classe.carnet_cotes.get(nom_eleve) #.get renvoit l'eleve recherché s'il existe dans le dict

        for j, nom_cours in enumerate(noms_cours):
            cours_details = eleve.grille_horaire.get(nom_cours) #renvoit un objet 'cours'
            if cours_details.points!=False: #je ne comprend pas pq il n'y a pas toujours de "cours', à vérifier
                item_text = str(cours_details.points)
            else:
                item_text = ''

            new_item = QTableWidgetItem(item_text)
            self.table.setItem(i, j, new_item)

    # 6. Afficher la table
    self.setCentralWidget(self.table)
    self.showMaximized()