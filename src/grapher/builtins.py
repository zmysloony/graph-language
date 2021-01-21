import os
import shutil
from operator import itemgetter

from src.visitor import exceptions, types

RESULT_DIR = ''
FUNCTIONS = {}


def builtin(func):
	FUNCTIONS[func.__name__] = func


def insert_css(html):
	pre = '<!DOCTYPE html>\n<html>\n<head>'
	abs_path = os.path.join(os.path.dirname(__file__), 'css')
	for fn in os.listdir(abs_path):
		if fn.endswith('.css'):
			shutil.copy(os.path.join(abs_path, fn), os.path.abspath(RESULT_DIR))
			pre += '\n<link rel="stylesheet" href="{}">'.format(fn)
	pre += '\n</head>\n<body>'
	return pre + html + '\n</body>\n</html>'


@builtin
def render():
	pass


@builtin
def pie():
	pass


@builtin
def bar(calling_identifier, named_values, title):
	if not named_values.type == types.LIST:
		raise exceptions.IncorrectType(calling_identifier, expected_types=types.LIST)
	html = '<dl>\n\t<dt>\n\t\t{}\n\t</dt>'.format(title.value)
	pv = []
	for i, nv in enumerate(named_values.value):
		if nv.type != types.NAMED_VALUE:
			raise exceptions.IncorrectType(calling_identifier, expected_types=types.NAMED_VALUE, nth=i)
		pv.append([nv.value.label.value, nv.value.value.value, nv.value.color.value])
	max_val = max(pv, key=itemgetter(1))[1]
	for v in pv:
		v[1] = int(v[1] * 1000 / max_val)
		html += '\n\t<dd class="bar__percentage bar__percentage-{}" {}>\n\t\t<span class="bar__text">{}</span>' \
				'\n\t</dd>'.format(v[1], ' style="--bar-color: {}"'.format(v[2] if v[2] else '#3d9970'), v[0])
	html += '\n</dl>'
	html = insert_css(html)
	open(os.path.join(RESULT_DIR, 'result.html'), 'w+').write(html)
