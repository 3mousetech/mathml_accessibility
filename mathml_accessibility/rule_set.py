"""A RuleSet is a set of math rules organized by category.

The actual rules are in the rulesets submodule.

Usage:
- Call begin_rule_set.
- Add topics with add_topic
- Set a default topic order by using set_topic_order.
- Add rules by importing modules which make use of the rule decorator.
- call end_rule_set.

there is an alternative and less declarative interface; see the RuleSet class.

Rules themselves should do one of two things:
- Fail.  A failed rule does nothing except returnFAILED_RULE (note the caps) from this module.
- Succeed.  A successful rule should return the result of an invocation of rule_return_value.
"""
from __future__ import unicode_literals
from . import data

#the constant for a failed rule.
#we compare with this using is.
FAILED_RULE = object()

class NoSuchTopicError(Exception):
	"""Thrown when we try to add a rule for an unregistered topic."""
	def __init__(self, topic):
		super(Exception, self).__init__("No Such Topic: {}".format(topic))

class NoSuchTagError(Exception):
	def __init__(self, tag):
		super(Exception, self).__init__("No such tag: {}".format(tag))

class NoSuchRuleSetError(Exception):
	def __init__(self, rule_set):
		super(Exception, self).__init__("No such rule set {}".format(rule_set))

class Rule(object):
	"""A rule: holds locale, func associations."""
	def __init__(self):
		self.rule_dict = dict()

	def add(self, locale, func):
		self.rule_dict[locale] = func

	def execute(self, node, locale):
		if locale in self.rule_dict:
			return self.rule_dict[locale](node)
		elif 'default' in self.rule_dict:
			return self.rule_dict['default'](node)
		return FAILED_RULE

class RuleSet(object):
	def __init__(self, name):
		self.name = name
		self.topics = []
		self.topic_order = [] #which order to look at topics for rules.
		self.rules = dict()

	def get_topics():
		return self.topics

	def add_topic(self, topic):
		self.topics.append(topic)
		self.rules[topic] = dict()

	def set_rule(self, topic, for_tag, func, locale = 'default'):
		"""set a rule which is active when a topic is active, for the MathML tag for_tag, and which is executed by calling func.

Func receives one argument: a node object."""
		if for_tag not in data.all_tags:
			raise NoSuchTagError(for_tag)
		if topic not in self.topics:
			raise NoSuchTopicError(topic)
		if for_tag not in self.rules[topic]:
			self.rules[topic][for_tag] = Rule()
		self.rules[topic][for_tag].add(locale, func)

	def get_topic_order(self):
		return self.topic_order

	def set_topic_order(self, new_order):
		for i in new_order:
			if i not in self.topics:
				raise NoSuchTopicError(i)
		self.topic_order = new_order

#the decorator-based API.

current_rule_set = None
rule_sets = dict()
no_current_rule_set = Exception("Error: attempt to add rules with decorator-based API before beginning rule set")

def begin_rule_set(name):
	global current_rule_set
	current_rule_set = RuleSet(name)

def end_rule_set():
	global rule_sets, current_rule_set
	if current_rule_set is None:
		raise no_current_rule_set
	rule_sets[current_rule_set.name] = current_rule_set
	current_rule_set = None

def add_topic(topic):
	global current_rule_set
	if current_rule_set is None:
		raise no_current_rule_set
	current_rule_set.add_topic(topic)

def add_topics(*args):
	for i in args:
		add_topic(i)

def set_topic_order(order):
	global current_rule_set
	if current_rule_set is None:
		raise no_current_rule_set
	current_rule_set.set_topic_order(order)

def set_rule(topic, tag, func, locale = 'default'):
	global current_rule_set
	if current_rule_set is None:
		raise no_current_rule_set
	current_rule_set.set_rule(topic, tag, func, locale)

def rule(topic, tag, locale = 'default'):
	def rule_dec(func):
		set_rule(topic, tag, func, locale)
		return func
	return rule_dec

#the special function that we use for return values:
def rule_return_value(node, template_string, template_string_low_verbocity = None, zoom_targets = None):
	if template_string_low_verbocity is None:
		template_string_low_verbocity = template_string
	if zoom_targets is None:
		zoom_targets = node.get_zoom_targets()
	return {
		'template_string' : template_string,
		'template_string_low_verbocity': template_string_low_verbocity,
		'zoom_targets' : zoom_targets,
	}

def _apply_node(node, rule_set, , locale):
	passed_rule = rule_return_value(node, template_string = "Error: could not translate node")
	candidates = []
	for i in rule_set.get_topic_order():
		if node.tag in rule_set.rules[i]:
			candidates += [(i, rule_set.rules[i][node.tag])]
	for i, rule in candidates:
		result = rule.execute(node)
		if result is not FAILED_RULE:
			passed_rule = result
			break
	#apply passed_rule
	node.zoom_targets = passed_rule['zoom_targets']
	node.template_string = passed_rule['template_string']
	node.template_string_low_verbocity = passed_rule['template_string_low_verbocity']

def apply_rule_set(tree, rule_set_name, locale):
	if rule_set_name not in rule_sets:
		raise NoSuchRuleSetError(rule_set_name)
	rule_set = rule_sets[rule_set_name]
	nodes = [list(tree.iterate())]
	for i in nodes:
		_apply_node(node, rule_set, locale)
	#it's a bredth-first iterator, so reversing it gives us deepest first.
	for i in reversed(nodes):
		i.compute_strings()
