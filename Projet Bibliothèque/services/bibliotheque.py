from models.livre import Livre
from models.user import Utilisateur
from models.emprunt import Emprunt

class Bibliotheque:
    def __init__(self, nom):
        self.nom = nom
        self.livres = []
        self.utilisateurs = []
        self.emprunts = []

    # --- Gestion des livres ---
    def ajouter_livre(self, livre):
        self.livres.append(livre)

    def trouver_livre(self, isbn):
        for livre in self.livres:
            if livre.isbn == isbn:
                return livre
        return None

    # --- Gestion des utilisateurs ---
    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs.append(utilisateur)

    def trouver_utilisateur(self, identifiant):
        for user in self.utilisateurs:
            if user.identifiant == identifiant:
                return user
        return None

    # --- Gestion des emprunts ---
    def emprunter_livre(self, identifiant, isbn):
        utilisateur = self.trouver_utilisateur(identifiant)
        livre = self.trouver_livre(isbn)

        if not utilisateur or not livre:
            print("❌ Utilisateur ou livre introuvable.")
            return
        if not livre.disponible:
            print("⚠️ Livre déjà emprunté.")
            return

        emprunt = Emprunt(utilisateur, livre)
        livre.disponible = False
        utilisateur.emprunts.append(emprunt)
        self.emprunts.append(emprunt)
        print(f"✅ {utilisateur.prenom} a emprunté '{livre.titre}'.")

    def retourner_livre(self, identifiant, isbn):
        utilisateur = self.trouver_utilisateur(identifiant)
        if not utilisateur:
            print("❌ Utilisateur introuvable.")
            return
        for emprunt in utilisateur.emprunts:
            if emprunt.livre.isbn == isbn and not emprunt.rendu:
                emprunt.marquer_rendu()
                print(f"📘 Livre '{emprunt.livre.titre}' rendu avec succès.")
                return
        print("⚠️ Aucun emprunt correspondant trouvé.")
