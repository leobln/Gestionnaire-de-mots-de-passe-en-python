import hashlib, os

DOSSIER = "config"
VERROU  = os.path.join(DOSSIER, "verrou.txt")
INFOS   = os.path.join(DOSSIER, "donnees.txt")

def hacher(texte):
    """ Transforme le mdp en code de sécurité (ton exemple) """
    return hashlib.sha256(texte.encode()).hexdigest()

def crypter_decrypter(donnees, mdp):
    cle = hashlib.sha256(mdp.encode()).digest()
    taille_cle = len(cle)
    resultat_melange = []
    
    for i in range(len(donnees)):
        octet_origine = donnees[i]
        octet_cle = cle[i % taille_cle]
        octet_modifie = octet_origine ^ octet_cle
        resultat_melange.append(octet_modifie)

    return bytes(resultat_melange)

def verifier_mot_de_pass(essai):
    """ Vérifie le mot de passe et affiche le résultat """
    with open(VERROU, "r") as f:
        code_stocke = f.read()
    
    if hacher(essai) == code_stocke:
        print("Accès autorisé !")
        return True
    else:
        print(" Accès refusé !")
        return False

def lire_texte_clair(mdp):
    if not os.path.exists(INFOS):
        print("ℹAucun compte enregistré pour le moment.")
        return ""

    with open(INFOS, "rb") as f:
        donnees_cachees = f.read()

    donnees_claires = crypter_decrypter(donnees_cachees, mdp).decode()
    #print(" Données déchiffrées avec succès !")
    return donnees_claires

def enregistrer_texte(texte_total, mdp):
    """ Chiffre et écrit le texte dans le fichier """
    donnees_a_ecrire = crypter_decrypter(texte_total.encode(), mdp)
    with open(INFOS, "wb") as f:
        f.write(donnees_a_ecrire)



def main():
    
    if not os.path.exists(DOSSIER):
        os.makedirs(DOSSIER)

    
    if not os.path.exists(VERROU):
        mdp_neuf = input("Crée ton mot de passe maître : ")
        with open(VERROU, "w") as f:
            f.write(hacher(mdp_neuf))

    
    secret = input("Entrez le mot de passe maître : ")
    if verifier_mot_de_pass(secret):
        
        while True:
            print("\n--- MENU ---")
            choix = input("1:Voir | 2:Ajouter | 3:Quitter > ")

            if choix == "1":
                print("\n--- Tes comptes ---")
                print(lire_texte_clair(secret))

            elif choix == "2":
                s = input("Site : ")
                u = input("User : ")
                p = input("Pass : ")
                
                ancien = lire_texte_clair(secret)
                nouveau_contenu = ancien + f"{s} ; {u} ; {p}\n"
                enregistrer_texte(nouveau_contenu, secret)
                print("Ajouté avec succès !")

            elif choix == "3":
                print("Fermeture du coffre...")
                break 
            else:
                print("Choix invalide.")
    else:
        # Si le mot de passe est faux, le programme s'arrête ici
        print("Fin du programme.")

if __name__ == "__main__":
    main()