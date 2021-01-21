import os

import sass

if __name__ == '__main__':
	abs_path = os.path.join(os.path.dirname(__file__), 'grapher/css')
	for fn in os.listdir(abs_path):
		if fn.endswith('.scss'):
			contents = sass.compile(filename=os.path.join(abs_path, fn))
			open(os.path.join(abs_path, fn.replace('.scss', '.css')), 'w+').write(contents)
