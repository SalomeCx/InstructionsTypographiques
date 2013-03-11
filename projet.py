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
def miroir( Aut ) :
	a = automaton(
		alphabet = list(Aut.get_alphabet()), 
		states = list(Aut.get_states()), 
		initials = list(Aut.get_final_states()),
		finals = list(Aut.get_initial_states())
	return a		
"""