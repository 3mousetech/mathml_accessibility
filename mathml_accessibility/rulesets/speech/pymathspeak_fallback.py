from __future__ import unicode_literals
from ... import data
from ...rule_set import set_rule, rule_return_value
from ...pymathspeak import en
import xml.etree.ElementTree as ElementTree

def pymathspeak_fallback(node):
	return rule_return_value(template_string = en.translate(ElementTree.tostring(node.for_xml, encoding="utf8")))

for i in data.all_tags:
	set_rule("pymathspeak_fallback", i, pymathspeak_fallback)
