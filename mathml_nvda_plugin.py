path_to_repository = r"c:\projects\in_progress\mathml_accessibility"
import sys
sys.path = [path_to_repository] + sys.path
import nvda_math_provider.py
import globalPluginHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	pass
