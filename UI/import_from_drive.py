from PyQt6.QtWidgets import QInputDialog
from UI.set_download_thread import set_download_thread

def dialog_import_download(self):
    if not self.sheets_id :
        with open('./UI/config/sheet.id') as f:
            sheet_id = f.read().rstrip() 
        set_download_thread(self,"main_sheet",sheet_id)

    classe,ok = QInputDialog.getItem(self,('Télécharger les points depuis Google Drive'),("Choisissez une classe"),['1 C a','1 C b','1 C c','1 C d','1 C e','1 C f','2 C a','2 C b','2 C c','2 C d','2 C e','2 C f','3 GT a','3 GT b','3 GT c','3 GT d','3 GT e','3 GT f','3 TQ','4 GT a','4 GT b','4 GT c','4 GT d','4 TQ','5 GT a','5 GT b','5 GT c','5 GT d','5 TQ','6 GT a','6 GT b','6 GT c','6 GT d','6 TQ'],editable = False)
    #classe=str(classe)
    
    if ok:
        niveau_classe=classe.split(' ')
    
        #on adapte les combos du dockinfos à la classe sélectionnée de facon à ce que les infos soient les bonnes lorsqu'on démarre les analyses
        if niveau_classe[1]=='TQ':
            self.combo_section.setCurrentIndex(2)
            self.combo_classes.setCurrentIndex(1)
            self.combo_niveau.setCurrentIndex(int(niveau_classe[0]))
            classe=niveau_classe[0]+'TQ'
        else:
            self.combo_section.setCurrentIndex(1)
            self.combo_niveau.setCurrentIndex(int(niveau_classe[0]))
            liste=['a','b','c','d','e','f']
            pos=liste.index(niveau_classe[2])+2
            self.combo_classes.setCurrentIndex(pos)
            classe=niveau_classe[0]+niveau_classe[2]
        get_sheet_classe(self,classe)
    
    


def get_sheet_classe(self,classe):
    if self.sheets_id :
        for ligne in self.sheets_id :
           infos = ligne.split('\t')
           if infos and infos[0].lower() == classe.lower():
               sheet_id = infos[1].strip()
               break
        
        if sheet_id:
            set_download_thread(self,"classe_sheet",sheet_id,classe)
            
        else:
            self.my_slots.show_messagebox("ID non trouvé", f"Aucun ID de feuille n'a été trouvé pour la classe : {classe_formattee}","warning")
                