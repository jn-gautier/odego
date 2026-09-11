from PyQt6.QtWidgets import QGridLayout, QDialog, QCheckBox, QLabel, QPushButton
from PyQt6.QtGui import QIcon


def config(self):
    self.check_tex=QCheckBox("Supprimer le fichier TEX")
    self.check_tex.setToolTip ('<p>Supprimer automatiquement les fichiers .tex et ne conserver que les fichiers .pdf.</p>')
    self.check_tex.setChecked(0)
    
    self.check_send_mail=QCheckBox("Envoyer par mail")
    self.check_send_mail.setToolTip ('<p>Envoyer automatiquement les fichiers pdf par mail au titulaire.</p>')
    self.check_send_mail.setChecked(0)
    
    self.check_upload_drive=QCheckBox("Sauvegarder sur Drive")
    self.check_upload_drive.setToolTip ("<p>Uploader le nombre d'heure d'échecs sur Drive</p>")
    self.check_upload_drive.setChecked(0)

    self.compile_typst=QCheckBox("Compiler avec Typst")
    self.compile_typst.setToolTip ("<p>Créer un fichier Typst à la place de Latex</p>")
    self.compile_typst.setChecked(0)

    self.compile_latex=QCheckBox("Compiler avec Latex")
    self.compile_latex.setToolTip ("<p>Créer un fichier Latex</p>")
    self.compile_latex.setChecked(1)

    button=QPushButton(QIcon('./icons/ok.svg'),'OK',self)

    
    

    grid=QGridLayout()
    grid.addWidget(QLabel('<p style="font-size:10pt;font-weight:bold">Configuration</p>' ),0,0)
    grid.addWidget(self.check_tex,1,0)
    grid.addWidget(self.check_send_mail,2,0)
    grid.addWidget(self.check_upload_drive,3,0)
    grid.addWidget(self.compile_latex,4,0)
    grid.addWidget(self.compile_typst,5,0)
    grid.addWidget(button,6,0)

    self.dial_config=QDialog(self)
    self.dial_config.setLayout(grid)

    button.clicked.connect(self.dial_config.close)
    self.dial_config.show()
    
