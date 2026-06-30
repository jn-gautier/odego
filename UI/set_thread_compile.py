from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QObject, QThread, pyqtSignal as Signal
from UI.threads import Compile_tableau_task

def set_thread_compile(self):
    self.prog = QProgressDialog()
    self.prog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.prog.setCancelButton(None)
    self.prog.setLabelText ('Compilation du document Latex...')
    self.prog.setRange(0, 100) # Pour un barème simple
    self.prog.setValue(0)
    self.prog.show()

    self.thread=QThread()
    self.thread.setObjectName("Compilation") 
    self.worker=Compile_tableau_task()
    self.worker.messagebox.connect(self.my_slots.show_messagebox)
    self.worker.chemin_fichier_tex=self.chemin_fichier_tex
    
    self.worker.moveToThread(self.thread)
    self.thread.started.connect(self.worker.run)
    self.worker.progress.connect(self.my_slots.progress_dialog)
    
    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.worker.failed.connect(self.thread.quit)
    self.worker.failed.connect(self.worker.deleteLater)
    #self.worker.failed.connect(self.thread.deleteLater)

    self.thread.finished.connect(self.thread.deleteLater)
    self.thread.finished.connect(lambda: self.threads_actifs.remove(self.thread))
    print(f"Compilation du document Latex...")
    self.threads_actifs.append(self.thread)
    self.thread.start()

    
    
    # On ajoute le thread à la liste pour empêcher Python de le détruire
    