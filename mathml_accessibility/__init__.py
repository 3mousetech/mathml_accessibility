from __future__ import unicode_literals
from . import rule_set
from . import normalizer
from . import math_tree
import xml.etree.ElementTree as ElementTree

#simple API: translate directly, no interaction.
def translate(xml_string, locale = 'default', rule_set_name = 'speech'):
	xml_tree = normalizer.normalize_mathml(ElementTree.fromstring(xml_string))
	#wrap this in nodes
	t = math_tree.build_tre(xml_root)
	rule_set.apply_rule_set(t, rule_set_name, locale)
	return t.string
