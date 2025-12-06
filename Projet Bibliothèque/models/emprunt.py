from datetime import datetime, timedelta
# datetime : permet d’obtenir la date et l’heure actuelles.
# timedelta : permet d’ajouter des jours/semaines/heures à une date.

class Emprunt:
#Cette classe représente un emprunt d’un livre par un utilisateur.

    def __init__(self, utilisateur, livre, duree_jours=14):
        #Constructeur de la classe
        # Il reçoit :
            # utilisateur → l’utilisateur qui emprunte
            # livre → le livre emprunté
            # duree_jours → la durée de l’emprunt (14 jours par défaut)

        self.utilisateur = utilisateur
        self.livre = livre
            #On save les info transmises dans l'objet.

        self.date_emprunt = datetime.now()
            #Sauvegarde la date exacte de l’emprunt.
            #datetime.now() donne la date/heure actuelle.

        self.date_retour = self.date_emprunt + timedelta(days=duree_jours)
            #Calcule auto la date limite de retour (= date d’emprunt + x jours)

        self.rendu = False #Etat de l'emprunt

    def marquer_rendu(self):
        #change l'état de l'emprunt si le livre est retourné
        self.rendu = True
        self.livre.disponible = True

    def __str__(self):
        # Méthode pour afficher un emprunt sous forme de texte.
        statut = "Rendu" if self.rendu else "En cours" #Détermine le texte du statut selon l’état du retour.
        return f"{self.livre.titre} emprunté par {self.utilisateur.prenom} {self.utilisateur.nom} ({statut})"
        # Formatage lisible
