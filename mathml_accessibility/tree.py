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
