#-*- coding: cp1252 -*-

from automaton import *
from expressionRationnelle_yacc import *

yacc.yacc()

"""
Supprime un état donné d'un automate. Si l'état avait des transitions,
les efface également.
"""
def delete_state( Aut, state ) :

    alpha = list(Aut.get_alphabet())
    s = list(Aut.get_states())
    if state not in s :
        return Aut
    else :
        s.remove(state)
    
    init = list(Aut.get_initial_states())
    if state in init :
        init.remove(state)

    fin = list(Aut.get_final_states())
    if state in fin :
        fin.remove(state)

    trans = list(Aut.get_transitions())
    i = 0
    while i != len(trans) :
        if trans[i][0] == state or trans[i][2] == state :
            trans.pop(i)
        else :
            i+=1

    return automaton(
        epsilons = Aut.get_epsilons(),
        alphabet = alpha,
        states = s,
        initials = init,
        finals = fin,
        transitions = trans)



"""
Complète l'automate donné en lui ajoutant un état puits.
On ne modifie pas l'automate pris en paramètre, on utilise un clone.  
"""
def completer( Aut ):
    a = Aut.get_renumbered_automaton()
    s = list(a.get_states())
    alpha = list(a.get_alphabet() - a.get_epsilons())

    # On parcourt tous les états pour donner un nom correct à l'état puits.
    puits = a.get_maximal_id()
    if puits == None :
        puits = 0
    else :
        puits += 1
    a.add_state(puits)
    
    # On modifie ce booléen si on fait au moins une modification.
    complet = False 

    for i in range(len(alpha)) :
        for j in range(len(s)) :
            if len(a.delta(alpha[i], [s[j]],True)) == 0 :
                complet = True
                a.add_transition( (s[j], alpha[i], puits) )

    # Si complet = False, c'est que l'automate est déjà  complet, 
    # on enlève l'état puits.
    if not complet :
        a = delete_state(a, puits)
    else :
        for i in range(len(alpha)) :
            a.add_transition( (puits, alpha[i], puits) )

    return a


"""
Genere un ensemble de transitions ((x,y),a,(x',y')) tel que (x,a,x') appartient à l'automate a1 et (y,a,y') appartient à l'automate a2
"""
def nouvelles_transitions_IU(a1,a2,etats1,etats2,alpha) :
    trans = []

    for i in range( len(etats1) ) :
        for j in range( len(etats2) ) : # pour chaque couple de sommet (x,y)
            for k in range( len(alpha) ) : # pour chaque lettre
                l1 = list( a1.delta(alpha[k],[ etats1[i] ]) )
                l2 = list( a2.delta(alpha[k],[ etats2[j] ]) )
                for ii in range( len(l1) ) :
                    for jj in range( len(l2) ) : # pour chaque couple (x',y') accessible avec la lettre et le couple précédent
                        trans = trans + [( (etats1[i],etats2[j]), alpha[k] , (l1[ii],l2[jj]) )] # on crée la transition correspondante
    return trans


"""
Renvoie le produit cartésien de deux listes.
"""
def produit_cartesien( l1, l2 ) :
    l = list()
    for i in range(len(l1)) :
        for j in range(len(l2)) :
            l.append(tuple((l1[i], l2[j])))

    return l


"""
Retourne un automate construit 
sur l'union des deux automates passés en paramètres.
On considère l'union uniquement sur deux automates comprenant
le même alphabet, sinon renvoie un automate vide.
"""
def union( Aut1, Aut2 ) :
    Aut1 = completer(Aut1)
    Aut2 = completer(Aut2)
    
    alpha = list(Aut1.get_alphabet() - Aut1.get_epsilons())

    if alpha != list( Aut2.get_alphabet() - Aut2.get_epsilons() ) :
        return automaton()

    # Tous les états.
    et1 = list(Aut1.get_states())
    et2 = list(Aut2.get_states())
    et = produit_cartesien(et1, et2)

    # Les états finaux.
    f1 = produit_cartesien(list(Aut1.get_final_states()), et2)
    f2 = produit_cartesien(et1, list(Aut2.get_final_states()))

    for i in range(len(f1)) :
        if f1[i] not in f2 :
            f2.append(f1[i])

    # Les états initiaux.
    ini = produit_cartesien(list(Aut1.get_initial_states()), 
        list(Aut2.get_initial_states()))

    tr = nouvelles_transitions_IU(Aut1, Aut2, et1, et2, alpha)

    u = automaton( 
        alphabet = alpha,
        states = et,
        initials = ini,
        finals = f2,
        transitions = tr)
    
    u.renumber_the_states()
    return u


"""
Retourne un automate construit 
sur l'intersection des deux automates passés en paramètres.
On considère l'intersection uniquement sur deux automates comprenant
le même alphabet, sinon renvoie un automate vide.
"""
def intersection(aut1,aut2) :

    aut1 = completer(aut1)
    aut2 = completer(aut2)
    
    alpha = list(aut1.get_alphabet() - aut1.get_epsilons() )

    if alpha != list( aut2.get_alphabet() - aut2.get_epsilons() ) :
        return automaton()

    #Tous les états
    etats1 = list( aut1.get_states() )
    etats2 = list( aut2.get_states() )
    etats = produit_cartesien(etats1,etats2)

    # les etats initiaux
    ini1 = list( aut1.get_initial_states() )
    ini2 = list( aut2.get_initial_states() )
    ini = produit_cartesien(ini1,ini2)

    #lLes etats finaux
    fin1 = list( aut1.get_final_states() )
    fin2 = list( aut2.get_final_states() )
    fin = produit_cartesien(fin1,fin2)

    trans = nouvelles_transitions_IU(aut1, aut2,etats1,etats2,alpha)

    a = automaton(alphabet = alpha,
             states = etats,
             initials = ini,
             finals = fin,
             transitions = trans )
    a.renumber_the_states()
    return a

"""
Retourne l'automate miroir de l'automate Aut
"""
def miroir( Aut ) :

    trans = list( Aut.get_transitions() )
    newTrans = []
    for i in range( len(trans) ) :
        newTrans = newTrans + [(trans[i][2], trans[i][1], trans[i][0] )] #chaque transitions de la forme (x,a,y) et remplacé par la trnsition (y,a,x)
    
    a = automaton(
        epsilons = Aut.get_epsilons(),
        alphabet = Aut.get_alphabet(), 
        states = Aut.get_states(), 
        initials = Aut.get_final_states(), # les etats finaux deviennent initiaux
        finals = Aut.get_initial_states(), #les etats initiaux deviennent finaux
        transitions = newTrans )
    return a

def determiniser( aut ) :

    ini = aut.get_initial_states() # nouvelle etat defini par l'ensemble des etats initiaux
    states = [ini] #liste des nouveaux états
    trans = []
        
    alpha = aut.get_alphabet() - aut.get_epsilons()

    l = [ini]  # on enfile cette etat, dans la file des etats a traiter
    while( len(l) != 0 ) : # tant qu'on a des etats a traiter
        for i in alpha : # pour chaque lettre 
            tmp = aut.delta(i,l[0]) #on defini l'etat qu'il peut rejoindre
            if len(tmp) != 0 : #s'il y en a
                trans += [ ( l[0] , i , tmp ) ] #on crée la transitions
                if not tmp in states : #et s'il n'a jamais été vu, on le rajoute
                    states += [tmp]
                    l += [tmp]
        l.pop(0) #on defile l'etat traiter

    oldFinals = aut.get_final_states()
    fin = []
    for i in states :
        for j in i :
            if j in oldFinals : #pour chaque nouveaux sommet, si un des sommets qui le définie est final, il devient final
                fin += [i]
                break

    a = automaton(
        alphabet = alpha,
        states = states,
        initials = [ini],
        finals = fin,
        transitions = trans)
    a.renumber_the_states()
    return a

def complement( aut ) :

    a = completer(determiniser( aut ) )

    oldFinals = a.get_final_states()
    fin = []

    """
    Pour chaque sommet, s'il n'etait pas final, il le devient.
    """
    for i in a.get_states() :
        if not i in oldFinals :
            fin += [i]

    return automaton(
        alphabet = a.get_alphabet(),
        states = a.get_states(),
        initials = a.get_initial_states(),
        finals = fin,
        transitions = a.get_transitions())


"""
Fonction intermédiaire qui applique une fois l'algorithme de Moore.
Elle prend en paramètres l'automate concerné, la liste de ses
états, son alphabet et une liste de tuples représentant les valeurs
obtenues en appliquant l'algorithme au tour précédent:
lim = [(groupe de etats[0], groupe par alpha[0], groupe par alpha[1]...),
        (groupe de etats[1], etc...)]
"""
def moore( Aut, etats, alpha, lim ) :
    # On crée une nouvelle liste que l'on retournera.
    lmoore = list()

    # On renumérote les états pour donner les nouveaux groupes.
    gpe = -1;
    for i in range(len(lim)) :
        if lim[i] not in lim[:i] :
            gpe += 1
            lmoore.append(tuple((gpe,)))
        else :
            lmoore.append(tuple((lim.index(lim[i]),)))

    # On recrée les nouveaux groupes d'états.
    for i in range(len(lim)) :
        for j in range(len(alpha)) :
            d = list(Aut.delta(alpha[j], [ etats[i] ]))
            lmoore[i] = lmoore[i] + tuple((lmoore[etats.index(d[0])][0],))

    return lmoore

"""
Minimise un automate complet déterministe grâce à l'algorithme de Moore.

"""
def minimiser( Aut ) :

    Aut2 = completer( Aut )
    Aut2 = determiniser( Aut2 )

    etats = list(Aut2.get_states())
    alpha = list(Aut2.get_alphabet())

    # Initialisation. On sépare les états finaux du reste.
    lm1 = list()
    for i in range(len(etats)) :
        if Aut2.state_is_final(etats[i]) :
            lm1.append(tuple((1,)))
        else :
            lm1.append(tuple((0,)))
        for j in range(len(alpha)) :
            d = list(Aut2.delta(alpha[j], [ etats[i] ]))
            if Aut2.state_is_final(d[0]) :
                lm1[i] = lm1[i] + tuple((1,))
            else :
                lm1[i] = lm1[i] + tuple((0,))
    
    # On applique l'algorithme de Moore tant que la liste 
    # n'est pas stable.
    lm2 = moore(Aut2, etats, alpha, lm1)
    while lm1 != lm2 :
        lm1 = lm2
        lm2 = moore(Aut2, etats, alpha, lm1)

    # On récupère l'état initial.
    init = lm2[etats.index(list(Aut2.get_initial_states())[0])][0]

    # On recherche les nouveaux états finaux.
    lm1 = list()
    ets = list()
    for i in range(len(etats)) :
        if Aut2.state_is_final(etats[i]) :
            lm1.append(lm2[i][0])
        ets.append(lm2[i][0])
    # On enlève les doublons
    # lm1 la liste des états finaux.
    # lm2 la totalité des états et des transitions.
    # ets la liste de tous les états.
    lm1 = list(set(lm1))
    lm2 = list(set(lm2))
    ets = list(set(ets))

    amin = automaton(
        alphabet = alpha,
        states = ets,
        initials = [init],
        finals = lm1)

    # On récupère les nouvelles transitions.
    for i in range(len(lm2)) :
        for j in range(len(alpha)) :
            amin.add_transition( (lm2[i][0], alpha[j], lm2[i][j + 1]) )

    return amin



""" 
expression vers automate
"""

"""
Fonction intermédiaire servant de pseudo-switch entre les differentes operation possibles.
"""
def operation(expr) :
    if len(expr) != 0 :
        if expr[0] == '*' :
            return etoile(expr[1])
        elif expr[0] == '+' :
            return unionEVA(expr[1],expr[2])
        elif expr[0] == '.' :
            return concatenation(expr[1],expr[2])
        elif len(expr) == 1 :
            return automaton(alphabet = expr,
                    states = [1,2],
                    initials = [1],
                    finals = [2],
                    transitions = [ (1 , expr , 2) ] )
        
    return None

"""
Chercher un charactere n'appartenant pas à l'alphabet et le retourne.
"""
def generer_epsilon(alpha) :
    i = 0
    while( True ) :
        if not str(i) in alpha :
            return str(i)
        i += 1


"""
Retourne l'automate correspondant à l'expression expr.
"""
def expression_vers_automate( expr ) :
    return operation(expr)

"""
Applique "Etoile" à l'automate defini par l'expression expr.
"""
def etoile(expr) :
    aut = operation(expr) # on recupere l'automate defini par expr.
    
    """
    On crée les etats nécessaires.
    """
    s1 = aut.get_maximal_id()
    if s1 == None :
        s1 = 0
    else :
        s1 += 1
    s2 = s1 + 1
    s3 = s2 + 1
    s4 = s3 + 1

    alpha = aut.get_alphabet()
    
    #On récupère un charactère definissant epsilons.
    if(aut.has_epsilon_characters()) :
        epsilon = list(aut.get_epsilons())[0]
    else :
        epsilon = generer_epsilon(alpha)

    #on genere les nouvelles transitions nécessaire.
    transitions = list( aut.get_transitions() ) 
    transitions += [ (s1 , epsilon , s2) ,
             (s1 , epsilon , s4) ,
             (s3 , epsilon , s2) ,
             (s3 , epsilon , s4) ]
    for i in aut.get_initial_states() :
        transitions += [ (s2 , epsilon , i ) ]
    for i in aut.get_final_states() :
        transitions += [ ( i , epsilon , s3 ) ]

    return automaton(
        alphabet = alpha,
        epsilons = [epsilon] + list(aut.get_epsilons()) ,
        states = list(aut.get_states()) + [s1 , s2 , s3, s4] ,
        initials = [s1] ,
        finals = [s4],
        transitions = transitions)

"""
Retourne l'automate union des automates correspondant à expr1 et expr2.
"""
def unionEVA(expr1,expr2) :

    #on récupère les automates correspondant à expr1 et expr2
    aut1 = operation(expr1)
    aut2 = operation(expr2)

    aut1.renumber_the_states()
    aut2.renumber_the_states()
    x = aut1.get_maximal_id()
    if x == None :
        x = 0
    else :
        x += 1
        
    def rajouter(y) :
        return y + x

    aut2.map(rajouter)

    #on génère le nouvel alphabet et on fusionne tous les epsilons en un même symbole,
    #permet d'éviter les problèmes liés au fait qu'un epsilon de aut1
    #peut être dans l'alphabet de aut2, et inversement.
    old_epsilon1 = aut1.get_epsilons()
    old_epsilon2 = aut2.get_epsilons()
    
    alpha1 = list( aut1.get_alphabet()  - old_epsilon1 )
    alpha2 = list( aut2.get_alphabet()  - old_epsilon2 )
    
    alpha = list( aut1.get_alphabet() - old_epsilon1 )
    for i in alpha2 :
        if not i in alpha :
            alpha += [i]

    epsilon = generer_epsilon(alpha)

    transitions = []

    for i in aut1.get_transitions() :
        if i[1] in old_epsilon1 :
            transitions += [ ( i[0] , epsilon , i[2] ) ]
        else :
            transitions += [i]
    for i in aut2.get_transitions() :
        if i[1] in old_epsilon2 :
            transitions += [ ( i[0] , epsilon , i[2] ) ]
        else :
            transitions += [i]
            
    #creation de l'automate union
    s1 = aut2.get_maximal_id()
    if s1 == None :
        s1 = 0
    else :
        s1 += 1
    s2 = s1 + 1

    for i in aut1.get_initial_states() :
        transitions += [ (s1 , epsilon , i ) ]
    for i in aut1.get_final_states() :
        transitions += [ (i , epsilon , s2) ]
    for i in aut2.get_initial_states() :
        transitions += [ (s1 , epsilon , i ) ]
    for i in aut2.get_final_states() :
        transitions += [ (i , epsilon , s2) ]

    return automaton( alphabet = alpha ,
              epsilons = [ epsilon ] ,
              finals = [s2] ,
              initials = [s1] ,
              transitions = transitions )


"""
Retourne l'automate correspondant à la concaténation des automates définis par expr1 et expr2.
"""
def concatenation(expr1,expr2) :

    #on renomme les états au cas où il y aurait des redondances
    aut1 = operation(expr1)
    aut2 = operation(expr2)

    aut1.renumber_the_states()
    aut2.renumber_the_states()
    x = aut1.get_maximal_id()
    if x == None :
        x = 0
    else :
        x+=1

    def rajouter(y) :
        return y + x

    aut2.map(rajouter)

    #on génère le nouvel alphabet et on fusionne tous les epsilons en un même symbole,
    #permet d'éviter les problèmes liés au fait qu'un epsilon de aut1
    #peut être dans l'alphabet de aut2, et inversement.
    old_epsilon1 = aut1.get_epsilons()
    old_epsilon2 = aut2.get_epsilons()
    
    alpha1 = list( aut1.get_alphabet()  - old_epsilon1 )
    alpha2 = list( aut2.get_alphabet()  - old_epsilon2 )
    
    alpha = list( aut1.get_alphabet() - old_epsilon1 )
    for i in alpha2 :
        if not i in alpha :
            alpha += [i]

    epsilon = generer_epsilon(alpha)

    transitions = []

    for i in aut1.get_transitions() :
        if i[1] in old_epsilon1 :
            transitions += [ ( i[0] , epsilon , i[2] ) ]
        else :
            transitions += [i]
    for i in aut2.get_transitions() :
        if i[1] in old_epsilon2 :
            transitions += [ ( i[0] , epsilon , i[2] ) ]
        else :
            transitions += [i]
            
    #creation de l'automate concaténation
    s1 = aut2.get_maximal_id()
    if s1 == None :
        s1 = 0
    else :
        s1 += 1
    s2 = s1 + 1

    for i in aut1.get_initial_states() :
        transitions += [ (s1 , epsilon , i ) ]
    for i in aut1.get_final_states() :
        for j in aut2.get_initial_states() :
            transitions += [ (i , epsilon , j) ]
    for i in aut2.get_final_states() :
        transitions += [ (i , epsilon , s2) ]

    return automaton( alphabet = alpha ,
              epsilons = [ epsilon ] ,
              finals = [s2] ,
              initials = [s1] ,
              transitions = transitions )


def expression_rationnelle_vers_liste(s) :
    return yacc.parse(expr_concat(s))


"""
Retourne une expression avec la concaténation explicite: '.'
Par exemple, la chaîne 'a+bc' deviendra 'a+b.c'
"""
def expr_concat ( expr ) :
    expr2 = expr[0]
    for i in range(1,len(expr)):
        # On rajoute entre deux caractères si celui d'avant est:
        # une parenthèse fermante, une étoile ou une lettre,
        # et celui d'après est une lettre ou une parenthèse ouvrante.
        if expr[i] not in [')', '+', '.', '*'] and expr2[len(expr2) - 1] not in ['(', '+', '.'] :
            expr2 += '.'
        expr2 += expr[i]

    return expr2


"""
Renvoie un booléen vérifiant si l'expression passée en paramètre est
syntaxiquement correcte ou non. Utile pour l'implémentation Python
de l'expression vers la liste préfixe.
"""
def est_correcte_expr ( expr ) :
    # 'par' sert à vérifier que l'expression est bien parenthèsée.
    # Il est incrémenté quand on voit '(', et décrémenté pour ')'.
    # Il ne doit jamais être inférieur à zéro, et doit être égal
    # à zéro à la fin du parcours de l'expression.
    par = 0

    if expr[0] in [')', '+', '.', '*'] :
        return False

    for i in range(len(expr)-1) :
        # Pour chaque symbole, on regarde ceux qui peuvent suivre
        # le symbole lu.
        if expr[i] == '(' :
            par += 1
            if  expr[i + 1] in [')', '+', '.', '*'] :
                return False
        elif expr[i] == ')' :
            par -= 1
            if par < 0 or expr[i + 1] not in [')', '+', '.', '*'] :
                return False
        elif expr[i] in ['+', '.'] :
            if expr[i + 1] in [')', '+', '.', '*'] :
                return False
        elif expr[i] == '*' :
            if expr[i + 1] not in [')', '+', '.'] :
                return False
        else :
            if expr[i + 1] not in [')', '+', '.', '*'] :
                return False

    # Pour le dernier caractère, on regarde si c'est un caractère qui peut
    # finir une expression, et si c'est le cas, les caractères qui
    # peuvent le précéder.
    if expr[len(expr) - 1] == '*' :
        if expr[len(expr) - 2] in ['(', '+', '.', '*'] :
            return False
    elif expr[len(expr) - 1] == ')' :
        par -= 1
        if expr[len(expr) - 2] in ['(', '+', '.'] :
            return False
    elif expr[len(expr) - 1] in ['(', '+', '.'] :
        return False
    else :
        if expr[len(expr) - 2] not in ['+', '.'] :
            return False

    # Expression bien parenthèsée.
    return par == 0


"""
Renvoie la liste en écriture préfixe de l'expression rationnelle donnée.
L'expression passée en paramètre peut contenir des concaténations implicites
'ab+cd', explicites 'a.b+c.d', ou les deux. Elle peut également contenir
des espaces pour aider à la lecture, ils ne seront pas traités.
exemple : 'a.b(c + d)* + b.c + a'
"""
def expr_rationnelle_vers_liste_bis ( expr ) :
    # On va utiliser une pile l.
    l = list()

    # On efface les éventuels espaces inutiles, et on rajoute les 
    # concaténations explicitement.
    exp = expr.split(" ")
    exp = "".join(exp)
    exp = expr_concat(exp)
    # On vérifie que l'expression est correcte
    if not est_correcte_expr( exp ) :
        print('erreur de syntaxe')
        return l

    for i in range(len(exp)) :

        # On teste tous les cas possibles dans un pseudo-switch.
        if exp[i] == '*' :
            tmp = l.pop()
            l.append(list(('*', tmp)))

        # On traitera l'entité à l'intérieur des parenthèses une fois
        # la parenthèse fermante correspondante trouvée.
        elif exp[i] == '(' :
            l.append('(')

        # Si le plus arrive après une autre opération, c'est que l'on
        # peut évaluer cette/ces opérations, l'empiler et continuer.
        elif exp[i] == '+' :
            if len(l) == 1 or l[len(l)-2] =='(' :
                l.append('+')
            else :
                while l[len(l) - 2] in ['.', '+'] and len(l) > 2:
                    arg2 = l.pop()
                    op = l.pop()
                    arg1 = l.pop()
                    l.append(list((op, arg1, arg2)))
                l.append('+')

        # Même principe que pour le '+', en rajoutant une priorité à
        # la concaténation.
        elif exp[i] == '.' :
            if len(l) == 1 or l[len(l)-2] in ['(', '+']:
                l.append('.')
            elif l[len(l) - 2] == '.' :
                arg2 = l.pop()
                op = l.pop()
                arg1 = l.pop()
                l.append(list((op, arg1, arg2)))
                l.append('.')

        # On évalue l'intérieur des parenthèses.
        elif exp[i] == ')' :
            while l[len(l)-2] != '(' :
                arg2 = l.pop()
                op = l.pop()
                arg1 = l.pop()
                l.append(list((op, arg1, arg2)))
            l.pop(len(l)-2) #parenthese ouvrante
            

        # tout le reste: une lettre de l'alphabet.
        else :
            l.append(exp[i])

    # On s'assure que toutes les expressions ont bien été transformées,
    # ce qui n'est pas le cas si l'expression se termine
    # par une lettre, par exemple.
    while l[len(l) - 2] in ['+', '.'] :
        arg2 = l.pop()
        op = l.pop()
        arg1 = l.pop()
        l.append(list((op, arg1, arg2)))

    if len(l) == 1 :
        return l[0]

    return l
