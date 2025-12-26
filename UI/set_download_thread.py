from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt, QThread
from UI.threads import Download_task


def set_download_thread(self,task_name,sheet_id,classe=None):

    #création du QProgressDialog
    self.prog = QProgressDialog()
    self.prog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.prog.setCancelButton(None)
    
    label="Téléchargement..."
    if task_name=="main_sheet":
        label="Téléchargement des id des classes..."
    elif task_name=="classe_sheet":
        label=f"Téléchargement du tableau de {classe}..."
    self.prog.setLabelText (label)
    self.prog.setRange(0, 100) # Pour un barème simple
    self.prog.setValue(0)
    self.prog.show()
    

    #creation du thread
    self.thread=QThread()
    self.worker=Download_task()
    self.worker.messagebox.connect(self.my_slots.show_messagebox)
    self.worker.sheet_id=sheet_id
    self.worker.moveToThread(self.thread)
    
    #creation des connecteurs
    self.thread.started.connect(self.worker.run)
    self.worker.progress.connect(self.my_slots.progress_dialog)
    
    
    if task_name=="main_sheet":
        self.worker.finished.connect(self.my_slots.handle_sheets_id)
    elif task_name=="classe_sheet":
        self.worker.finished.connect(self.my_slots.handle_sheet_classe)
    

    #creations des connecteurs de fin de tache
    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    
    #creation des connecteurs d'échec
    self.worker.failed.connect(self.thread.quit)
    self.worker.failed.connect(self.worker.deleteLater)
    
    #lancement du thread
    print(label)
    self.thread.start()