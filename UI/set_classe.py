import traceback
from models.classe import Classe
from models.eleve import Eleve
from models.cours import Cours
from UI.set_table_view import update_tableau_points_view


def set_classe(self):
    """Traite le tableau brut qui est une liste de listes dans laquelle chaque element contient False ou du texte, crée une Classe(obj), pour chaque ligne du tableau crée un Eleve(obj). Pour chaque Eleve, récupère son nom et sa ddn, crée une grille_horaire(dict) dans laquelle keys=nom d'un cour, value=un Cours(obj) ou False(bool)"""
    self.classe=Classe(parent=self)
    self.classe.messagebox.connect(self.my_slots.show_messagebox)
    self.classe.carnet_cotes={}
    self.classe.liste_cours=get_ligne_cours(self)
    
    try:
        for ligne_points in self.tableau_points:
            if (ligne_points[0]==False) or (ligne_points[0].lower()=='cours'):
                # il peut y avoir des lignes vides en bas de tableau, cela justifie le test ligne_points[0]==False
                pass
            else:
                eleve=Eleve(parent=self)
                eleve.messagebox.connect(self.my_slots.show_messagebox)

                eleve.nom=ligne_points[0]
                
                for cours,points_eleve in zip(self.classe.liste_cours,ligne_points[1:]):
                    
                    if (cours.lower()=='ddn') & (points_eleve!=False):
                        eleve.ddn=points_eleve
                    
                    elif points_eleve!=False:
                        eleve.grille_horaire[cours]=Cours()
                        eleve.grille_horaire[cours].set_eval(points_eleve)
                    else : 
                        eleve.grille_horaire[cours]=Cours()
                    print (eleve.nom , cours, points_eleve)
                    #    
                self.classe.carnet_cotes.setdefault(eleve.nom,eleve)
                #self.classe.carnet_cotes[eleve.nom]=eleve
        
        if 'ddn' in self.classe.liste_cours:
            self.classe.liste_cours.remove('ddn')
        self.classe.prod_liste_eleves()
        self.tableau_valide=True
        update_tableau_points_view(self)

    except Exception as e:
        message="<p>Un problème majeur a été rencontré lors de la création du modèle de tableau.</p>"
        message+='<p>Veuillez signaler cette erreur au développeur.</p></div>'
        self.my_slots.show_messagebox('Échec', message, "critical")
        print (f'Erreur : {e}')
        print ('Message : ', traceback.format_exc())
        
        

def get_ligne_cours(self):
    liste_cours=[]
    try:
        is_ligne_cours=False
        ligne_cours=self.tableau_points[2]
        if ligne_cours[0].lower()=='cours':
            is_ligne_cours=True
            for cell in ligne_cours :
                if cell!=(False): #il peut y avoir des cellules vides qui suivent celles avec les intitulés des cours ; on ne prend en compte que les cellules non vides.
                    liste_cours.append(cell.lower().rstrip('\r\n '))
            del liste_cours[0]       
        
        if not is_ligne_cours :
            raise Exception
        else:
            return liste_cours
    except Exception as e:
        message="<p>Il n'y a pas de ligne avec les cours dans votre fichier</p> <p>ou celle-ci n'est pas indiquée par le mot 'Cours'</p>"
        self.my_slots.show_messagebox('Échec', message, "critical")
        print (f'Erreur : {e}')
        print ('Message : ', traceback.format_exc())



