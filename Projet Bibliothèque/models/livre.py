class Livre:
    # Constructeur : initialise un livre avec ses informations
    def __init__(self, titre, auteur, annee, disponible=True):
        self.titre = titre              # Titre du livre
        self.auteur = auteur            # Nom de l'auteur
        self.annee = annee              # Année de publication
        self.disponible = disponible    # Disponibilité du livre (True = empruntable)

    # Méthode pour emprunter le livre
    def emprunter(self):
        if self.disponible:
            self.disponible = False     # Le livre passe en état "non disponible"
        else:
            raise Exception("Livre déjà emprunté")  # On empêche un deuxième emprunt

    # Méthode pour rendre le livre
    def rendre(self):
        self.disponible = True          # Le livre redevient disponible

    # Convertit l'objet Livre en dictionnaire (utile pour sauvegarder en JSON)
    def to_dict(self):
        return {
            "titre": self.titre,
            "auteur": self.auteur,
            "annee": self.annee,
            "disponible": self.disponible
        }

    # Méthode statique pour reconstruire un objet Livre depuis un dictionnaire
    @staticmethod
    def from_dict(data):
        return Livre(
            titre=data["titre"],
            auteur=data["auteur"],
            annee=data["annee"],
            disponible=data["disponible"]
        )
