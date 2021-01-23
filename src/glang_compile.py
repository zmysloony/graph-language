import argparse
import os
from sys import exit

from src.grapher import builtins
from src.tools import gparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Glang parser.')
	parser.add_argument('--infile', '-i')
	parser.add_argument('--outdir', '-o')
	args = parser.parse_args()

	if args.infile:
		try:
			file = open(args.infile)
		except IOError:
			print('Input file not accessible.')
			exit(1)
		if args.outdir:
			builtins.RESULT_DIR = os.path.dirname(args.outdir)
		visitor = gparse(file.read())
		visitor.generate_total_html()
