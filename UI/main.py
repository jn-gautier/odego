from PyQt6.QtWidgets import QMainWindow,QApplication
from PyQt6.QtGui import QIcon
from UI.menu import set_menu
from UI.dock_infos import set_dock_infos
from UI.dock_analyses import set_dock_analyses
from UI.dock_start import set_dock_start
from UI.slots import Slots



class Gui(QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        self.my_slots=Slots(self)
        self.tableau_valide=False #cette variable passe sur True quand on télécharege et tableau de points et qu'il est traité valablement par la fct_carnet_cotes
        self.setWindowTitle('Odego : un guide pour les délibérations')
        self.setWindowIcon(QIcon("./UI/icons/odego.svg"));
        set_menu(self)
        self.statusBar()
        set_dock_infos(self)
        set_dock_analyses(self)
        set_dock_start(self)
        #self.center()
        self.sheets_id=None
    
    def center(self):
        screen = QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        self.move(center_point.x() - self.width() // 2, center_point.y() - self.height() // 2)
    