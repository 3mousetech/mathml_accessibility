from __future__ import unicode_literals
import xml.etree.ElementTree as ElementTree

class MathNode(object):
	"""Backs ont an ElementTree node.  Provides an easier interface, info on where to go for zooming, and node-specific template strings set by the rule functions."""

	def __init__(self, tag, associated_xml, template_string = "MathML Error: No Rule", parent = None, children = ()):
		self.tag = tag
		self.associated_xml = associated_xml
		self.parent = parent
		self.children = list(children)
		self.template_string = template_string
		self.zoom_targets = None

	def compute_strings(self):
		"""Assumes that compute_strings has been called on all children."""
		children_strings = [i.string for i in self.children]
		children_strings_low_verbocity = [i.string_low_verbocity for i in self.children]
		zoom_target_strings = [i.string for i in getattr(self, 'zoom_targets', self.children)]
		zoom_target_low_verbocity_strings = [i.string_low_verbocity for i in getattr(self, 'zoom_targets', self.children)]
		self.string = self.template_string.format(*children_strings, zoom_targets = zoom_target_strings)
		self.string_low_verbocity = self.template_string_low_verbocity.format(*children_strings_low_verbocity, zoom_targets = zoom_target_low_verbocity_strings)

	def get_zoom_targets(self):
		"""Where zooming should go, and in what order.
Rules can override this by setting self.zoom_targets, typically to a list of non-immediate children or a list of intermediate children but in a different order."""
		if self.zoom_targets is None: #not overridden by a rule.
			return self.children
		return self.zoom_targets

	def get_xml_fragment(self):
		"""Returns an XML fragment representing this node  For use with braille providers."""
		return ElementTree.tostring(self.associated_xml, encoding = "utf-8")

	def iterate(self):
		"""Returns a bredth-first iterator starting at this node."""
		yield self
		next = self.children
		new_next = []
		while len(next):
			for i in next:
				yield i
				new_next += i.children
			next = new_next
			new_next = []

def build_tree(root):
	"""Build a tree from an ElementTree element.  Does not normalize."""
	#first, a dict of etree xml to nodes.
	xml_to_nodes = dict()
	for i in root.iter():
		xml_to_nodes[i] = MathNode(tag = i.tag, associated_xml = i)
	#hook up the children.  Order is important here.
	needs_processing = set([root])
	while len(needs_processing):
		processing = needs_processing.pop()
		n = xml_to_nodes[processing]
		xml_children = list(processing)
		children = [xml_to_nodes[i] for i in xml_children]
		for i in children:
			i.parent = n
		n.children = children
		needs_processing.update(xml_children)
	return xml_to_nodes[root]
