import argparse
import os

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
		builtins.RESULT_DIR = os.path.dirname(args.infile)
		gparse(file.read())
