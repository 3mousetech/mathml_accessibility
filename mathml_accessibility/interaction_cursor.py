class InteractionCursor(object):
	"""All of the functions do exactly what you think.  All of the functions return strings to be spoken. That is all."""

	def __init__(self, root):
		"""Root must be the mathml tag or bad things happen.

More specifically, the root must have been run through the normalizer. The document must look like:
<mathml>
<mrow>
...stuff...
</mrow>
</mathml>
"""
		self.root = root
		self.stack = [root]
		self.siblings = root.get_zoom_targets()
		self.current_position = 0

	def get_current_position(self):
		return self.siblings[self.current_position].string

	def go_left(self):
		if self.current_position == 0:
			return "Cannot go left"
		self.current_position -= 1
		return self.get_current_position()

	def go_right(self):
		if self.current_position+1 == len(self.siblings):
			return "Cannot go right"
		self.current_position += 1
		return self.get_current_position()

	def zoom_in(self):
		_from = self.siblings[self.current_position]
		new_siblings = _from.get_zoom_targets()
		if len(new_siblings) == 0:
			return "Zoomed in all of the way"
		self.siblings = new_siblings
		self.current_position = 0
		self.stack.append(_from) #remember how we got here so that we can zoom out.
		return self.get_current_position()

	def zoom_out(self):
		if len(self.stack) == 1: #the only thing on the stack is the mathml node, no more zooming out.
			return "Zoomed out all of the way"
		#the item on the top of the stack is the item for which we are currently exploring siblings.
		#pop it, recalcculate siblings and position, reannounce.
		self.stack.pop()
		self.siblings = self.stack[-1].get_zoom_targets()
		self.current_position = 0
		return self.get_current_position()
