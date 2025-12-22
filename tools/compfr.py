import locale

class Compfr(object):
    """Cette classe contient une unique fonction servant à comparer des chaines de caractères pour créer une classement alphabétique français"""
    # Solution prise sur : http://python.jpvweb.com/mesrecettespython/doku.php?id=tris_dictionnaire_francais
    def __init__(self):
        # --- 1. Robustesse de la Locale ---
        # Tentative de configurer la locale française la plus appropriée.
        # Ceci est crucial pour que 'locale.strcoll' gère correctement les accents (é, à, ç).
        locales_a_essayer = ['fr-BE' , 'fr_FR.UTF-8' , 'fr_FR', 'fr', 'fra']
        locale_definie = False
        
        for loc in locales_a_essayer:
            try:
                # LC_ALL permet de définir tous les aspects linguistiques
                locale.setlocale(locale.LC_ALL, loc)
                locale_definie = True
                # On arrête dès qu'une locale est acceptée par le système
                break 
            except locale.Error:
                continue

        if not locale_definie:
            print("Attention : Aucune locale française n'a pu être définie. Le tri risque d'être incorrect (gestion des accents).")


        # --- 2. Préparation pour l'optimisation ---
        self.espinsec = '\xA0' # Espace insécable

        # Caractères à ignorer : tiret (-), apostrophe ('), espace insécable (self.espinsec), espace simple ( )
        chars_to_remove = "-\'" + self.espinsec + " "
        
        # Création du tableau de traduction pour une suppression en une seule passe (optimisé)
        self.translation_table = str.maketrans('', '', chars_to_remove)
    
    #
    def __call__(self, v1, v2):
        # 1. Conversion en minuscules pour un tri insensible à la casse
        v1 = v1.lower() 
        v2 = v2.lower()

        # 2. Suppression optimisée des caractères (tirets, espaces, apostrophes)
        v1 = v1.translate(self.translation_table)
        v2 = v2.translate(self.translation_table)

        # 3. Comparaison linguistique (utilise la locale configurée)
        return locale.strcoll(v1, v2)