from __future__ import unicode_literals
from ...rule_set import *

begin_rule_set("speech")
add_topics("identifiers", "operators", "algebra", "calculus", "pymathspeak_fallback")
set_topic_order(["calculus", "algebra", "operators", "identifiers", "pymathspeak_fallback"])
from . import pymathspeak_fallback
end_rule_set()
