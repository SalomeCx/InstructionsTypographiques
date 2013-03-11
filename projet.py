from automaton import *

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
		a.delete_state(puit)

	return a

def nouvelles_transitions_IU(etats1,etats2,alpha) :
	trans = []

	for i in range( len(etats1) ) :
		for j in range( len(etats2) ) :
			for k in range( len(alpha) ) :
				l1 = a1.delta(alpha[k],etats1[i])
				l2 = a2.delta(alpha[k],etats2[j])
				for ii in range( len(l1) ) :
					for jj in range( len(l2) ) :
						trans = trans + [( (etats1[i],etats2[j]), alpha[k] , (l1[ii],l2[jj]) )]
	return trans


"""
Retourne un automate construit 
sur l'union des deux automates passés en paramètres.
On considère l'union uniquement sur deux automates comprenant
le même alphabet.
"""
def union( Aut1, Aut2 ) :
	# L'union se fait sur deux automates complets.
	a1 = completer( Aut1 )
	a2 = completer( Aut2 )

	# On récupère les états finaux pour connaître les nouveaux
	# états finaux.
	f1 = list(a1.get_final_states())
	f2 = list(a2.get_final_states())

	# L'état initial.
	ini = tuple((tuple(a1.get_initial_states()), 
		tuple(a2.get_initial_states())))

	alpha = list(a1.get_alphabet())

	u = automaton( 
		alphabet = alpha,
		initials = [ini])

	# On construit la liste des nouveaux états au fur et à mesure.
	etats = list( (ini,) )

	for i in range(len(etats)) :
		for j in range(len(alpha)) :
			etmp = tuple((tuple((a1.delta(alpha[j], etats[i][0]))),
				tuple((a2.delta(alpha[j], etats[i][1])))))
			if etmp not in etats :
				etats.append(etmp)
				etats
				isf = False
				# Pas terrible. A changer. Probablement.
				# Si un état du premier automate est final, l'état
				# obtenu est final.
				for k in range(len(etmp[0])) :
					if etmp[0][k] in f1 :
						u.add_final_state(etmp)
						isf = True
						break
				# Sinon, on cherche dans les états finaux du 
				# second automate.
				if not isf :
					for k in range(len(etmp[1])) :
						if etmp[1][k] in f2 :
							u.add_final_state(etmp)
							isf = True
							break

				# Sinon, c'est que l'état obtenu n'est pas final.
				if not isf :
					u.add_state(etmp)

			u.add_transition( (etats[i], alpha[j], etmp) )

	#u.renumber_the_states()
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

	if alpha != list(a2.get_alphabet()) :
		return None

	etats1 = list( a1.get_states() )
	etats2 = list( a2.get_states() )
	etats = produit_cartesien(etats1,etats2)

	ini1 = list( a1.get_initial_states() )
	ini2 = list( a2.get_initial_states() )
	ini = produit_cartesien(ini1,ini2)

	fin1 = list( a1.get_final_states() )
	fin2 = list( a2.get_final_states() )
	fin = produit_cartesien()

	trans = nouvelles_transitions_IU(etats1,etats2,alpha)

	return automaton(alphabet = alpha, states = etats, initials = ini, finals = fin, transitions = trans)
 
"""
def miroir( Aut ) :
	a = automaton(
		alphabet = list(Aut.get_alphabet()), 
		states = list(Aut.get_states()), 
		initials = list(Aut.get_final_states()),
		finals = list(Aut.get_initial_states())
	return a		
"""
