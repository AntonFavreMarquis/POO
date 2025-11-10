from datetime import datetime, timedelta

class Emprunt:
    def __init__(self, utilisateur, livre, duree_jours=14):
        self.utilisateur = utilisateur
        self.livre = livre
        self.date_emprunt = datetime.now()
        self.date_retour = self.date_emprunt + timedelta(days=duree_jours)
        self.rendu = False

    def marquer_rendu(self):
        self.rendu = True
        self.livre.disponible = True

    def __str__(self):
        statut = "Rendu" if self.rendu else "En cours"
        return f"{self.livre.titre} emprunté par {self.utilisateur.prenom} {self.utilisateur.nom} ({statut})"
