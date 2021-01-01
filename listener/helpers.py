class DataPoint:
	def __init__(self, x, y, color=None):
		self.x, self.y, color = x, y, color


class NamedValue:
	def __init__(self, name, value, color=None):
		self.name, self.value, self.color = name, value, color
