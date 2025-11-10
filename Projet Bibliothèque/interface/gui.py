import tkinter as tk
from tkinter import ttk, messagebox
from services.bibliotheque import Bibliotheque
from models.livre import Livre
from models.user import Utilisateur

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Bibliothèque Python")
        self.geometry("700x500")
        self.resizable(False, False)

        self.biblio = Bibliotheque("Bibliothèque Python")

        self.create_widgets()

    def create_widgets(self):
        # --- Onglets ---
        tab_control = ttk.Notebook(self)
        self.tab_livres = ttk.Frame(tab_control)
        self.tab_utilisateurs = ttk.Frame(tab_control)
        self.tab_emprunts = ttk.Frame(tab_control)
        tab_control.add(self.tab_livres, text="Livres")
        tab_control.add(self.tab_utilisateurs, text="Utilisateurs")
        tab_control.add(self.tab_emprunts, text="Emprunts")
        tab_control.pack(expand=1, fill="both")

        self.create_tab_livres()
        self.create_tab_utilisateurs()
        self.create_tab_emprunts()

    # --- Onglet Livres ---
    def create_tab_livres(self):
        frame_ajout = ttk.LabelFrame(self.tab_livres, text="Ajouter un livre")
        frame_ajout.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_ajout, text="Titre:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame_ajout, text="Auteur:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(frame_ajout, text="ISBN:").grid(row=2, column=0, padx=5, pady=5)

        self.titre_entry = ttk.Entry(frame_ajout)
        self.auteur_entry = ttk.Entry(frame_ajout)
        self.isbn_entry = ttk.Entry(frame_ajout)

        self.titre_entry.grid(row=0, column=1, padx=5, pady=5)
        self.auteur_entry.grid(row=1, column=1, padx=5, pady=5)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_ajout, text="Ajouter", command=self.ajouter_livre).grid(row=3, column=0, columnspan=2, pady=10)

        # Liste des livres
        self.liste_livres = ttk.Treeview(self.tab_livres, columns=("Titre", "Auteur", "ISBN", "Statut"), show="headings")
        for col in ("Titre", "Auteur", "ISBN", "Statut"):
            self.liste_livres.heading(col, text=col)
            self.liste_livres.column(col, width=150)
        self.liste_livres.pack(fill="both", expand=True, padx=10, pady=10)

    def ajouter_livre(self):
        titre = self.titre_entry.get()
        auteur = self.auteur_entry.get()
        isbn = self.isbn_entry.get()
        if not titre or not auteur or not isbn:
            messagebox.showwarning("Champs manquants", "Merci de remplir tous les champs.")
            return

        livre = Livre(titre, auteur, isbn)
        self.biblio.ajouter_livre(livre)
        self.mettre_a_jour_liste_livres()
        self.titre_entry.delete(0, tk.END)
        self.auteur_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)

    def mettre_a_jour_liste_livres(self):
        for row in self.liste_livres.get_children():
            self.liste_livres.delete(row)
        for livre in self.biblio.livres:
            statut = "Disponible" if livre.disponible else "Emprunté"
            self.liste_livres.insert("", "end", values=(livre.titre, livre.auteur, livre.isbn, statut))

    # --- Onglet Utilisateurs ---
    def create_tab_utilisateurs(self):
        frame_ajout = ttk.LabelFrame(self.tab_utilisateurs, text="Ajouter un utilisateur")
        frame_ajout.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_ajout, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame_ajout, text="Prénom:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(frame_ajout, text="ID:").grid(row=2, column=0, padx=5, pady=5)

        self.nom_entry = ttk.Entry(frame_ajout)
        self.prenom_entry = ttk.Entry(frame_ajout)
        self.id_entry = ttk.Entry(frame_ajout)

        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)
        self.prenom_entry.grid(row=1, column=1, padx=5, pady=5)
        self.id_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_ajout, text="Ajouter", command=self.ajouter_utilisateur).grid(row=3, column=0, columnspan=2, pady=10)

        # Liste des utilisateurs
        self.liste_utilisateurs = ttk.Treeview(self.tab_utilisateurs, columns=("Nom", "Prénom", "ID"), show="headings")
        for col in ("Nom", "Prénom", "ID"):
            self.liste_utilisateurs.heading(col, text=col)
            self.liste_utilisateurs.column(col, width=150)
        self.liste_utilisateurs.pack(fill="both", expand=True, padx=10, pady=10)

    def ajouter_utilisateur(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        identifiant = self.id_entry.get()
        if not nom or not prenom or not identifiant:
            messagebox.showwarning("Champs manquants", "Merci de remplir tous les champs.")
            return

        user = Utilisateur(nom, prenom, identifiant)
        self.biblio.ajouter_utilisateur(user)
        self.mettre_a_jour_liste_utilisateurs()
        self.nom_entry.delete(0, tk.END)
        self.prenom_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)

    def mettre_a_jour_liste_utilisateurs(self):
        for row in self.liste_utilisateurs.get_children():
            self.liste_utilisateurs.delete(row)
        for user in self.biblio.utilisateurs:
            self.liste_utilisateurs.insert("", "end", values=(user.nom, user.prenom, user.identifiant))

    # --- Onglet Emprunts ---
    def create_tab_emprunts(self):
        frame_actions = ttk.LabelFrame(self.tab_emprunts, text="Gérer les emprunts")
        frame_actions.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_actions, text="ID Utilisateur:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame_actions, text="ISBN Livre:").grid(row=1, column=0, padx=5, pady=5)

        self.id_emprunt_entry = ttk.Entry(frame_actions)
        self.isbn_emprunt_entry = ttk.Entry(frame_actions)

        self.id_emprunt_entry.grid(row=0, column=1, padx=5, pady=5)
        self.isbn_emprunt_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_actions, text="Emprunter", command=self.emprunter).grid(row=2, column=0, pady=10)
        ttk.Button(frame_actions, text="Rendre", command=self.rendre).grid(row=2, column=1, pady=10)

    def emprunter(self):
        id_user = self.id_emprunt_entry.get()
        isbn = self.isbn_emprunt_entry.get()
        self.biblio.emprunter_livre(id_user, isbn)
        self.mettre_a_jour_liste_livres()

    def rendre(self):
        id_user = self.id_emprunt_entry.get()
        isbn = self.isbn_emprunt_entry.get()
        self.biblio.retourner_livre(id_user, isbn)
        self.mettre_a_jour_liste_livres()
