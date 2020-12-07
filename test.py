import antlr4
from antlr4 import StdinStream, ParseTreeWalker

from glangLexer import glangLexer
from glangListener import glangListener
from glangParser import glangParser

if __name__ == '__main__':
	glexer = glangLexer(StdinStream())
	for token in glexer.getAllTokens():
		print('{}: "{}"'.format(glangLexer.symbolicNames[token.type], token.text))
	# stream = antlr4.CommonTokenStream(glexer)

	# parser = glangParser(stream)
	# tree = parser.test()
	# printer = glangListener()
	# walker = ParseTreeWalker()
	# walker.walk(printer, tree)