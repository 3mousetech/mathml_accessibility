from __future__ import unicode_literals
import mathml_accessibility
import mathPres
import speech

#interaction
class NaturalMathMlInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, cursor, provider = None, mathMl = None):
		super(NaturalMathMlInteraction, self).__init__(provider=provider, mathMl=None)
		self.cursor = cursor

	def reportFocus(self):
		super(NaturalMathMlInteraction, self).reportFocus()
		speech.speak([self.cursor.get_current_position()])

	def script_moveLeft(self, gesture):
		speech.speak([self.cursor.move_left()])

	def script_moveRight(self, gesture):
		speech.speak([self.cursor.move_right()])

	def script_zoomIn(self, gesture):
		speech.speak([self.cursor.zoom_in()])

	def script_zoomOut(self, gesture):
		speech.speak([self.cursor.zoom_out()])

	def script_sayXml(self, gesture):
		speech.speak([self.cursor.get_xml().encode("raw_unicode_escape")])

	__gestures = {
		"kb:rightArrow": "moveRight",
		"kb:leftArrow": "moveLeft",
		"kb:downArrow": "zoomIn",
		"kb:upArrow": "zoomOut",
		"kb:x": "sayXml",
	}

class NaturalMathMlProvider(mathPres.MathPresentationProvider):

	def __init__(self):
		super(NaturalMathMlProvider, self).__init__()

	def getSpeechForMathMl(self, mathMl):
		return [mathml_accessibility.translate(mathMl.encode("UTF-8"))]

	def interactWithMathMl(self, mathMl):
		NaturalMathMlInteraction(cursor = mathml_accessibility.interact(mathMl.encode("UTF-8")), provider = self, mathMl = mathMl).setFocus()

prov = NaturalMathMlProvider()
mathPres.registerProvider(prov, speech = True, interaction = True)
