import mathml_accessibility
import mathPres

class NaturalMathML(mathPres.MathPresentationProvider):

	def __init__(self):
		pass

	def getSpeechForMathMl(self, mathMl):
		return [mathml_accessibility.translate(mathMl.encode("UTF-8"))]

	def interactWithMathMl(self, mathMl):
		pass

prov = NaturalMathML()
mathPres.registerProvider(prov, speech = True)
