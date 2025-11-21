import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from services.bibliotheque import Bibliotheque
from models.livre import Livre
from models.user import Utilisateur



class Application(tb.Window):
    def __init__(self):
        super().__init__(
            title="📚 Bibliothèque ",
            themename="darkly",        # Thème moderne (dark)
            size=(800, 600),
            resizable=(False, False)
        )

        self.biblio = Bibliotheque("Bibliothèque Python")

        self.create_widgets()

    # -------------------------------------------------------------------------
    # CRÉATION DES ONGLET
    # -------------------------------------------------------------------------
    def create_widgets(self):
        notebook = tb.Notebook(self, bootstyle=PRIMARY)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.tab_livres = tb.Frame(notebook)
        self.tab_utilisateurs = tb.Frame(notebook)
        self.tab_emprunts = tb.Frame(notebook)

        notebook.add(self.tab_livres, text="📘 Livres")
        notebook.add(self.tab_utilisateurs, text="👤 Utilisateurs")
        notebook.add(self.tab_emprunts, text="🔄 Emprunts")

        self.create_tab_livres()
        self.create_tab_utilisateurs()
        self.create_tab_emprunts()

    # -------------------------------------------------------------------------
    # ONGLET LIVRES
    # -------------------------------------------------------------------------
    def create_tab_livres(self):
        frame_ajout = tb.Labelframe(self.tab_livres, text="Ajouter un livre", bootstyle=INFO)
        frame_ajout.pack(fill=X, padx=10, pady=10)

        tb.Label(frame_ajout, text="Titre :").grid(row=0, column=0, padx=5, pady=5)
        tb.Label(frame_ajout, text="Auteur :").grid(row=1, column=0, padx=5, pady=5)
        tb.Label(frame_ajout, text="ISBN :").grid(row=2, column=0, padx=5, pady=5)

        self.titre_entry = tb.Entry(frame_ajout)
        self.auteur_entry = tb.Entry(frame_ajout)
        self.isbn_entry = tb.Entry(frame_ajout)

        self.titre_entry.grid(row=0, column=1, padx=5, pady=5)
        self.auteur_entry.grid(row=1, column=1, padx=5, pady=5)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        tb.Button(frame_ajout, text="Ajouter le livre", bootstyle=SUCCESS,
                  command=self.ajouter_livre).grid(row=3, column=0, columnspan=2, pady=10)

        # Liste des livres
        self.liste_livres = tb.Treeview(self.tab_livres, columns=("Titre", "Auteur", "ISBN", "Statut"),
                                        show="headings", bootstyle=PRIMARY)
        for col in ("Titre", "Auteur", "ISBN", "Statut"):
            self.liste_livres.heading(col, text=col)
            self.liste_livres.column(col, width=150)

        self.liste_livres.pack(fill=BOTH, expand=True, padx=10, pady=10)

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

        self.titre_entry.delete(0, 'end')
        self.auteur_entry.delete(0, 'end')
        self.isbn_entry.delete(0, 'end')

    def mettre_a_jour_liste_livres(self):
        for row in self.liste_livres.get_children():
            self.liste_livres.delete(row)

        for livre in self.biblio.livres:
            statut = "Disponible" if livre.disponible else "Emprunté"
            self.liste_livres.insert("", "end",
                                     values=(livre.titre, livre.auteur, livre.isbn, statut))

    # -------------------------------------------------------------------------
    # ONGLET UTILISATEURS
    # -------------------------------------------------------------------------
    def create_tab_utilisateurs(self):
        frame_ajout = tb.Labelframe(self.tab_utilisateurs, text="Ajouter un utilisateur", bootstyle=INFO)
        frame_ajout.pack(fill=X, padx=10, pady=10)

        tb.Label(frame_ajout, text="Nom :").grid(row=0, column=0, padx=5, pady=5)
        tb.Label(frame_ajout, text="Prénom :").grid(row=1, column=0, padx=5, pady=5)
        tb.Label(frame_ajout, text="ID :").grid(row=2, column=0, padx=5, pady=5)

        self.nom_entry = tb.Entry(frame_ajout)
        self.prenom_entry = tb.Entry(frame_ajout)
        self.id_entry = tb.Entry(frame_ajout)

        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)
        self.prenom_entry.grid(row=1, column=1, padx=5, pady=5)
        self.id_entry.grid(row=2, column=1, padx=5, pady=5)

        tb.Button(frame_ajout, text="Ajouter l'utilisateur", bootstyle=SUCCESS,
                  command=self.ajouter_utilisateur).grid(row=3, column=0, columnspan=2, pady=10)

        self.liste_utilisateurs = tb.Treeview(self.tab_utilisateurs, columns=("Nom", "Prénom", "ID"),
                                              show="headings", bootstyle=PRIMARY)
        for col in ("Nom", "Prénom", "ID"):
            self.liste_utilisateurs.heading(col, text=col)
            self.liste_utilisateurs.column(col, width=150)

        self.liste_utilisateurs.pack(fill=BOTH, expand=True, padx=10, pady=10)

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

        self.nom_entry.delete(0, 'end')
        self.prenom_entry.delete(0, 'end')
        self.id_entry.delete(0, 'end')

    def mettre_a_jour_liste_utilisateurs(self):
        for row in self.liste_utilisateurs.get_children():
            self.liste_utilisateurs.delete(row)

        for user in self.biblio.utilisateurs:
            self.liste_utilisateurs.insert("", "end",
                                           values=(user.nom, user.prenom, user.identifiant))

    # -------------------------------------------------------------------------
    # ONGLET EMPRUNTS
    # -------------------------------------------------------------------------
    def create_tab_emprunts(self):
        frame = tb.Labelframe(self.tab_emprunts, text="Gérer les emprunts", bootstyle=INFO)
        frame.pack(fill=X, padx=10, pady=10)

        tb.Label(frame, text="ID Utilisateur :").grid(row=0, column=0, padx=5, pady=5)
        tb.Label(frame, text="ISBN Livre :").grid(row=1, column=0, padx=5, pady=5)

        self.id_emprunt_entry = tb.Entry(frame)
        self.isbn_emprunt_entry = tb.Entry(frame)

        self.id_emprunt_entry.grid(row=0, column=1, padx=5, pady=5)
        self.isbn_emprunt_entry.grid(row=1, column=1, padx=5, pady=5)

        tb.Button(frame, text="📥 Emprunter", bootstyle=SUCCESS, command=self.emprunter).grid(row=2, column=0, pady=10)
        tb.Button(frame, text="📤 Rendre", bootstyle=DANGER, command=self.rendre).grid(row=2, column=1, pady=10)

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
