from ___future__ import unicode_literals
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

	def get_zoom_targets():
		"""Where zooming should go, and in what order.
Rules can override this by setting self.zoom_targets, typically to a list of non-immediate children or a list of intermediate children but in a different order."""
		if self.zoom_targets is None: #not overridden by a rule.
			return self.children
		return self.zoom_targets

	def get_xml_fragment():
		"""Returns an XML fragment representing this node  For use with braille providers."""
		return ElementTree.tostring(self.associated_xml)

	def get_template_string(self):
		return self.template_string

def build_tree(root):
	"""Build a tree from an ElementTree element.  Does not normalize."""
	#first, a dict of etree to nodes.
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
