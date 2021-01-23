import antlr4
from antlr4 import InputStream

from generated.src.glangLexer import glangLexer
from generated.src.glangParser import glangParser
from src.utils import LexerErrorListener, ParserErrorListener
from src.visitor.core import GVisitor


def glex(text, return_lexer=False):
	lexer = glangLexer(InputStream(text))
	lexer.removeErrorListeners()
	lexer._listeners = [LexerErrorListener()]
	if return_lexer:
		return lexer
	return lexer.getAllTokens()


def gparse(text, return_visitor=True):
	lexer = glex(text, return_lexer=True)
	# print_tokens(lexer.getAllTokens())
	stream = antlr4.CommonTokenStream(lexer)
	parser = glangParser(stream)
	parser.removeErrorListeners()
	parser.addErrorListener(ParserErrorListener())
	tree = parser.script()
	visitor = GVisitor()
	visitor.visit(tree)
	if return_visitor:
		return visitor