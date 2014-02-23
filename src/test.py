from projet import *

def test() :

    print("Pour effectuer le test, veuillez décrire 3 automates ayants le même alphabet.\n")
    while True :
        while True :
            expr1 = input("Veuillez entrer l'expression régulière définissant le première automate utilisé pour le test :\n")
            try :
                aut1 = expression_vers_automate(expression_rationnelle_vers_liste(expr1))
            except :
                print("expression invalide")
            else :
                break
        print("Affichage du premier automate.\n")
        aut1.display()
        input("Appuyez sur entrée pour continuer le test.\n")

        while True :
            expr2 = input("Veuillez entrer l'expression régulière définissant le second automate utilisé pour le test :\n")
            try :
                aut2 = expression_vers_automate(expression_rationnelle_vers_liste(expr2))
            except :
                print("expression invalide")
            else :
                break
        print("Affichage du second automate.\n")
        aut2.display()
        input("Appuyez sur entrée pour continuer le test.\n")
        
        while True :
            expr3 = input("Veuillez entrer l'expression régulière définissant le troisième automate utilisé pour le test :\n")
            try :
                aut3 = expression_vers_automate(expression_rationnelle_vers_liste(expr3))
            except :
                print("expression invalide")
            else :
                break
        print("Affichage du troisième automate.\n")
        aut3.display()
        input("Appuyez sur entrée pour continuer le test.\n")

        print("Automate complet équivalent au première automate.\n")
        completer(aut1).display()
        input("Appuyez sur entrée pour continuer le test.\n")

        if aut1.get_alphabet() == aut2.get_alphabet() and aut2.get_alphabet() == aut3.get_alphabet() :
            print("Union minimisé du premier et du second automate.\n")
            autU = minimiser(union(aut1 , aut2))
            autU.display()
            input("Appuyez sur entrée pour continuer le test.\n")

            print("Intersection minimisé du troisième automate et de l'automate précédent.\n")
            autI = minimiser(intersection(autU,aut3))
            autI.display()
            input("Appuyez sur entrée pour continuer le test.\n")

        else :
            printf("Les 3 alphabets ne sont pas identiques.\n")

        print("Automate miroir du deuxième automate.\n")
        miroir(aut2).display()
        input("Appuyez sur entrée pour continuer le test.\n")

        print("Automate déterministe équivalent au troisième automate.\n")
        determiniser(aut3).display()
        input("Appuyez sur entrée pour continuer le test.\n")

        print("Automate complément du première automate.\n")
        complement(aut1).display()
        input("Appuyez sur entrée pour continuer le test.\n")

        s = ""
        while s != "oui" and s != "non" :
            s = input("Voulez-vous recommencer le test ? ( Répondre par \"oui\" ou \"non\" )\n")

        if s == "non" :
            break
        
        

        

        
