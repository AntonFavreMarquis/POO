class Livre:
    def __init__(self, titre, auteur, isbn):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True

    def __str__(self):
        etat = "✅ Disponible" if self.disponible else "❌ Emprunté"
        return f"{self.titre} - {self.auteur} (ISBN: {self.isbn}) [{etat}]"
