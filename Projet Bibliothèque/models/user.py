class Utilisateur:
    # Constructeur : initialise un utilisateur avec nom, prénom et identifiant
    def __init__(self, nom, prenom, identifiant):
        self.nom = nom                       # Nom de l'utilisateur
        self.prenom = prenom                 # Prénom de l'utilisateur
        self.identifiant = identifiant       # Identifiant unique (ex: numéro)
        self.emprunts = []                   # Liste simple des titres empruntés (pour compatibilité)
        self.emprunts_detailles = []         # Liste détaillée : [{titre, date_fin}, ...] avec dates de retour

    # Méthode spéciale pour afficher l'utilisateur sous forme de texte lisible
    def __str__(self):
        return f"{self.prenom} {self.nom} (ID: {self.identifiant})"

    # Convertit l'objet Utilisateur en dictionnaire (utile pour sauvegarder en JSON)
    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "identifiant": self.identifiant,
            "emprunts": self.emprunts,                          # Sauvegarde la liste simple des titres
            "emprunts_detailles": self.emprunts_detailles       # Sauvegarde les détails avec dates de retour
        }

    # Méthode statique pour recréer un Utilisateur à partir d'un dictionnaire
    @staticmethod
    def from_dict(data):
        # Crée une nouvelle instance d'Utilisateur
        u = Utilisateur(
            data["nom"],                     # Restaure le nom
            data["prenom"],                  # Restaure le prénom
            data["identifiant"]              # Restaure l'identifiant
        )
        # Recharge la liste simple des emprunts (utilise une liste vide par défaut si absente)
        u.emprunts = data.get("emprunts", [])
        # Recharge la liste détaillée des emprunts avec dates (utilise une liste vide par défaut si absente)
        u.emprunts_detailles = data.get("emprunts_detailles", [])

        # Gestion de la rétrocompatibilité : convertit les anciennes données sans dates
        # Si l'utilisateur a des emprunts mais pas de détails, on génère les détails avec une date par défaut
        if u.emprunts and not u.emprunts_detailles:
            from datetime import datetime, timedelta
            # Pour chaque titre emprunté, crée une entrée détaillée avec date de retour (+14 jours)
            for titre in u.emprunts:
                u.emprunts_detailles.append({
                    "titre": titre,
                    "date_fin": (datetime.now() + timedelta(days=14)).strftime("%d/%m/%Y")
                })
        return u                              # Retourne l'utilisateur reconstruit

    # Méthode pour ajouter un emprunt avec sa date de retour
    def add_emprunt(self, titre, date_fin):
        # Ajoute le titre à la liste simple (pour compatibilité)
        self.emprunts.append(titre)
        # Ajoute les détails complets (titre + date de fin) à la liste détaillée
        self.emprunts_detailles.append({
            "titre": titre,
            "date_fin": date_fin
        })

    # Méthode pour retirer un emprunt (quand l'utilisateur rend le livre)
    def remove_emprunt(self, titre):
        # Supprime le titre de la liste simple s'il existe
        if titre in self.emprunts:
            self.emprunts.remove(titre)
        # Supprime l'entrée correspondante dans la liste détaillée (filtre tous les emprunts sauf celui-ci)
        self.emprunts_detailles = [e for e in self.emprunts_detailles if e["titre"] != titre]