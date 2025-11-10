class Utilisateur:
    def __init__(self, nom, prenom, identifiant):
        self.nom = nom
        self.prenom = prenom
        self.identifiant = identifiant
        self.emprunts = []  # liste d’objets Emprunt

    def __str__(self):
        return f"{self.prenom} {self.nom} (ID: {self.identifiant})"
