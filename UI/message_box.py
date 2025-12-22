from PyQt6.QtCore import QT_VERSION_STR
import platform, sys

def about(self):
    message='<div><p><b>Odego</b>, inspiré du grec <i>οδηγω : "je guide"</i>, est un outil '
    message+="d'aide à la décision pour les délibés. <br/>  Il permet de produire des tableaux récapitulatifs, des tableaux de classement et de situer chaque élève par rapport aux critères de réussite.</p> <p>Les fichiers sont produits aux formats tex et pdf.</p><p> <b>Auteur : </b> J.N. Gautier</p>  <p> <b>Language : </b> Python %s</p>  <p> <b>Interface : </b> Qt %s</p> <p> Merci à Noëlle qui a baptisé ce logiciel ainsi qu'à tous ceux dont les conseils ont permis d'en améliorer la qualité.</p> <p> Pour signaler un bug ou proposer une amélioration : <br/><a" %(platform.python_version(),QT_VERSION_STR)
    message+='href="mailto:gautier.sciences@gmail.com">gautier.sciences@gmail.com</a></p></div>'
    self.my_slots.show_messagebox("À propos d'odego", message, "question")


def help(self):
    message="<div><p>Pour obtenir de l'aide conçernant l'emploi de ce logiciel "
    message+="vous pouvez contacter J.N. Gautier par téléphone à n'importe quelle heure "
    message+="décente.</p>"
    message+="<p>J.N. Gautier : <b>0494/84.14.59</b></p></div>"
    message+="<p>Ce service vous coûtera généralement un café.</p>"
    message+="<p>En cas d'utilisation du service d'aide en dehors des heures prévues, vous me serez redevable d'un bon sandwich pendant les délibés.</p>"
    message+="</div>"
    self.my_slots.show_messagebox('AIde', message, "information")
    
    

def appExit(self):
    print ("Au revoir!")
    #app.quit()
    sys.exit()