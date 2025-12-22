from PyQt6.QtCore import Qt, QObject, pyqtSlot as Slot
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QProgressDialog, QApplication
from PyQt6.QtCore import QThread, Qt, pyqtSignal as Signal
import os
import subprocess
from UI.set_classe import set_classe
from UI.threads import Compile_tableau_task
import traceback # Utile pour le débogage

class Slots(QObject):
    signal_doc_saved = Signal()
    def __init__(self, main_window,parent=None):
        super().__init__(parent)
        self.main_window = main_window

    @Slot(str, str, str) # Décorateur pour déclarer que ceci est un slot qui prend deux chaînes
    def show_messagebox(self, titre, message, icon="information"):
        """Ce slot est appelé lorsque le signal est émis par l'instance Eleve."""
        msg_box = QMessageBox(self.main_window) # On utilise 'self' (la QMainWindow) comme parent
        msg_box.setWindowTitle(titre)
        msg_box.setText(message)
        if icon == "critical":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif icon == "warning" :
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif icon=="information":
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif icon=="question":
            msg_box.setIcon(QMessageBox.Icon.Question)
        
        msg_box.exec() # Affiche la boîte de dialogue modale
    
    @Slot(str, str, str, str)
    def enregistrer_document_latex(self, latex_content: str, titre: str, doc_name: str, doc_type: str):
        """
        Slot appelé pour l'enregistrement. Il écrit le fichier, puis le compile en PDF.
        """
        chemin_fichier, _ = QFileDialog.getSaveFileName(
            self.main_window, 
            titre, 
            doc_name, 
            doc_type
        )

        if chemin_fichier:
            try:
                with open(chemin_fichier, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                self.main_window.chemin_fichier_tex=chemin_fichier
                self.signal_doc_saved.emit()
            
            except Exception as e:
                # Si l'écriture ou la compilation échoue
                QMessageBox.critical(
                    self.main_window, 
                    "Erreur Critique", 
                    f"Échec de l'opération.\nErreur: {e}\n\nTraceback:\n{traceback.format_exc()}"
                )
        else:
            print("Enregistrement annulé par l'utilisateur.")

    @Slot(str)
    def compiler_latex_en_pdf(self, chemin_fichier_tex: str):
        """
        Gère la compilation du fichier .tex en utilisant latexmk ou pdflatex.
        """
        self.main_window.prog.show()
        self.thread=QThread()
        self.worker=Compile_tableau_task()
        self.worker.messagebox.connect(self.show_messagebox)
        self.worker.chemin_fichier_tex=chemin_fichier_tex
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress_dialog)
        #self.worker.finished.connect(self.my_slots.handle_sheets_id)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.failed.connect(self.thread.quit)
        self.worker.failed.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.thread.deleteLater)
        #print(f"Téléchargement du document contenant les id des classes...")
        self.thread.start()



        
    @Slot(str)
    def nettoyer_fichiers_temporaires(self, dossier: str):
        """Supprime les fichiers générés par LaTeX (.aux, .log, .fls, etc.)."""
        commande=["latexmk","-c"]
        proc = subprocess.Popen(commande, cwd=dossier)
        proc.wait()
        
    
    @Slot(list)
    def handle_sheets_id(self,tableau):
        """Slot appelé en cas de succès du téléchargement de la sheets_id, la feuille qui contient le sheet_id de chaque classe"""
        self.main_window.sheets_id=tableau

    @Slot(list)
    def handle_sheet_classe(self,tableau):
        """Slot appelé en cas de succès du téléchargement de la sheet d'une classe"""
        self.main_window.tableau_points=[]
        for ligne in tableau:
            liste_ligne_points=ligne.split('\t')
            ligne_points=[]
            for elem in liste_ligne_points:
                elem=elem.rstrip('\n\r ')
                if not elem :
                    elem=False
                ligne_points.append(elem)
            self.main_window.tableau_points.append(ligne_points)
        set_classe(self.main_window)
    
    @Slot(int)
    def progress_dialog(self,value):
        self.main_window.prog.setValue(value)
        self.main_window.prog.raise_()
        QApplication.processEvents()
