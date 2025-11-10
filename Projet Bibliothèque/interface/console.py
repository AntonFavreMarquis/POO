from services.bibliotheque import Bibliotheque
from models.livre import Livre
from models.user import Utilisateur

def menu():
    print("\n--- Menu ---")
    print("1. Ajouter un livre")
    print("2. Ajouter un utilisateur")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Afficher les livres")
    print("6. Quitter")

def lancer_console():
    biblio = Bibliotheque("Bibliothèque Python")

    while True:
        menu()
        choix = input("Choisissez une option : ")

        if choix == "1":
            titre = input("Titre : ")
            auteur = input("Auteur : ")
            isbn = input("ISBN : ")
            biblio.ajouter_livre(Livre(titre, auteur, isbn))
        elif choix == "2":
            nom = input("Nom : ")
            prenom = input("Prénom : ")
            identifiant = input("ID utilisateur : ")
            biblio.ajouter_utilisateur(Utilisateur(nom, prenom, identifiant))
        elif choix == "3":
            identifiant = input("ID utilisateur : ")
            isbn = input("ISBN du livre : ")
            biblio.emprunter_livre(identifiant, isbn)
        elif choix == "4":
            identifiant = input("ID utilisateur : ")
            isbn = input("ISBN du livre : ")
            biblio.retourner_livre(identifiant, isbn)
        elif choix == "5":
            for livre in biblio.livres:
                print(livre)
        elif choix == "6":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide.")
