from automaton import *


"""
Complète l'automate donné en lui ajoutant un état puit.
On ne modifie pas l'automate pris en paramètre, on utilise un clone.  
"""
def completer( Aut ):
	a = Aut.clone()
	s = list(a.get_states())
	alpha = list(a.get_alphabet())

	# On parcourt tous les états pour donner un nom correct à l'état puit.
	puit = 0
	while puit in s :
		puit = puit + 1
	a.add_state(puit)
	# On modifie ce booléen si on fait au moins une modification.
	complet = False 

	for i in range(len(alpha)) :
		for j in range(len(s)) :
			if len(a.delta(alpha[i], [s[j]])) == 0 :
				complet = True
				a.add_transition( (j,alpha[i],puit) )

	# Si complet = False, c'est que l'automate est déjà complet, 
	# on enlève l'état puit.
	if not complet :
		a.delete_state(puit)

	return a


"""
Retourne un automate construit 
sur l'union des deux automates passés en paramètres.
"""
def union( Aut1, Aut2 ) :
	# L'union se fait sur deux automates complets.
	a1 = completer( Aut1 )
	a2 = completer( Aut2 )
	alpha1 = list(a1.get_alphabet())
	alpha2 = list(a2.get_alphabet())

	# On recherche l'union des alphabets, stockée dans alpha2.
	for i in range(len(alpha1)) :
		if alpha1[i] not in alpha2 :
			alpha2.append(alpha1[i])

	u = automaton( alphabet = alpha2 )
	return u

def miroir( Aut ) :
	a = automaton(
		alphabet = list(Aut.get_alphabet()), 
		states = list(Aut.get_states()), 
		initials = list(Aut.get_final_states()),
		finals = list(Aut.get_initial_states())
	return a		
