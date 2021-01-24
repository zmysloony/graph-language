import argparse
import os
from sys import exit

from src.grapher import builtins
from src.tools import gparse
from src.utils import SyntaxException
from src.visitor.exceptions import ParsingException

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Glang parser.')
	parser.add_argument('--infile', '-i', help='Input file.')
	parser.add_argument('--outdir', '-o', help='Output directory.')
	parser.add_argument('--colorseed', '-s', help='Seed for color generation.')
	args = parser.parse_args()

	if args.infile:
		try:
			file = open(args.infile)
		except IOError:
			print('Input file not accessible.')
			exit(1)
		if args.outdir:
			builtins.RESULT_DIR = os.path.dirname(args.outdir)
		if args.colorseed:
			builtins.init_color_seed(args.colorseed)
		else:
			builtins.init_color_seed()
		try:
			visitor = gparse(file.read())
			visitor.generate_total_html()
		except SyntaxException as e:
			print('Syntax error:\n', e)
			exit(1)
		except ParsingException as e:
			print('Runtime exception:\n', e)
			exit(1)
		exit(0)
