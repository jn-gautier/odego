from PyQt6.QtCore import QObject, QThread, pyqtSignal as Signal
from PyQt6.QtWidgets import QProgressDialog, QApplication
from PyQt6.QtCore import Qt
from urllib.error import URLError, HTTPError
import urllib.request
import os
import subprocess


class Download_task(QObject):
    finished=Signal(list)
    failed=Signal()
    messagebox = Signal(str, str, str)
    progress=Signal(int)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.sheet_id=""
        #self.my_slots=Slots(self)
    
    def run(self):        
        link=f"https://docs.google.com/spreadsheets/export?id={self.sheet_id}&exportFormat=tsv"
        
        
        try:
            req = urllib.request.Request(link)
            req.add_header('Cache-Control', 'max-age=0')#j'ajoute cette ligne pour recevoir la dernière version du fichier et non une vieille version en cache
            self.progress.emit(50)
            with urllib.request.urlopen(req) as tsv:
                reader = tsv.read().decode('utf-8')
                tableau = reader.split('\n')
                print("Finished")
                
                self.finished.emit(tableau)
            self.progress.emit(100)
                
        except HTTPError as e:
            print("Erreur HTTP", f"Erreur lors de la connexion à Google Drive (Code: {e.code}).")
            self.messagebox.emit("Erreur HTTP", f"Erreur lors de la connexion à Google Drive (Code: {e.code}).","critical")
            self.failed.emit()
        except URLError as e:
            print("Erreur de connexion", f"Impossible de se connecter à Google Drive. Vérifiez votre connexion internet. ({e.reason})")
            self.messagebox.emit("Erreur de connexion", f"Impossible de se connecter à Google Drive. Vérifiez votre connexion internet. ({e.reason})","critical")
            self.failed.emit()
        except Exception as e:
            print("Erreur Inconnue", f"Une erreur inattendue s'est produite lors de la récupération de l'ID : {e}")
            self.messagebox.emit("Erreur Inconnue", f"Une erreur inattendue s'est produite lors de la récupération de l'ID : {e}","critical")
            self.failed.emit()

class Compile_tableau_task(QObject):
    messagebox = Signal(str, str, str)
    finished = Signal()
    progress=Signal(int)
    failed=Signal()

    def __init__(self,parent=None):
        super().__init__(parent)
        self.chemin_fichier_tex=""
    
    def run(self):
        dossier_sortie = os.path.dirname(self.chemin_fichier_tex)
        nom_base = os.path.basename(self.chemin_fichier_tex)
        
        # --- Affichage d'une barre de progression (optionnel mais fortement recommandé) ---
        
        
        try:
            commande = ['latexmk', '-pdflatex', nom_base]
            self.progress.emit(50)
            proc = subprocess.Popen(commande, cwd=dossier_sortie)
            proc.wait() # Assure que le processus est terminé
            


            # --- Vérification du succès (simple) ---
            if proc.returncode != 0:
                 raise Exception("La commande 'latexmk' a échoué. Vérifiez votre installation LaTeX.")
                 self.failed.emit()
            
            
            # --- ÉTAPE 3: Nettoyage des fichiers temporaires (.aux, .log, etc.) ---
            # C'est une bonne pratique de nettoyer après la compilation réussie
            self.progress.emit(75)
            self.nettoyer_fichiers_temporaires(dossier_sortie)
        
        except FileNotFoundError:
            self.messagebox.emit("Programme Introuvable" , "La commande 'latexmk' n'a pas été trouvée" , "critical")
            self.failed.emit()
            raise # Relaisser l'exception pour la gestion globale
            
        except Exception as e:
            self.messagebox.emit("Erreur de Compilation" , f"La compilation LaTeX a échoué.\nDétails: {e}","critical")
            self.failed.emit()
            raise # Relaisser l'exception pour la gestion globale
        finally:
            pass
            #prog.close()
    
    def nettoyer_fichiers_temporaires(self, dossier: str):
        """Supprime les fichiers générés par LaTeX (.aux, .log, .fls, etc.)."""
        commande=["latexmk","-c"]
        proc = subprocess.Popen(commande, cwd=dossier)
        self.finished.emit()
        self.progress.emit(100)
        self.messagebox.emit("Succès" , f"Le document a été compilé avec succès","information")
