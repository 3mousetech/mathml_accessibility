from ...rule_set import *

begin_rule_set("en")
add_topics("identifiers", "operators", "algebra", "calculus", "mathspeak_fallback")
set_topic_order(["calculus", "algebra", "operators", "identifiers", "mathspeak_fallback"])
