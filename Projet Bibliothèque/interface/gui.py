# Interface complète avec gestion des livres ET des utilisateurs
# Version moderne avec sidebar + persistance JSON + gestion utilisateurs (Option B)

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from models.livre import Livre
from models.user import Utilisateur
from models.emprunt import Emprunt
from services.bibliotheque import Bibliotheque


class InterfaceBibliotheque:
    def __init__(self):
        self.bib = Bibliotheque()

        self.root = tk.Tk()
        self.root.title("📘 Bibliothèque Moderne")
        self.root.geometry("1100x650")
        self.root.configure(bg="#121212")

        self.configure_style()
        self.create_layout()

        self.refresh_livres()
        self.refresh_users()

        self.root.mainloop()

    # ---------------------------------------------------------
    # STYLE
    # ---------------------------------------------------------
    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            rowheight=28,
            fieldbackground="#1e1e1e",
            bordercolor="#1e1e1e",
        )
        style.map("Treeview", background=[("selected", "#3a7cfc")])

        style.configure(
            "Sidebar.TButton",
            background="#2a2a2a",
            foreground="white",
            padding=10,
            relief="flat",
            font=("Segoe UI", 12),
        )
        style.map("Sidebar.TButton", background=[("active", "#3a3a3a")])

    # ---------------------------------------------------------
    # LAYOUT (SIDEBAR + TABLE ZONES)
    # ---------------------------------------------------------
    def create_layout(self):
        sidebar = tk.Frame(self.root, bg="#1b1b1b", width=230)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="📘 BIBLIOTHÈQUE",
            bg="#1b1b1b",
            fg="white",
            font=("Segoe UI", 16, "bold"),
            pady=20,
        ).pack()

        # --- Boutons gestion livres ---
        ttk.Button(sidebar, text="Ajouter Livre", style="Sidebar.TButton",
                   command=self.ajouter_livre).pack(fill="x", padx=20, pady=5)

        ttk.Button(sidebar, text="Supprimer Livre", style="Sidebar.TButton",
                   command=self.supprimer_livre).pack(fill="x", padx=20, pady=5)

        ttk.Button(sidebar, text="Emprunter Livre", style="Sidebar.TButton",
                   command=self.emprunter_livre).pack(fill="x", padx=20, pady=5)

        ttk.Button(sidebar, text="Rendre Livre", style="Sidebar.TButton",
                   command=self.rendre_livre).pack(fill="x", padx=20, pady=5)

        # --- Boutons gestion utilisateurs ---
        tk.Label(sidebar, text="Gestion Utilisateurs", bg="#1b1b1b",
                 fg="white", font=("Segoe UI", 14, "bold"), pady=18).pack()

        ttk.Button(sidebar, text="Ajouter Utilisateur", style="Sidebar.TButton",
                   command=self.ajouter_user).pack(fill="x", padx=20, pady=5)

        ttk.Button(sidebar, text="Supprimer Utilisateur", style="Sidebar.TButton",
                   command=self.supprimer_user).pack(fill="x", padx=20, pady=5)

        # -----------------------------------------------------
        # MAIN AREA = Livres + Utilisateurs côte-à-côte
        # -----------------------------------------------------
        main = tk.Frame(self.root, bg="#121212")
        main.pack(side="right", fill="both", expand=True)

        # TABLE LIVRES
        tk.Label(main, text="📚 Livres", bg="#121212", fg="white",
                 font=("Segoe UI", 16)).pack(pady=10)

        self.table_livres = ttk.Treeview(
            main,
            columns=("Titre", "Auteur", "Année", "Dispo"),
            show="headings",
        )
        for col in ("Titre", "Auteur", "Année", "Dispo"):
            self.table_livres.heading(col, text=col)
            self.table_livres.column(col, anchor="center")

        self.table_livres.pack(fill="both", expand=True, padx=20, pady=10)

        # TABLE UTILISATEURS
        tk.Label(main, text="👤 Utilisateurs", bg="#121212", fg="white",
                 font=("Segoe UI", 16)).pack(pady=10)

        self.table_users = ttk.Treeview(
            main,
            columns=("Nom", "Prénom", "ID", "Nb Emprunts"),
            show="headings",
        )
        for col in ("Nom", "Prénom", "ID", "Nb Emprunts"):
            self.table_users.heading(col, text=col)
            self.table_users.column(col, anchor="center")

        self.table_users.pack(fill="x", padx=20, pady=10)

        # Dans create_layout(), après avoir créé les Treeview :
        self.table_livres.bind("<<TreeviewSelect>>", self.on_select_livre)
        self.table_users.bind("<<TreeviewSelect>>", self.on_select_user)

    # ---------------------------------------------------------
    # ÉVÉNEMENTS DE SÉLECTION
    # ---------------------------------------------------------
    def on_select_livre(self, event):
        selection = self.table_livres.selection()
        if selection:
            item = self.table_livres.item(selection)["values"]
            # print(f"📚 Livre sélectionné : {item}")

    def on_select_user(self, event):
        selection = self.table_users.selection()
        if selection:
            item = self.table_users.item(selection)["values"]
            # print(f"👤 Utilisateur sélectionné : {item}")
    # ---------------------------------------------------------
    # REFRESH TABLES
    # ---------------------------------------------------------
    def refresh_livres(self):
        for row in self.table_livres.get_children():
            self.table_livres.delete(row)
        for l in self.bib.livres:
            self.table_livres.insert("", "end", values=(l.titre, l.auteur, l.annee,
                                                          "Oui" if l.disponible else "Non"))

    def refresh_users(self):
        for row in self.table_users.get_children():
            self.table_users.delete(row)
        for u in self.bib.utilisateurs:
            self.table_users.insert("", "end", values=(u.nom, u.prenom, u.identifiant,
                                                         len(u.emprunts)))

    # ---------------------------------------------------------
    # POPUPS UTILES
    # ---------------------------------------------------------
    def popup(self, title, size="350x300"):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(size)
        win.configure(bg="#1e1e1e")
        win.grab_set()
        return win

    def input_field(self, parent, label):
        tk.Label(parent, text=label, bg="#1e1e1e", fg="white",
                 font=("Segoe UI", 11)).pack(pady=5)
        entry = tk.Entry(parent, font=("Segoe UI", 12), relief="flat")
        entry.pack(fill="x", padx=20)
        return entry

    # ---------------------------------------------------------
    # 📚 GESTION DES LIVRES
    # ---------------------------------------------------------
    def ajouter_livre(self):
        win = self.popup("Ajouter un Livre")

        e_titre = self.input_field(win, "Titre :")
        e_auteur = self.input_field(win, "Auteur :")
        e_annee = self.input_field(win, "Année :")

        def valider():
            try:
                livre = Livre(e_titre.get(), e_auteur.get(), int(e_annee.get()))
                self.bib.ajouter_livre(livre)
                self.refresh_livres()
                win.destroy()
            except:
                messagebox.showerror("Erreur", "Données invalides")

        ttk.Button(win, text="Ajouter", command=valider).pack(pady=15)

    def supprimer_livre(self):
        try:
            item = self.table_livres.item(self.table_livres.selection())["values"]
            titre = item[0]
            self.bib.supprimer_livre(titre)
            self.refresh_livres()
        except:
            messagebox.showerror("Erreur", "Sélectionne un livre")

    def emprunter_livre(self):
        try:
            print(self.table_livres.selection())
            print(self.table_users.selection())
            livre = self.table_livres.item(self.table_livres.selection())["values"][0]
            user = self.table_users.item(self.table_users.selection())["values"][2]
            self.bib.emprunter_livre(user, livre)
            self.refresh_livres()
            self.refresh_users()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def rendre_livre(self):
        try:
            livre = self.table_livres.item(self.table_livres.selection())["values"][0]
            user = self.table_users.item(self.table_users.selection())["values"][2]
            self.bib.rendre_livre(user, livre)
            self.refresh_livres()
            self.refresh_users()
        except:
            messagebox.showerror("Erreur", "Sélectionne un utilisateur et un livre")

    # ---------------------------------------------------------
    # 👤 GESTION DES UTILISATEURS
    # ---------------------------------------------------------
    def ajouter_user(self):
        win = self.popup("Ajouter un Utilisateur")

        e_nom = self.input_field(win, "Nom :")
        e_prenom = self.input_field(win, "Prénom :")
        e_id = self.input_field(win, "Identifiant :")

        def valider():
            user = Utilisateur(e_nom.get(), e_prenom.get(), e_id.get())
            self.bib.ajouter_utilisateur(user)
            self.refresh_users()
            win.destroy()

        ttk.Button(win, text="Ajouter", command=valider).pack(pady=15)

    def supprimer_user(self):
        try:
            identifiant = self.table_users.item(self.table_users.selection())["values"][2]
            self.bib.supprimer_utilisateur(identifiant)
            self.refresh_users()
        except:
            messagebox.showerror("Erreur", "Sélectionne un utilisateur")

# (I will generate the full updated code including user management on your next instruction.)
