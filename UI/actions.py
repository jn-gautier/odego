#from PyQt6.QtCore import QAction
from PyQt6.QtGui import QIcon, QAction
from UI.message_box import help, about,appExit
from UI.config import config
from UI.import_from_drive import dialog_import_download
from UI.import_from_file import select_file
from UI.check import check_before_start



#les action correspondent à des entrée dans le menu et dans la toolbar
def file_action(self):
    new_from_fileAction = QAction(QIcon('./UI/icons/import_file.svg'),"&Importer les points à partir d'un fichier", self)
    new_from_fileAction.setShortcut('Ctrl+I')
    new_from_fileAction.setStatusTip("Importer les points directement à partir d'un fichier")
    new_from_fileAction.triggered.connect(lambda : select_file(self))
    return new_from_fileAction

def download_action(self):
    new_from_downloadAction = QAction(QIcon('./UI/icons/download_file.svg'),"Télécharger les points à partir de Google Drive", self)
    new_from_downloadAction.setShortcut('Ctrl+D')
    new_from_downloadAction.setStatusTip("Télécharger les points à partir de Google Drive")
    new_from_downloadAction.triggered.connect(lambda : dialog_import_download(self))
    return new_from_downloadAction

def start_action(self):
    StartAction = QAction(QIcon('./UI/icons/ok_apply.svg'),"Démarrer l'analyse", self)
    StartAction.setShortcut('Ctrl+G')
    StartAction.setStatusTip("Démarrer")
    StartAction.triggered.connect(lambda : check_before_start(self))
    return StartAction

def quit_action(self):
    #self.about=about
    QuitAction = QAction(QIcon('./UI/icons/quit.svg'),"Quitter", self)
    QuitAction.setShortcut('Ctrl+Q')
    QuitAction.setStatusTip("Quitter")
    QuitAction.triggered.connect(lambda : appExit(self))
    return QuitAction

def help_action(self):
    HelpAction = QAction(QIcon('./UI/icons/help.svg'),"Obtenir de l'aide", self)
    HelpAction.setStatusTip("Obtenir de l'aide concernant l'utilisation de ce logiciel")
    HelpAction.triggered.connect(lambda : help(self))
    return HelpAction

def about_action(self):
    AboutAction = QAction(QIcon('./UI/icons/odego.svg'),"À propos", self)
    AboutAction.setStatusTip("A propos de ce logiciel")
    AboutAction.triggered.connect(lambda : about(self))
    return AboutAction

def config_action(self):
    ConfigAction = QAction(QIcon('./UI/icons/config.svg'),"Configurer", self)
    ConfigAction.setStatusTip("Configurer le logiciel")
    ConfigAction.triggered.connect(lambda : config(self))
    return ConfigAction
