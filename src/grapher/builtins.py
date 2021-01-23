import os
import shutil
from operator import itemgetter

from src.visitor import exceptions, types

RESULT_DIR = ''
FUNCTIONS = {}


def builtin_html_generator(func):
	def with_visitor_args(*args, **kwargs):
		visitor = kwargs.pop('visitor')
		visitor.html += func(*args, **kwargs)
	FUNCTIONS[func.__name__] = with_visitor_args


def insert_css(html):
	pre = '<!DOCTYPE html>\n<html>\n<head>'
	abs_path = os.path.join(os.path.dirname(__file__), 'css')
	for fn in os.listdir(abs_path):
		if fn.endswith('.css'):
			shutil.copy(os.path.join(abs_path, fn), os.path.abspath(RESULT_DIR))
			pre += '\n<link rel="stylesheet" href="{}">'.format(fn)
	pre += '\n</head>\n<body>'
	return pre + html + '\n</body>\n</html>'


def random_hex_color():
	return '#3d9970'


# @builtin_html_generator
def render(calling_identifer, data_points, title):
	if not data_points.type == types.LIST:
		raise exceptions.IncorrectType(calling_identifer, expected_types=types.LIST)
	html = '<dl>\n\t<dt>\n\t\t{}\n\t</dt>\n\t'.format(title.value)
	pv = []
	for i, dp in enumerate(data_points.value):
		if dp.type != types.DATA_POINT:
			raise exceptions.IncorrectType(calling_identifer, expected_types=types.DATA_POINT, nth=i)
		pv.append([dp.value.x.value, dp.value.y.value, dp.value.color.value])
	y_range = (min(pv, key=itemgetter(1))[1], max(pv, key=itemgetter(1))[1])
	x_range = (min(pv, key=itemgetter(0))[0], max(pv, key=itemgetter(0))[0])
	for i, v in pv:
		pass
	# TODO


@builtin_html_generator
def pie(calling_identifier, named_values, title):
	if not named_values.type == types.LIST:
		raise exceptions.IncorrectType(calling_identifier, expected_types=types.LIST)
	html = '<dl>\n\t<dt>\n\t\t{}\n\t</dt>\n\t<div class="pie" style="--size: 300;">'.format(title.value)
	pv = []
	for i, nv in enumerate(named_values.value):
		if nv.type != types.NAMED_VALUE:
			raise exceptions.IncorrectType(calling_identifier, expected_types=types.NAMED_VALUE, nth=i)
		pv.append([nv.value.label.value, nv.value.value.value, nv.value.color.value])
	max_val = sum(v[1] for v in pv)
	offset = 0
	for i, v in enumerate(pv):
		v[1] = int(v[1] * 100 / max_val)
		value = v[1] + 1 if i == len(pv) - 1 and v[1]+offset == 99 else v[1]
		if not v[2]:
			v[2] = random_hex_color()
		html += '<div class="pie__segment" style="--offset:{};--value:{};--bg:{};--over50:{}"></div>'.format(
			offset, value, v[2], '1' if value > 50 else '0'
		)
		offset += v[1]
	html += '</div><div class="pie__legend">'
	for v in pv:
		html += '<div class="pie__legend__entry"><div class="pie__legend__entry__percent" style="--bg:{}">{}%</div>' \
				'<div class="pie__legend__entry__desc">{}</div></div>'.format(v[2], v[1], v[0])
	html += '</div></dl>'
	return html


@builtin_html_generator
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
	return html
