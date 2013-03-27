from expressionRationnelle_lex import *
import ply.yacc as yacc

lex.lex()

precedence = (
	('left' , 'PLUS' ) ,
	('left' , 'POINT') ,
	('left' , 'ETOILE')
	)

def p_expression_etoile(t) :
	'expression : expression ETOILE'
	t[0] = ['*' , t[1]]

def p_expression_plus(t) :
	'expression : expression PLUS expression'
	t[0] = ['+',t[1],t[3]]

def p_expression_concatene(t) :
	'expression : expression POINT expression'
	t[0] = [ '.' , t[1] , t[3] ]

def p_expression_paranthese(t) :
	'expression : PAR_O expression PAR_F'
	t[0] = t[2]

def p_expression_letter(t) :
	'expression : LETTER'
	t[0] = t[1]

def p_error(t) :
	print("Syntax error")