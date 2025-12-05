class Livre:
    def __init__(self, titre, auteur, annee, disponible=True):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.disponible = disponible

    def emprunter(self):
        if self.disponible:
            self.disponible = False
        else:
            raise Exception("Livre déjà emprunté")

    def rendre(self):
        self.disponible = True

    def to_dict(self):
        return {
            "titre": self.titre,
            "auteur": self.auteur,
            "annee": self.annee,
            "disponible": self.disponible
        }

    @staticmethod
    def from_dict(data):
        return Livre(
            titre=data["titre"],
            auteur=data["auteur"],
            annee=data["annee"],
            disponible=data["disponible"]
        )
