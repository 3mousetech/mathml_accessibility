"""This file implements the normalization of MathML.

The normalize_mathml function expects an elementtree root element and normalizes.  The most important components of normalization are removal of namespace and addition of inferred mrow."""

from __future__ import unicode_literals
import xml.etree.ElementTree as ElementTree
import re
from . import data

#these elements wrap their immediate children in mrow elements.
single_argument_elements = set(["msqrt", "mstyle", "merror", "mpadded", "mphantom",

#matches XML namespace.
namespace_re = re.compile(".+:.+")

def _normalize_node(node):
	#handle the single mrow case.
	if node.tag in data.single_argument_elements and (node[0].tag != "mrow" or len(node) != 1):
		old_children = list(node) #get the children in order.
		#We kill the children.  We're holding copies
		while len(node):
			del node[len(node)-1]
		new_mrow = ElementTree.SubElement(node, "mrow")
		#and then add the children back in.
		new_mrow.extend(old_children)
	#otherwise, we need to wrap all children in mrow.
	else:
		for i, child in list(node): #we need to be holding the old list.
			if child.tag == "mrow": #okay, fine, good. Skip it.
				continue
		new_mrow = ElementTree.Element(tag = "mrow")
		del node[i]
		new_mrow.insert(child, 0)
		node.insert(new_mrow, i)

def _remove_namespaces(node):
	nodes = list(node.iter()) #python docs are unclear if we can modify .tag attribute while iterating.
	for n in nodes:
		if namespace_re.match(n.tag) is not None:
			needed = n.tag.split(":")[1] #grab the nonnamespace part.

#The normalizer.
def normalize_mathml(root):
	#simply apply namespace normalization to the root.
	_remove_namespaces(root)
	#can't iterate and modify.
	needs_normalization = list(root.iter())
	for i in needs_normalization:
		_normalize_node(i)
