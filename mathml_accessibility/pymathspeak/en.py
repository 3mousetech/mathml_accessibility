#-*- encoding: utf-8 -*-
#
#MathSpeak localization for English
#
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright 2012-2013 World Light Information Limited and Hong Kong Blind Union.


from . import _core


class MathSpeakNode(_core.MathSpeakNode):

	def __init__(self):
		_core.MathSpeakNode.__init__(self)

	def _naturalNum(self,idx):
		return {
			1:u"one",
			2:u"two",
			3:u"three",
			4:u"four",
			5:u"five",
			6:u"six",
			7:u"seven",
			8:u"eight",
			9:u"nine"}[idx]

	def _ordinalNum(self,idx):
		return {
			1:u"first",
			2:u"second",
			3:u"third",
			4:u"fourth",
			5:u"fifth",
			6:u"sixth",
			7:u"seventh",
			8:u"eighth",
			9:u"ninth",
			10:u"tenth",
			11:u"eleventh",
			12:u"twelfth",
			13:u"thirteenth",
			14:u"fourteenth",
			15:u"fifteenth",
			16:u"sixteenth",
			17:u"seventeenth",
			18:u"eighteenth",
			19:u"nineteenth"}[idx]

	def _mergeNumericFraction(self):
		if not self[0]._isNumber():  return
		if not self[1]._isNumber():  return
		if not 0<int(self[0].text)<10:  return
		if not 1<int(self[1].text)<100:  return
		n=int(self[0].text)
		d=int(self[1].text)
		num=self._naturalNum(n)
		denom=u""
		if   d==2:  denom=u"half"
		elif d==4:  denom=u"quarter"
		elif d<20:  denom=self._ordinalNum(d)
		else:
			denom={
				2:u"twent",3:u"thirt",4:u"fort",5:u"fift",
				6:u"sixt",7:u"sevent",8:u"eight",9:u"ninet"}[d//10]
			if (d%10)==0:  denom+=u"ieth"
			else:          denom+=u"y-"+self._ordinalNum(d%10)
		if n>1:
			# Use plural form of denominator when numerator > 1
			if denom[-1]==u"f":  denom=denom[0:-1]+u"ves"
			else:                denom+=u"s"
		self.text=num+u"-"+denom


class MathSpeak(_core.MathSpeak):

	locale=u"en"

	def __init__(self):
		_core.MathSpeak.__init__(self)

	def _createNode(self):
		return MathSpeakNode()


# vim: set tabstop=4 shiftwidth=4:
