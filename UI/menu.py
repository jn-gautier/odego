from UI.actions import *

def set_menu(self):
    menubar = self.menuBar()
    fileMenu = menubar.addMenu("&Application")
    fileMenu.addAction(start_action(self))
    fileMenu.addAction(quit_action(self))
    fileMenu.addAction(config_action(self))

    fileMenu = menubar.addMenu("&Importer")
    fileMenu.addAction(file_action(self))
    fileMenu.addAction(download_action(self))
    
    fileMenu = menubar.addMenu("&Aide")
    fileMenu.addAction(help_action(self))
    fileMenu.addAction(about_action(self))
    
    toolbar = self.addToolBar('Toolbar')
    toolbar.addAction(file_action(self))
    toolbar.addAction(download_action(self))
    toolbar.addAction(quit_action(self))