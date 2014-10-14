from __future__ import unicode_literals
from ... import data
from ...rule_set import set_rule, rule_return_value
from ...pymathspeak import en
import xml.etree.ElementTree as ElementTree

mathspeak = en.MathSpeak()

def pymathspeak_fallback(node):
	fragment = node.get_xml_fragment()
	if node.tag != "math":
		fragment = "<math>" + fragment + "</math>"
	s = mathspeak.translate(fragment)
	return rule_return_value(node, template_string = s)

for i in data.all_tags:
	set_rule("pymathspeak_fallback", i, pymathspeak_fallback)
