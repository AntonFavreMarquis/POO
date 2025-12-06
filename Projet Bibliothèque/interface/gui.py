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
        self.root.title("📘 Bibliothèque")
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

        # TABLE LIVRES avec barre de recherche
        livres_frame = tk.Frame(main, bg="#121212")
        livres_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(livres_frame, text="📚 Livres", bg="#121212", fg="white",
                 font=("Segoe UI", 16)).pack(pady=5)

        # Barre de recherche livres
        search_livres_frame = tk.Frame(livres_frame, bg="#121212")
        search_livres_frame.pack(fill="x", pady=5)

        tk.Label(search_livres_frame, text="🔍 Rechercher:", bg="#121212", fg="white",
                 font=("Segoe UI", 10)).pack(side="left", padx=5)

        self.search_livre_entry = tk.Entry(search_livres_frame, font=("Segoe UI", 11), relief="flat", bg="#2a2a2a",
                                           fg="white")
        self.search_livre_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_livre_entry.bind("<KeyRelease>", self.search_livres)

        ttk.Button(search_livres_frame, text="✖ Effacer", style="Sidebar.TButton",
                   command=self.clear_search_livres).pack(side="left", padx=5)

        self.table_livres = ttk.Treeview(
            livres_frame,
            columns=("Titre", "Auteur", "Année", "Dispo"),
            show="headings",
        )
        for col in ("Titre", "Auteur", "Année", "Dispo"):
            self.table_livres.heading(col, text=col)
            self.table_livres.column(col, anchor="center")

        self.table_livres.pack(fill="both", expand=True)

        # TABLE UTILISATEURS avec barre de recherche
        users_frame = tk.Frame(main, bg="#121212")
        users_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(users_frame, text="👤 Utilisateurs", bg="#121212", fg="white",
                 font=("Segoe UI", 16)).pack(pady=5)

        # Barre de recherche utilisateurs
        search_users_frame = tk.Frame(users_frame, bg="#121212")
        search_users_frame.pack(fill="x", pady=5)

        tk.Label(search_users_frame, text="🔍 Rechercher:", bg="#121212", fg="white",
                 font=("Segoe UI", 10)).pack(side="left", padx=5)

        self.search_user_entry = tk.Entry(search_users_frame, font=("Segoe UI", 11), relief="flat", bg="#2a2a2a",
                                          fg="white")
        self.search_user_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_user_entry.bind("<KeyRelease>", self.search_users)

        ttk.Button(search_users_frame, text="✖ Effacer", style="Sidebar.TButton",
                   command=self.clear_search_users).pack(side="left", padx=5)

        self.table_users = ttk.Treeview(
            users_frame,
            columns=("Nom", "Prénom", "ID", "Nb Emprunts"),
            show="headings",
        )
        for col in ("Nom", "Prénom", "ID", "Nb Emprunts"):
            self.table_users.heading(col, text=col)
            self.table_users.column(col, anchor="center")

        self.table_users.pack(fill="x")


        # Dans create_layout(), après avoir créé les Treeview :
        self.table_livres.bind("<<TreeviewSelect>>", self.on_select_livre)
        self.table_users.bind("<<TreeviewSelect>>", self.on_select_user)
        self.table_livres.bind("<Button-1>", self.on_click_livre)
        self.table_users.bind("<Button-1>", self.on_click_user)

        # Variables pour traquer les sélections précédentes
        self.last_selected_livre = None
        self.last_selected_user = None

        ttk.Button(sidebar, text="Détails Utilisateur", style="Sidebar.TButton",
                   command=self.open_user_details).pack(fill="x", padx=20, pady=5)

    # ---------------------------------------------------------
    # ÉVÉNEMENTS DE SÉLECTION
    # ---------------------------------------------------------
    def on_click_livre(self, event):
        # Identifier l'item cliqué
        item_id = self.table_livres.identify_row(event.y)
        
        if item_id == self.last_selected_livre:
            # Si c'est le même item, désélectionner
            self.table_livres.selection_remove(item_id)
            self.last_selected_livre = None
        else:
            # Sinon, sélectionner le nouvel item
            self.last_selected_livre = item_id

    def on_click_user(self, event):
        # Identifier l'item cliqué
        item_id = self.table_users.identify_row(event.y)
        
        if item_id == self.last_selected_user:
            # Si c'est le même item, désélectionner
            self.table_users.selection_remove(item_id)
            self.last_selected_user = None
        else:
            # Sinon, sélectionner le nouvel item
            self.last_selected_user = item_id

    def on_select_livre(self, event):
        selection = self.table_livres.selection()
        if selection:
            self.last_selected_livre = selection[0]
            item = self.table_livres.item(selection)['values']
            # print(f"📚 Livre sélectionné : {item}")
        else:
            self.last_selected_livre = None

    def on_select_user(self, event):
        selection = self.table_users.selection()
        if selection:
            self.last_selected_user = selection[0]
            item = self.table_users.item(selection)['values']
            # print(f"👤 Utilisateur sélectionné : {item}")
        else:
            self.last_selected_user = None
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
            selection = self.table_users.selection()
            if not selection:
                messagebox.showerror("Erreur", "Sélectionne un utilisateur")
                return
                
            identifiant = self.table_users.item(selection[0])["values"][2]
            
            # Vérifier si l'utilisateur a des emprunts en cours
            user = self.bib.trouver_utilisateur(identifiant)
            if user and len(user.emprunts) > 0:
                response = messagebox.askyesno(
                    "Confirmation", 
                    f"L'utilisateur {user.nom} {user.prenom} a {len(user.emprunts)} emprunt(s) en cours.\n"
                    "Voulez-vous vraiment le supprimer? Les livres seront automatiquement rendus."
                )
                if not response:
                    return
                
                # Rendre tous les livres empruntés avant de supprimer l'utilisateur
                for livre_titre in user.emprunts.copy():
                    try:
                        self.bib.rendre_livre(identifiant, livre_titre)
                    except:
                        pass  # Ignorer les erreurs de retour
            
            # Supprimer l'utilisateur
            self.bib.supprimer_utilisateur(identifiant)
            self.refresh_users()
            self.refresh_livres()
            messagebox.showinfo("Succès", "Utilisateur supprimé avec succès")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")
    
    def voir_emprunts(self):
        """Afficher les emprunts de l'utilisateur sélectionné"""
        try:
            selection = self.table_users.selection()
            if not selection:
                messagebox.showerror("Erreur", "Sélectionne un utilisateur")
                return
                
            identifiant = self.table_users.item(selection[0])["values"][2]
            user = self.bib.trouver_utilisateur(identifiant)
            
            if not user:
                messagebox.showerror("Erreur", "Utilisateur introuvable")
                return
            
            if len(user.emprunts) == 0:
                messagebox.showinfo("Emprunts", f"{user.nom} {user.prenom} n'a aucun emprunt en cours.")
            else:
                emprunts_text = "\n".join([f"• {livre}" for livre in user.emprunts])
                messagebox.showinfo(
                    "Emprunts", 
                    f"Emprunts de {user.nom} {user.prenom}:\n\n{emprunts_text}"
                )
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")

    # ---------------------------------------------------------
    # 🔍 FONCTIONNALITÉS DE RECHERCHE
    # ---------------------------------------------------------
    def search_livres(self, event=None):
        """Filtrer les livres en fonction de la recherche"""
        search_term = self.search_livre_entry.get().strip().lower()

        # Effacer la table
        for row in self.table_livres.get_children():
            self.table_livres.delete(row)

        # Filtrer et afficher
        for l in self.bib.livres:
            # Recherche dans titre, auteur ou année
            if (search_term in l.titre.lower() or
                    search_term in l.auteur.lower() or
                    search_term in str(l.annee)):
                self.table_livres.insert("", "end", values=(
                    l.titre, l.auteur, l.annee,
                    "Oui" if l.disponible else "Non"
                ))

    def clear_search_livres(self):
        """Effacer la recherche et réafficher tous les livres"""
        self.search_livre_entry.delete(0, tk.END)
        self.refresh_livres()

    def search_users(self, event=None):
        """Filtrer les utilisateurs en fonction de la recherche"""
        search_term = self.search_user_entry.get().strip().lower()

        # Effacer la table
        for row in self.table_users.get_children():
            self.table_users.delete(row)

        # Filtrer et afficher
        for u in self.bib.utilisateurs:
            # Recherche dans nom, prénom ou identifiant
            if (search_term in u.nom.lower() or
                    search_term in u.prenom.lower() or
                    search_term in str(u.identifiant).lower()):
                self.table_users.insert("", "end", values=(
                    u.nom, u.prenom, u.identifiant,
                    len(u.emprunts)
                ))

    def clear_search_users(self):
        """Effacer la recherche et réafficher tous les utilisateurs"""
        self.search_user_entry.delete(0, tk.END)
        self.refresh_users()

    # ---------------------------------------------------------
    # Pop UP USER pour gestion d'emprunts
    # ---------------------------------------------------------
    def open_user_details(self):
        """Popup affichant les emprunts + dates + bouton pour rendre un livre"""

        # Vérifier sélection utilisateur
        selection = self.table_users.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionne un utilisateur")
            return

        identifiant = self.table_users.item(selection[0])["values"][2]
        user = self.bib.trouver_utilisateur(identifiant)

        if not user:
            messagebox.showerror("Erreur", "Utilisateur introuvable")
            return

        # --- FENÊTRE POPUP ---
        win = tk.Toplevel(self.root)
        win.title(f"Emprunts de {user.prenom} {user.nom}")
        win.geometry("550x500")
        win.configure(bg="#1e1e1e")
        win.grab_set()

        # Titre
        tk.Label(
            win,
            text=f"📖 Emprunts de {user.prenom} {user.nom}",
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)

        # TABLE
        table = ttk.Treeview(
            win,
            columns=("Livre", "Date Fin"),
            show="headings",
            height=10
        )

        table.heading("Livre", text="Livre")
        table.heading("Date Fin", text="Date de Retour")

        table.column("Livre", anchor="center", width=230)
        table.column("Date Fin", anchor="center", width=140)

        table.pack(fill="both", expand=True, padx=20, pady=10)

        # Remplir la table directement avec emprunts_detailles
        for emp in user.emprunts_detailles:
            table.insert("", "end", values=(emp["titre"], emp["date_fin"]))

        # --- Bouton rendre ---
        def rendre_selection():
            try:
                selection = table.selection()
                if not selection:
                    messagebox.showerror("Erreur", "Sélectionne un emprunt dans la liste")
                    return

                emprunt_values = table.item(selection[0])["values"]
                titre = emprunt_values[0]

                self.bib.rendre_livre(user.identifiant, titre)

                # Refresh interface principale
                self.refresh_livres()
                self.refresh_users()

                # Refresh popup table (user.emprunts_detailles est déjà à jour après rendre_livre)
                table.delete(*table.get_children())
                for emp in user.emprunts_detailles:
                    table.insert("", "end", values=(emp["titre"], emp["date_fin"]))

                messagebox.showinfo("Succès", f"Le livre '{titre}' a été rendu.")

            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ttk.Button(win, text="Rendre le livre sélectionné", command=rendre_selection).pack(pady=15)

