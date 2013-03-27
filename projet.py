#-*- coding: cp1252 -*-

from automaton import *
from expressionRationnelle_yacc import *

yacc.yacc()

"""
Supprime un �tat donn� d'un automate. Si l'�tat avait des transitions,
les efface �galement.
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

	return automaton(alphabet = alpha,
		states = s,
		initials = init,
		finals = fin,
		transitions = trans)



"""
Compl�te l'automate donn� en lui ajoutant un �tat puit.
On ne modifie pas l'automate pris en param�tre, on utilise un clone.  
"""
def completer( Aut ):
	a = Aut.get_renumbered_automaton()
	s = list(a.get_states())
	alpha = list(a.get_alphabet())

	# On parcourt tous les �tats pour donner un nom correct � l'�tat puit.
	puit = a.get_maximal_id() + 1
	a.add_state(puit)
	
	# On modifie ce bool�en si on fait au moins une modification.
	complet = False 

	for i in range(len(alpha)) :
		for j in range(len(s)) :
			if len(a.delta(alpha[i], [s[j]])) == 0 :
				complet = True
				a.add_transition( (s[j], alpha[i], puit) )

	# Si complet = False, c'est que l'automate est d�j� complet, 
	# on enl�ve l'�tat puit.
	if not complet :
		a = delete_state(a, puit)
	else :
		for i in range(len(alpha)) :
			a.add_transition( (puit, alpha[i], puit) )

	return a

def nouvelles_transitions_IU(a1,a2,etats1,etats2,alpha) :
	trans = []

	for i in range( len(etats1) ) :
		for j in range( len(etats2) ) :
			for k in range( len(alpha) ) :
				l1 = list( a1.delta(alpha[k],[ etats1[i] ]) )
				l2 = list( a2.delta(alpha[k],[ etats2[j] ]) )
				for ii in range( len(l1) ) :
					for jj in range( len(l2) ) :
						trans = trans + [( (etats1[i],etats2[j]), alpha[k] , (l1[ii],l2[jj]) )]
	return trans


"""
Renvoie le produit cart�sien de deux listes.
"""
def produit_cartesien( l1, l2 ) :
	l = list()
	for i in range(len(l1)) :
		for j in range(len(l2)) :
			l.append(tuple((l1[i], l2[j])))

	return l


"""
Retourne un automate construit 
sur l'union des deux automates pass�s en param�tres.
On consid�re l'union uniquement sur deux automates comprenant
le m�me alphabet.
"""
def union( Aut1, Aut2 ) :
	Aut1 = completer(Aut1)
	Aut2 = completer(Aut2)
	
	alpha = list(Aut1.get_alphabet())

	if alpha != list( Aut2.get_alphabet() ) :
		return None

	# Tous les �tats.
	et1 = list(Aut1.get_states())
	et2 = list(Aut2.get_states())
	et = produit_cartesien(et1, et2)

	# Les �tats finaux.
	f1 = produit_cartesien(list(Aut1.get_final_states()), et2)
	f2 = produit_cartesien(et1, list(Aut2.get_final_states()))

	for i in range(len(f1)) :
		if f1[i] not in f2 :
			f2.append(f1[i])

	# Les �tats initiaux.
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
sur l'intersection des deux automates pass�s en param�tres.
On consid�re l'intersection uniquement sur deux automates comprenant
le m�me alphabet.
"""
def intersection(aut1,aut2) :

	aut1 = completer(aut1)
	aut2 = completer(aut2)
	
	alpha = list(aut1.get_alphabet())

	if alpha != list( aut2.get_alphabet() ) :
		return None

	etats1 = list( aut1.get_states() )
	etats2 = list( aut2.get_states() )
	etats = produit_cartesien(etats1,etats2)

	ini1 = list( aut1.get_initial_states() )
	ini2 = list( aut2.get_initial_states() )
	ini = produit_cartesien(ini1,ini2)

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
 
def miroir( Aut ) :

	trans = list( Aut.get_transitions() )
	newTrans = []
	for i in range( len(trans) ) :
		newTrans = newTrans + [(trans[i][2], trans[i][1], trans[i][0] )]
	
	a = automaton(
		alphabet = Aut.get_alphabet(), 
		states = Aut.get_states(), 
		initials = Aut.get_final_states(),
		finals = Aut.get_initial_states(),
		transitions = newTrans )
	return a

def determiniser( aut ) :

    ini = aut.get_initial_states()
    states = [ini]
    trans = []
        
    alpha = aut.get_alphabet() - aut.get_epsilons()

    l = [ini]
    while( len(l) != 0 ) :
        for i in alpha :
            tmp = aut.delta(i,l[0])
            if len(tmp) != 0 :
                trans += [ ( l[0] , i , tmp ) ]
                if not tmp in states :
                    states += [tmp]
                    l += [tmp]
        l.pop(0)

    oldFinals = aut.get_final_states()
    fin = []
    for i in states :
        for j in i :
            if j in oldFinals :
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
Fonction interm�diaire qui applique une fois l'algorithme de Moore.
Elle prend en param�tres l'automate concern�, la liste de ses
�tats, son alphabet et une liste de tuples repr�sentant les valeurs
obtenues en appliquant l'algorithme au tour pr�c�dent:
lim = [(groupe de etats[0], groupe par alpha[0], groupe par alpha[1]...),
		(groupe de etats[1], etc...)]
"""
def moore( Aut, etats, alpha, lim ) :
	# On cr�e une nouvelle liste que l'on retournera.
	lmoore = list()

	# On renum�rote les �tats pour donner les nouveaux groupes.
	gpe = -1;
	for i in range(len(lim)) :
		if lim[i] not in lim[:i] :
			gpe += 1
			lmoore.append(tuple((gpe,)))
		else :
			lmoore.append(tuple((lim.index(lim[i]),)))

	# On recr�e les nouveaux groupes d'�tats.
	for i in range(len(lim)) :
		for j in range(len(alpha)) :
			d = list(Aut.delta(alpha[j], [ etats[i] ]))
			lmoore[i] = lmoore[i] + tuple((lmoore[etats.index(d[0])][0],))

	return lmoore

"""
Minimise un automate complet d�terministe gr�ce � l'algorithme de Moore.

"""
def minimiser( Aut ) :

	Aut2 = completer( Aut )
	Aut2 = determiniser( Aut2 )

	etats = list(Aut2.get_states())
	alpha = list(Aut2.get_alphabet())

	# Initialisation. On s�pare les �tats finaux du reste.
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

	# On r�cup�re l'�tat initial.
	init = lm2[etats.index(list(Aut2.get_initial_states())[0])][0]

	# On recherche les nouveaux �tats finaux.
	lm1 = list()
	ets = list()
	for i in range(len(etats)) :
		if Aut2.state_is_final(etats[i]) :
			lm1.append(lm2[i][0])
		ets.append(lm2[i][0])
	# On enl�ve les doublons
	# lm1 la liste des �tats finaux.
	# lm2 la totalit� des �tats et des transitions.
	# ets la liste de tous les �tats.
	lm1 = list(set(lm1))
	lm2 = list(set(lm2))
	ets = list(set(ets))

	amin = automaton(
		alphabet = alpha,
		states = ets,
        initials = [init],
        finals = lm1)

	# On r�cup�re les nouvelles transitions.
	for i in range(len(lm2)) :
		for j in range(len(alpha)) :
			amin.add_transition( (lm2[i][0], alpha[j], lm2[i][j + 1]) )

	return amin



""" 
expression vers automate
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

def generer_epsilon(alpha) :
	i = 0
	while( True ) :
		if not str(i) in alpha :
			return str(i)
		i += 1

def expression_vers_automate( expr ) :
	return operation(expr)


def etoile(expr) :
	aut = operation(expr)
	
	s1 = aut.get_maximal_id() + 1
	s2 = s1 + 1
	s3 = s2 + 1
	s4 = s3 + 1

	alpha = aut.get_alphabet()
	
	if(aut.has_epsilon_characters()) :
		epsilon = list(aut.get_epsilons())[0]
	else :
		epsilon = generer_epsilon(alpha)

	transitions = list( aut.get_transitions() ) 
	transitions += [ (s1 , epsilon , s2) ,
			 (s1 , epsilon , s4) ,
			 (s3 , epsilon , s2) ,
			 (s3 , epsilon , s4) ]
	for i in aut.get_initial_states() :
		transitions += [ (s2 , epsilon , i ) ]
	for i in aut.get_final_states() :
		transitions += [ ( i , epsilon , s3 ) ]

	return automaton(alphabet = alpha,
			 epsilons = [epsilon] ,
			 states = list(aut.get_states()) + [s1 , s2 , s3, s4] ,
			 initials = [s1] ,
			 finals = [s4],
                         transitions = transitions)

def unionEVA(expr1,expr2) :

	#on renomme les �tats au cas o� il y aurait des redondances
	aut1 = operation(expr1)
	aut2 = operation(expr2)

	aut1.renumber_the_states()
	aut2.renumber_the_states()
	x = aut1.get_maximal_id() + 1

	def rajouter(y) :
		return y + x

	aut2.map(rajouter)

	#on g�n�re le nouvel alphabet et on fusionne tous les epsilons en un m�me symbole,
	#permet d'�viter les probl�mes li�s au fait qu'un epsilon de aut1
	#peut �tre dans l'alphabet de aut2, et inversement.
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
	s1 = aut2.get_maximal_id() + 1
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

def concatenation(expr1,expr2) :

	#on renomme les �tats au cas o� il y aurait des redondances
	aut1 = operation(expr1)
	aut2 = operation(expr2)

	aut1.renumber_the_states()
	aut2.renumber_the_states()
	x = aut1.get_maximal_id() + 1

	def rajouter(y) :
		return y + x

	aut2.map(rajouter)

	#on g�n�re le nouvel alphabet et on fusionne tous les epsilons en un m�me symbole,
	#permet d'�viter les probl�mes li�s au fait qu'un epsilon de aut1
	#peut �tre dans l'alphabet de aut2, et inversement.
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
			
	#creation de l'automate concat�nation
	s1 = aut2.get_maximal_id() + 1
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
Retourne une expression avec la concat�nation explicite: '.'
Par exemple, la cha�ne 'a+bc' deviendra 'a+b.c'
"""
def expr_concat ( expr ) :
	expr2 = expr[0]
	for i in range(1,len(expr)):
		# On rajoute entre deux caract�res si celui d'avant est:
		# une parenth�se fermante, une �toile ou une lettre,
		# et celui d'apr�s est une lettre ou une parenth�se ouvrante.
		if expr[i] not in [')', '+', '.', '*'] and expr2[len(expr2) - 1] not in ['(', '+', '.'] :
			expr2 += '.'
		expr2 += expr[i]

	return expr2


"""
Renvoie un bool�en v�rifiant si l'expression pass�e en param�tre est
syntaxiquement correcte ou non. Utile pour l'impl�mentation Python
de l'expression vers la liste pr�fixe.
"""
def est_correcte_expr ( expr ) :
	# 'par' sert � v�rifier que l'expression est bien parenth�s�e.
	# Il est incr�ment� quand on voit '(', et d�cr�ment� pour ')'.
	# Il ne doit jamais �tre inf�rieur � z�ro, et doit �tre �gal
	# � z�ro � la fin du parcours de l'expression.
	par = 0

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

	# Pour le dernier caract�re, on regarde si c'est un caract�re qui peut
	# finir une expression, et si c'est le cas, les caract�res qui
	# peuvent le pr�c�der.
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

	# Expression bien parenth�s�e.
	return par == 0


"""
Renvoie la liste en �criture pr�fixe de l'expression rationnelle donn�e.
L'expression pass�e en param�tre peut contenir des concat�nations implicites
'ab+cd', explicites 'a.b+c.d', ou les deux. Elle peut �galement contenir
des espaces pour aider � la lecture, ils ne seront pas trait�s.
exemple : 'a.b(c + d)* + b.c + a'
"""
def expr_rationnelle_vers_liste_bis ( expr ) :
	# On va utiliser une pile l.
	l = list()

	# On efface les �ventuels espaces inutiles, et on rajoute les 
	# concat�nations explicitement.
	exp = expr.split(" ")
	exp = "".join(exp)
	exp = expr_concat(exp)
	# On v�rifie que l'expression est correcte
	if not est_correcte_expr( exp ) :
		print('erreur de syntaxe')
		return l

	for i in range(len(exp)) :

		# On teste tous les cas possibles dans un pseudo-switch.
		if exp[i] == '*' :
			tmp = l.pop()
			l.append(list(('*', tmp)))

		# On traitera l'entit� � l'int�rieur des parenth�ses une fois
		# la parenth�se fermante correspondante trouv�e.
		elif exp[i] == '(' :
			l.append('(')

		# Si le plus arrive apr�s une autre op�ration, c'est que l'on
		# peut �valuer cette/ces op�rations, l'empiler et continuer.
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

		# M�me principe que pour le '+', en rajoutant une priorit� �
		# la concat�nation.
		elif exp[i] == '.' :
			if len(l) == 1 or l[len(l)-2] in ['(', '+']:
				l.append('.')
			elif l[len(l) - 2] == '.' :
				arg2 = l.pop()
				op = l.pop()
				arg1 = l.pop()
				l.append(list((op, arg1, arg2)))
				l.append('.')

		# On �value l'int�rieur des parenth�ses.
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

	# On s'assure que toutes les expressions ont bien �t� transform�es,
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
