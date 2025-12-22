from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QObject, QThread, pyqtSignal as Signal
from UI.threads import Compile_tableau_task

def set_download_thread(self):
    self.prog = QProgressDialog()
    self.prog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.prog.setCancelButton(None)
    self.prog.setLabelText ('Téléchargement de la feuille...')
    self.prog.setRange(0, 100) # Pour un barème simple
    self.prog.setValue(0)
    self.prog.show()

    self.thread=QThread()
    self.worker=Compile_tableau_task()
    self.worker.messagebox.connect(self.my_slots.show_messagebox)
    self.worker.chemin_fichier_tex=self.chemin_fichier_tex
    
    self.worker.moveToThread(self.thread)
    self.thread.started.connect(self.worker.run)
    self.worker.progress.connect(self.my_slots.progress_dialog)
    #self.worker.finished.connect(self.my_slots.handle_sheets_id)
    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.worker.failed.connect(self.thread.quit)
    self.worker.failed.connect(self.worker.deleteLater)
    self.worker.failed.connect(self.thread.deleteLater)
    print(f"Compilation du document Latex...")
    self.thread.start()