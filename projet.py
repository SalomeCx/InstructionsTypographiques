from automaton import *


"""
Supprime un état donné d'un automate. Si l'état avait des transitions,
les efface également.
"""
def delete_state( Aut, state ) :
	alpha = list(Aut.get_alphabet())
	s = list(Aut.get_states())
	if state not in s :
		return None
	else :
		s.remove(state)
	
	init = list(Aut.get_initial_states())
	if state in init :
		init.remove(state)

	fin = list(Aut.get_final_states())
	if state in fin :
		fin.remove(state)

	trans = list(Aut.get_transitions())
	for i in range(len(trans)) :
		if trans[i][0] == state or trans[i][2] == state :
			trans.pop([i])

	return automaton(alphabet = alpha,
		states = s,
		initials = init,
		finals = fin,
		transitions = trans)



"""
Complète l'automate donné en lui ajoutant un état puit.
On ne modifie pas l'automate pris en paramètre, on utilise un clone.  
"""
def completer( Aut ):
	a = Aut.get_renumbered_automaton()
	s = list(a.get_states())
	alpha = list(a.get_alphabet())

	# On parcourt tous les états pour donner un nom correct à l'état puit.
	puit = a.get_maximal_id() + 1
	#while puit in s :
	#	puit = puit + 1
	a.add_state(puit)
	# On modifie ce booléen si on fait au moins une modification.
	complet = False 

	for i in range(len(alpha)) :
		for j in range(len(s)) :
			if len(a.delta(alpha[i], [s[j]])) == 0 :
				complet = True
				a.add_transition( (j, alpha[i], puit) )

	# Si complet = False, c'est que l'automate est déjà complet, 
	# on enlève l'état puit.
	if not complet :
		a = delete_state(a, puit)

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
le même alphabet.
"""
def union( Aut1, Aut2 ) :
	alpha = list(Aut1.get_alphabet())

	if alpha != list( Aut2.get_alphabet() ) :
		return None

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
le même alphabet.
"""
def intersection(aut1,aut2) :
	# L'intersection se fait sur deux automates complets.
	a1 = completer( aut1 )
	a2 = completer( aut2 )

	alpha = list(a1.get_alphabet())

	if alpha != list( a2.get_alphabet() ) :
		return None

	etats1 = list( a1.get_states() )
	etats2 = list( a2.get_states() )
	etats = produit_cartesien(etats1,etats2)

	ini1 = list( a1.get_initial_states() )
	ini2 = list( a2.get_initial_states() )
	ini = produit_cartesien(ini1,ini2)

	fin1 = list( a1.get_final_states() )
	fin2 = list( a2.get_final_states() )
	fin = produit_cartesien(fin1,fin2)

	trans = nouvelles_transitions_IU(a1, a2,etats1,etats2,alpha)

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
		alphabet = list(Aut.get_alphabet()), 
		states = list(Aut.get_states()), 
		initials = list(Aut.get_final_states()),
		finals = list(Aut.get_initial_states()),
		transitions = newTrans )
	return a
