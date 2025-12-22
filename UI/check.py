from UI.process_classe import process_classe

def check_before_start(self):
    param_valides=True
    alert="<div><p> Veuillez renseigner :</p> <ul>"
    if self.combo_niveau.currentText()=='':
        param_valides=False
        alert+='<li>Le <b> niveau </b> de la classe.</li>'
    
    if self.combo_section.currentText()=='':
        param_valides=False
        alert+='<li>La <b> section </b> de la classe.</li>'
    if self.combo_classes.currentText()=='':
        param_valides=False
        alert+='<li>Le <b> nom </b> de la classe.</li>'
    
    if param_valides==False:
        alert+='</ul> </div>'
        self.my_slots.show_messagebox('Informations manquantes', alert, "warning")
        
    if not self.radio_tab_recap.isChecked() and not self.radio_ana_det.isChecked() and not self.radio_classmt.isChecked():
        message="<div><p>Aucune analyse n'a été demandée pour cette classe.</p>"
        message+="<p>N'oubliez pas de cocher les analyses souhaitées <b>avant de pousser sur démarrage</b>.</p> </div>"
        self.my_slots.show_messagebox('Aucune analyse demandée', message, "information")
    
    if self.tableau_valide==False:
        alert="<div><p>Aucun point n'a encore été importé.</p>"
        alert+="<p> Veuillez importer des points <b>avant de pousser sur démarrage</b>.</p> </div>"
        self.my_slots.show_messagebox('Points manquants', alert, "warning")
    
    
    if self.tableau_valide & param_valides:
        process_classe(self)