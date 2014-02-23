import ply.lex as lex

tokens = (
	'LETTER' ,
	'PLUS' ,
	'ETOILE' ,
	'PAR_O' ,
	'PAR_F' ,
	'POINT'
	)

t_PLUS = r'\+'
t_ETOILE = r'\*'
t_PAR_O = r'\('
t_PAR_F = r'\)'
t_POINT = r'\.'

def t_LETTER(t) :
	r'[^+*.()]'
	return t

def t_error(t): 
	print("Illegal character '%s'" % t.value[0])