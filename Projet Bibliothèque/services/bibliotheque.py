# Interface complète avec gestion des livres ET des utilisateurs
# Version moderne avec sidebar + persistance JSON + gestion utilisateurs (Option B)

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from models.livre import Livre
from models.user import Utilisateur

class Bibliotheque:
    def __init__(self, fichier="bibliotheque.json"):
        self.fichier = fichier
        self.livres = []
        self.utilisateurs = []
        self.emprunts = []
        self.charger()

    # --- SAUVEGARDE GLOBALE ---
    def save(self):
        data = {
            "livres": [l.to_dict() for l in self.livres],
            "utilisateurs": [u.to_dict() for u in self.utilisateurs]
        }
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def charger(self):
        if not os.path.exists(self.fichier):
            return

        with open(self.fichier, "r", encoding="utf-8") as f:
            data = json.load(f)

        # --- Ancien format : une simple liste de livres ---
        if isinstance(data, list):
            self.livres = [Livre.from_dict(d) for d in data]
            self.utilisateurs = []  # pas d'utilisateurs dans l'ancien format
            self.save()
            return

        # --- Nouveau format : dictionnaire moderne ---
        self.livres = [Livre.from_dict(d) for d in data.get("livres", [])]
        self.utilisateurs = [Utilisateur.from_dict(u) for u in data.get("utilisateurs", [])]

    # --- Gestion Livres ---
    def ajouter_livre(self, livre):
        self.livres.append(livre)
        self.save()

    def supprimer_livre(self, titre):
        self.livres = [l for l in self.livres if l.titre != titre]
        self.save()

    def trouver_livre(self, titre):
        titre_norm = titre.strip().casefold()
        for livre in self.livres:
            print(f"[DEBUG LIVRE] stocké='{livre.titre}', recherche='{titre_norm}'")
            if livre.titre.strip().casefold() == titre_norm:
                return livre
        return None

    # --- Gestion Utilisateurs ---
    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs.append(utilisateur)
        self.save()

    def supprimer_utilisateur(self, identifiant):
        identifiant_norm = str(identifiant).strip().casefold()
        self.utilisateurs = [u for u in self.utilisateurs if str(u.identifiant).strip().casefold() != identifiant_norm]
        self.save()

    def trouver_utilisateur(self, identifiant):
        identifiant_norm = str(identifiant).strip().casefold()
        for user in self.utilisateurs:
            print(f"[DEBUG USER] stocké='{user.identifiant}', recherche='{identifiant_norm}'")
            if str(user.identifiant).strip().casefold() == identifiant_norm:
                return user
        return None
    # --- Emprunts ---
    def emprunter_livre(self, identifiant_user, titre):
        print(identifiant_user, titre)
        utilisateur = self.trouver_utilisateur(identifiant_user)
        livre = self.trouver_livre(titre)
        if not utilisateur or not livre:
            print("Utilisateur ou livre introuvable")
            raise Exception("Utilisateur ou livre introuvable")
        if not livre.disponible:
            print("Livre déjà emprunté")
            raise Exception("Livre déjà emprunté")
        livre.disponible = False
        utilisateur.emprunts.append(livre.titre)
        self.save()

    def rendre_livre(self, identifiant, titre):
        utilisateur = self.trouver_utilisateur(identifiant)
        livre = self.trouver_livre(titre)
        if not utilisateur or not livre:
            raise Exception("Utilisateur ou livre introuvable")
        if titre not in utilisateur.emprunts:
            raise Exception("Ce livre n'est pas emprunté par cet utilisateur")
        livre.disponible = True
        utilisateur.emprunts.remove(titre)
        self.save()
