import re
class Cours(object):
     #
    def __init__(self):
        self.points=False
        self.certif_med=False
        self.evaluation=0
        self.contrat=False
        self.echec_force=False
        self.echec_travail=False
        self.pseudo=False
        self.ccnc=False
        self.heures=0
        self.intitule=''
        self.abr=''
        self.verrou=False
        self.option=False
        self.disp_ndls=False
     #c
    def set_eval(self,points):
        """Cette fonction n'est appelé qui si les points sont !False, elle attribue une évaluation et eventuellement des points au cours"""
        #points=points_eleve.rstrip('\r\n ') #pas nécessaire, déjà fait à l'importation depuis le drive
        if "!" in points:  
            self.echec_force=True
            self.evaluation=1
            points=points.replace('!','')
        
        if points.lower()=='cm':
            self.evaluation=4
            self.certif_med=True
        elif points.lower()=='disp':
            self.evaluation=5
        elif points.lower()=='x':#le cours n'est pas évalué (ex: meth en 3TQ)
            self.evaluation=4
        
        else: #les points sont des points "classiques"
            points=self.nettoie_point(points)# rappel: la fonction nettoie_point converti également les points en float
            self.points=points
            if points<50:
                self.evaluation=1
            elif (50<=points<60) & (self.echec_force==False):
                self.evaluation=2
            elif (points>=60) & (self.echec_force==False):
                self.evaluation=3
            else:
                pass
    
    def nettoie_point(self,points):
        points=points.replace(',','.')
        points=points.replace(';','.')
        points=re.findall(r'[0-9.]+', points) #une regex pour récupérer les digit et les symboles '.' dans les string
        points=''.join(points)
        if points=='': #si après avoir retiré les caractères parasites il ne reste rien alors c'est qu'il n'y a pas de points
            points=False
        
        if points!=False:
            points=float(points)
            if points==0.0 : 
                points=0.1 #pour éviter que les poinst soient considérés comme False dans les tests
            if points!=int(points):
                points=round(points,1)
            else :
                points=int(points) #pour éviter que les points s'affichent avec .0
        return points
#
#