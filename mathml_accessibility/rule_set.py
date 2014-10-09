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
- Succeed.  A successful rule should modify the tree to be spoken, starting with the node it was passed.  See tree.py for a description of nodes and their properties.
"""

#the constant for a failed rule.
#we compare with this using is.
FAILED_RULE = object()

class NoSuchTopicError(Exception):
	"""Thrown when we try to add a rule for an unregistered topic."""
	def __init__(self, topic):
		super(Exception, self).__init__("No Such Topic: {}".format(topic))

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
		self.rules['topic'] = dict()

	def add_rule(self, topic, for_tag, func):
		"""Add a rule which is active when a topic is active, for the MathML tag for_tag, and which is executed by calling func.

Func receives one argument: a node object."""
		if topic not in self.topics:
			raise NoSuchTopicError(topic)
		self.rules[topic][for_tag] = func

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

def add_topic(self, topic):
	global current_rule_set
	if current_rule_set is None:
		raise no_current_rule_set
	current_rule_set.add_topic(topic)

def set_topic_order(order):
	global current_rule_set
	if current_rule_set is None:
		raise no_current_rule_set
	current_rule_set.set_topic_order(order)

def add_rule(topic, tag, func):
	global current_rule_set
	if current_rule_set is None:
		raise no_current_rule_set
	current_rule_set.add_rule(topic, tag, func)

def rule(topic, tag):
	def rule_dec(func):
		add_rule(topic, tag, func)
		return func
	return rule_dec
