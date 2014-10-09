#-*- encoding: utf-8 -*-
#
#Implementation of MathSpeak Core Specification Grammer Rules from:
#    http://www.gh-mathspeak.com/examples/grammar-rules/
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright 2012-2013 World Light Information Limited and Hong Kong Blind Union.


from xml.parsers import expat
import re
import sys


# Compatibility fixes for Python 2.x
if sys.version_info[0]<3:  range=xrange


# Verbosity levels
VERB_VERBOSE=0
VERB_BRIEF=1
VERB_SUPERBRIEF=2


# Lookup table for <mathvariant> styles
VARIANT_DICT={
	u"bold":        {None:u"Bold"},
	u"italic":      {None:u"Italic"},
	u"bold-italic": {None:u"BoldItalic"},
	u"fraktur":     {None:u"German"},
	u"bold-fraktur":{None:u"BoldGerman"},
	}


# Lookup table for MathSpeak textual descriptions
LABEL_DICT={
	u"number":     {
		VERB_VERBOSE:u"Number",
		None:        u"Num"},
	u"row":        {None:u"Row"},
	u"column":     {None:u"Column"},
	u"label":      {None:u"Label"},
	u"error":      {None:u"Error"},
	u"capital":    {None:u"Upper"},
	u"capword":    {None:u"UpperWord"},
	u"positive":   {None:u"positive"},
	u"negative":   {None:u"negative"},
	u"start":      {None:u"Start"},
	u"end":        {None:u"End"},
	u"script":     {None:u"Script"},
	u"scriptclose":{
		VERB_VERBOSE:u"Script",
		None:        u""},
	u"scriptend":  {None:u"EndScripts"},
	u"under":      {None:u"Under"},
	u"over":       {None:u"Over"},
	u"above":      {None:u"Above"},
	u"below":      {None:u"Below"},
	u"baseline":   {
		VERB_VERBOSE:u"Baseline",
		None:        u"Base"},
	u"super":      {
		VERB_VERBOSE:u"Super",
		None:        u"Sup"},
	u"sub":        {None:u"Sub"},
	u"string":     {None:u"String"},
	u"blank":	   {None:u"Blank"},
	u"layout":     {None:u"Layout"},
	u"enlarged":   {None:u"Enlarged"},
	u"matrix":     {None:u"Matrix"},
	u"determinant":{None:u"Determinant"},
	u"binomial":   {None:u"BinomialOrMatrix"},
	u"choose":     {None:u"Choose"},
	u"absolute":   {None:u"AbsoluteValue"},
	u"modifying":  {
		VERB_VERBOSE:u"Modifying",
		None:        u"Mod"},
	u"each":       {None:u"Each"},
	u"with":       {None:u"with"},
	u"by":         {None:u"by"},
	u"point":      {None:u"point"},
	u"and":        {None:u"and"},
	u"..":         {None:u"two-dots"},
	u"once":       {None:u"Once"},
	u"twice":      {None:u"Twice"},
	u"fracnest":   {None:u"Nest"},
	u"fracover":   {None:u"Over"},
	u"frac":   {
		VERB_SUPERBRIEF:u"Frac",
		VERB_BRIEF:     u"Frac",
		None:           u"Fraction"},
	u"rootnest":   {
		VERB_SUPERBRIEF:u"Nest",
		VERB_BRIEF:     u"Nest",
		None:           u"Nested"},
	u"rootindex":  {
		VERB_SUPERBRIEF:u"Index",
		None:           u"RootIndex"},
	u"rootstart":  {
		VERB_SUPERBRIEF:u"Root",
		None:           u"StartRoot"},
	u"rootend":    {None:u"EndRoot"},
	u"squared":    {None:u"squared"},
	u"cubed":      {None:u"cubed"},
	u"cancel":     {None:u"CrossOut"},
	u"cancelwith": {None:u"With"},
	u"set":        {None:u"Set"},
	}


# Lookup table for <mi> identifiers
IDENTIFIER_DICT={
	u"\u0391":{None:u"Alpha"},
	u"\u0392":{None:u"Beta"},
	u"\u0393":{None:u"Gamma"},
	u"\u0394":{None:u"Delta"},
	u"\u0395":{None:u"Epsilon"},
	u"\u0396":{None:u"Zeta"},
	u"\u0397":{None:u"Eta"},
	u"\u0398":{None:u"Theta"},
	u"\u0399":{None:u"Iota"},
	u"\u039a":{None:u"Kappa"},
	u"\u039b":{None:u"Lambda"},
	u"\u039c":{None:u"Mu"},
	u"\u039d":{None:u"Nu"},
	u"\u039e":{None:u"Xi"},
	u"\u039f":{None:u"Omicron"},
	u"\u03a0":{None:u"Pi"},
	u"\u03a1":{None:u"Rho"},
	u"\u03a3":{None:u"Sigma"},
	u"\u03a4":{None:u"Tau"},
	u"\u03a5":{None:u"Upsilon"},
	u"\u03a6":{None:u"Phi"},
	u"\u03a7":{None:u"Chi"},
	u"\u03a8":{None:u"Psi"},
	u"\u03a9":{None:u"Omega"},
	u"\u03b1":{None:u"alpha"},
	u"\u03b2":{None:u"beta"},
	u"\u03b3":{None:u"gamma"},
	u"\u03b4":{None:u"delta"},
	u"\u03b5":{None:u"epsilon"},
	u"\u03b6":{None:u"zeta"},
	u"\u03b7":{None:u"eta"},
	u"\u03b8":{None:u"theta"},
	u"\u03b9":{None:u"iota"},
	u"\u03ba":{None:u"kappa"},
	u"\u03bb":{None:u"lambda"},
	u"\u03bc":{None:u"mu"},
	u"\u03bd":{None:u"nu"},
	u"\u03be":{None:u"xi"},
	u"\u03bf":{None:u"omicron"},
	u"\u03c0":{None:u"pi"},
	u"\u03c1":{None:u"rho"},
	u"\u03c2":{None:u"final-sigma"},
	u"\u03c3":{None:u"sigma"},
	u"\u03c4":{None:u"tau"},
	u"\u03c5":{None:u"upsilon"},
	u"\u03c6":{None:u"phi"},
	u"\u03c7":{None:u"chi"},
	u"\u03c8":{None:u"psi"},
	u"\u03c9":{None:u"omega"},
	u"\u03d0":{None:u"beta-symbol"},
	u"\u03d1":{None:u"theta-symbol"},
	u"\u03d2":{None:u"hooked-upsilon"},
	u"\u03d5":{None:u"phi-symbol"},
	u"\u03d6":{None:u"pi-symbol"},
	u"\u03d7":{None:u"kai"},
	u"\u03da":{None:u"Stigma"},
	u"\u03db":{None:u"stigma"},
	u"\u03dc":{None:u"Digamma"},
	u"\u03dd":{None:u"digamma"},
	u"\u03de":{None:u"Koppa"},
	u"\u03df":{None:u"koppa"},
	u"\u03e0":{None:u"Sampi"},
	u"\u03e1":{None:u"sampi"},
	u"\u03f0":{None:u"kappa-symbol"},
	u"\u03f1":{None:u"rho-symbol"},
	u"\u03f2":{None:u"lunate-sigma"},
	u"\u03f3":{None:u"yot"},
	u"\u03f4":{None:u"Theta-symbol"},
	u"\u03f5":{None:u"lunate-epsilon"},
	u"\u03f6":{None:u"reversed-lunate-epsilon"},
	u"\u03f7":{None:u"Sho"},
	u"\u03f8":{None:u"sho"},
	u"\u03f9":{None:u"Lunate-sigma"},
	u"\u03fa":{None:u"San"},
	u"\u03fb":{None:u"san"},
	u"\u03fc":{None:u"stroked-rho"},
	u"\u03fd":{None:u"Reversed-lunate-sigma"},
	u"\u03fe":{None:u"Dotted-lunate-sigma"},
	u"\u03ff":{None:u"Reversed-dotted-lunate-sigma"},
	u"\u221e":{None:u"infinity"},
	u"lim":{None:u"limit"},
	u"ln":{
		VERB_VERBOSE:u"natural-log",
		None:        u"log-e"},
	u"sin":{None:u"sine"},
	u"cos":{None:u"cosine"},
	u"tan":{None:u"tangent"},
	u"cot":{None:u"cotangent"},
	u"sec":{None:u"secant"},
	u"csc":{None:u"cosecant"},
	u"asin":{None:u"arc-sine"},
	u"acos":{None:u"arc-cosine"},
	u"atan":{None:u"arc-tangent"},
	u"acot":{None:u"arc-cotangent"},
	u"asec":{None:u"arc-secant"},
	u"acsc":{None:u"arc-cosecant"},
	u"arcsin":{None:u"arc-sine"},
	u"arccos":{None:u"arc-cosine"},
	u"arctan":{None:u"arc-tangent"},
	u"arccot":{None:u"arc-cotangent"},
	u"arcsec":{None:u"arc-secant"},
	u"arccsc":{None:u"arc-cosecant"},
	}


# Lookup table for <mo> operators
OPERATOR_DICT={
	u"=":{None:u"equals"},
	u",":{None:u"comma"},
	u".":{None:u"period"},
	u":":{None:u"colon"},
	u";":{None:u"semicolon"},
	u"+":{None:u"plus"},
	u"-":{None:u"minus"},
	u"#":{
		VERB_VERBOSE:u"number-sign",
		None:        u"num-sign"},
	u"$":{None:u"dollar-sign"},
	u"<":{None:u"less-than"},
	u">":{None:u"greater-than"},
	u"~":{None:u"tilde"},
	u"^":{None:u"circumflex-accent"},
	u"_":{None:u"low-line"},
	u"|":{None:u"vertical-line"},
	u"{":{
		VERB_SUPERBRIEF:u"L curly-brace",
		None:           u"left-curly-brace"},
	u"}":{
		VERB_SUPERBRIEF:u"R curly-brace",
		None:           u"right-curly-brace"},
	u"[":{
		VERB_SUPERBRIEF:u"L brack",
		VERB_BRIEF:     u"left-brack",
		None:           u"left-bracket"},
	u"]":{
		VERB_SUPERBRIEF:u"R brack",
		VERB_BRIEF:     u"right-brack",
		None:           u"right-bracket"},
	u"(":{
		VERB_SUPERBRIEF:u"L p'ren",
		VERB_BRIEF:     u"left-p'ren",
		None:           u"left-parenthesis"},
	u")":{
		VERB_SUPERBRIEF:u"R p'ren",
		VERB_BRIEF:     u"right-p'ren",
		None:           u"right-parenthesis"},
	u"\u00af":{None:u"bar"},
	u"\u00b1":{None:u"plus-or-minus"},
	u"\u00b7":{None:u"dot"},
	u"\u00d7":{None:u"times"},
	u"\u00f7":{None:u"divided-by"},
	u"\u02d9":{None:u"dot"},
	u"\u2016":{None:u"double-vertical-lines"},
	u"\u2018":{None:u"open-single-quote"},
	u"\u2019":{None:u"close-single-quote"},
	u"\u201c":{None:u"open-double-quote"},
	u"\u201d":{None:u"close-double-quote"},
	u"\u2026":{None:u"ellipsis"},
	u"\u2032":{None:u"prime"},
	u"\u2033":{None:u"double-prime"},
	u"\u2034":{None:u"triple-prime"},
	u"\u2038":{None:u"caret"},
	u"\u2044":{None:u"division-slash"},
	u"\u2061":{None:u""},
	u"\u2062":{None:u"times"},
	u"\u2107":{None:u"euler-constant"},
	u"\u210e":{None:u"planck-constant"},
	u"\u210f":{None:u"reduced-planck-constant"},
	u"\u2135":{None:u"alef-infinity"},
	u"\u2190":{
		VERB_SUPERBRIEF:u"L arrow",
		None:           u"left-arrow"},
	u"\u2191":{
		VERB_SUPERBRIEF:u"U arrow",
		None:           u"up-arrow"},
	u"\u2192":{
		VERB_SUPERBRIEF:u"R arrow",
		None:           u"right-arrow"},
	u"\u2193":{
		VERB_SUPERBRIEF:u"D arrow",
		None:           u"down-arrow"},
	u"\u2200":{None:u"for-all"},
	u"\u2201":{None:u"compliment"},
	u"\u2202":{
		VERB_SUPERBRIEF:u"partial-d",
		VERB_BRIEF:     u"partial-diff",
		None:           u"partial-differential"},
	u"\u2203":{None:u"there-exists"},
	u"\u2204":{None:u"there-does-not-exists"},
	u"\u2206":{None:u"increment"},
	u"\u2207":{None:u"nabla"},
	u"\u2208":{None:u"element-of"},
	u"\u2209":{None:u"not-element-of"},
	u"\u220a":{None:u"element-of"},
	u"\u220b":{None:u"contains-member"},
	u"\u220c":{None:u"does-not-contain-member"},
	u"\u220d":{None:u"contains-member"},
	u"\u220e":{None:u"end-of-proof"},
	u"\u220f":{None:u"n-ary-product"},
	u"\u2210":{None:u"n-ary-coproduct"},
	u"\u2211":{None:u"sigma-summation"},
	u"\u2212":{None:u"minus"},
	u"\u2213":{None:u"minus-or-plus"},
	u"\u2214":{None:u"dot-plus"},
	u"\u2215":{None:u"division-slash"},
	u"\u2216":{None:u"set-minus"},
	u"\u2217":{None:u"asterisk"},
	u"\u2218":{None:u"ring"},
	u"\u2219":{None:u"bullet"},
	u"\u221a":{None:u"square-root"},
	u"\u221b":{None:u"cube-root"},
	u"\u221c":{None:u"fourth-root"},
	u"\u221d":{None:u"proportional-to"},
	u"\u221f":{None:u"right-angle"},
	u"\u2220":{None:u"angle"},
	u"\u2221":{None:u"measured-angle"},
	u"\u2222":{None:u"spherical-angle"},
	u"\u2223":{None:u"divides"},
	u"\u2224":{None:u"not-divides"},
	u"\u2225":{None:u"parallel-to"},
	u"\u2226":{None:u"not-parallel-to"},
	u"\u2227":{None:u"logical-and"},
	u"\u2228":{None:u"logical-or"},
	u"\u2229":{None:u"intersect"},
	u"\u222a":{None:u"union"},
	u"\u222b":{None:u"integral"},
	u"\u222c":{None:u"double-integral"},
	u"\u222d":{None:u"triple-integral"},
	u"\u222e":{None:u"contour-integral"},
	u"\u222f":{None:u"surface-integral"},
	u"\u2230":{None:u"volume-integral"},
	u"\u2231":{
		VERB_SUPERBRIEF:u"CW Integral",
		None:           u"clockwise-integral"},
	u"\u2232":{
		VERB_SUPERBRIEF:u"CW contour-integral",
		None:           u"clockwise-contour-integral"},
	u"\u2233":{
		VERB_SUPERBRIEF:u"CCW contour-integral",
		None:           u"counterclockwise-contour-integral"},
	u"\u2234":{None:u"therefore"},
	u"\u2235":{None:u"because"},
	u"\u2236":{None:u"ratio"},
	u"\u2237":{None:u"proportional-to"},
	u"\u2238":{None:u"dot-minus"},
	u"\u2239":{None:u"excess"},
	u"\u223a":{None:u"geometrically-proportional-to"},
	u"\u223b":{None:u"homothetic-to"},
	u"\u223c":{None:u"tilde"},
	u"\u223d":{None:u"reversed-tilde"},
	u"\u223e":{None:u"inverted-lazy-s"},
	u"\u223f":{None:u"sine-wave"},
	u"\u2241":{None:u"not-tilde"},
	u"\u2242":{None:u"minus-tilde"},
	u"\u2243":{None:u"asymptotically-equals"},
	u"\u2244":{None:u"not-asymptotically-equals"},
	u"\u2245":{
		VERB_SUPERBRIEF:u"approx-equals",
		None:           u"approximately-equals"},
	u"\u2246":{
		VERB_SUPERBRIEF:u"approx-but-not-equals",
		None:           u"approximately-but-not-actually-equals"},
	u"\u2247":{
		VERB_SUPERBRIEF:u"neither-approx-nor-equals",
		None:           u"neither-approximately-nor-actually-equals"},
	u"\u2248":{None:u"almost-equals"},
	u"\u2249":{None:u"not-almost-equals"},
	u"\u224a":{None:u"almost-equals-or-equals"},
	u"\u224b":{None:u"triple-tilde"},
	u"\u224c":{None:u"all-equals"},
	u"\u224d":{
		VERB_SUPERBRIEF:u"equiv-to",
		None:           u"equivalent-to"},
	u"\u224e":{
		VERB_SUPERBRIEF:u"geom-equiv-to",
		None:           u"geometrically-equivalent-to"},
	u"\u224f":{None:u"difference-between"},
	u"\u2250":{
		VERB_SUPERBRIEF:u"approaches",
		None:           u"approaches-the-limit"},
	u"\u2251":{
		VERB_SUPERBRIEF:u"geom-equals",
		None:           u"geometrically-equals"},
	u"\u2252":{
		VERB_SUPERBRIEF:u"approx-equals-or-image-of",
		None:           u"approximately-equals-or-image-of"},
	u"\u2253":{
		VERB_SUPERBRIEF:u"image-of-or-approx-equals",
		None:           u"image-of-or-approximately-equals"},
	u"\u2254":{None:u"colon-equals"},
	u"\u2255":{None:u"equals-colon"},
	u"\u2257":{None:u"ring-in-equal-to"},
	u"\u2258":{None:u"corresponds-to"},
	u"\u2259":{None:u"estimates"},
	u"\u225a":{None:u"equiangular-to"},
	u"\u225c":{None:u"delta-equals"},
	u"\u225d":{
		VERB_SUPERBRIEF:u"equals-by-def",
		None:           u"equals-by-definition"},
	u"\u225e":{None:u"measured-by"},
	u"\u225f":{None:u"questioned-equals"},
	u"\u2260":{None:u"not-equals"},
	u"\u2261":{None:u"identical-to"},
	u"\u2262":{None:u"not-identical-to"},
	u"\u2263":{None:u"strictly-equivalent-to"},
	u"\u2264":{None:u"less-than-or-equals"},
	u"\u2265":{None:u"greater-than-or-equals"},
	u"\u2266":{None:u"less-than-over-equal-to"},
	u"\u2267":{None:u"greater-than-over-equal-to"},
	u"\u2268":{None:u"less-than-but-not-equals"},
	u"\u2269":{None:u"greater-than-but-not-equals"},
	u"\u226a":{None:u"much-less-than"},
	u"\u226b":{None:u"much-greater-than"},
	u"\u226c":{None:u"betweens"},
	u"\u226d":{None:u"not-equivalent-to"},
	u"\u226e":{None:u"not-less-than"},
	u"\u226f":{None:u"not-greater-than"},
	u"\u2270":{None:u"neither-less-than-or-equals"},
	u"\u2271":{None:u"neither-greater-than-or-equals"},
	u"\u2272":{None:u"less-than-or-equivalent-to"},
	u"\u2273":{None:u"greater-than-or-equivalent-to"},
	u"\u2274":{None:u"neither-less-than-nor-equivalent-to"},
	u"\u2275":{None:u"neither-greater-than-nor-equivalent-to"},
	u"\u2276":{None:u"less-than-or-greater-than"},
	u"\u2277":{None:u"greater-than-or-less-than"},
	u"\u2278":{None:u"neither-less-than-nor-greater-than"},
	u"\u2279":{None:u"neither-greater-than-nor-less-than"},
	u"\u227a":{None:u"precedes"},
	u"\u227b":{None:u"succeeds"},
	u"\u227c":{None:u"precedes-or-equals"},
	u"\u227d":{None:u"succeeds-or-equals"},
	u"\u227e":{None:u"precedes-or-equivalent-to"},
	u"\u227f":{None:u"succeeds-or-equivalent-to"},
	u"\u2282":{None:u"subset-of"},
	u"\u2283":{None:u"superset-of"},
	u"\u2284":{None:u"not-subset-of"},
	u"\u2285":{None:u"not-superset-of"},
	u"\u2286":{None:u"subset-of-or-equals"},
	u"\u2287":{None:u"superset-of-or-equals"},
	u"\u2288":{None:u"neither-subset-nor-equals"},
	u"\u2289":{None:u"neither-superset-nor-equals"},
	u"\u228a":{None:u"subset-of-but-not-equals"},
	u"\u228b":{None:u"superset-of-but-not-equals"},
	u"\u228c":{None:u"multiset"},
	u"\u228d":{None:u"multiset-multiply"},
	u"\u228e":{None:u"multiset-union"},
	u"\u228f":{None:u"square-image-of"},
	u"\u2290":{None:u"square-original-of"},
	u"\u2291":{None:u"square-image-of-or-equals"},
	u"\u2292":{None:u"square-original-of-or-equals"},
	u"\u2293":{None:u"square-cap"},
	u"\u2294":{None:u"square-cup"},
	u"\u229a":{None:u"circled-ring"},
	u"\u229b":{None:u"circled-asterisk"},
	u"\u229c":{None:u"circled-equals"},
	u"\u229d":{None:u"circled-dash"},
	u"\u22a2":{
		VERB_SUPERBRIEF:u"R tack",
		None:           u"right-tack"},
	u"\u22a3":{
		VERB_SUPERBRIEF:u"L tack",
		None:           u"left-tack"},
	u"\u22a4":{
		VERB_SUPERBRIEF:u"D tack",
		None:           u"down-tack"},
	u"\u22a5":{
		VERB_SUPERBRIEF:u"U tack",
		None:           u"up-tack"},
	u"\u22a6":{None:u"asserts"},
	u"\u22a7":{None:u"models"},
	u"\u22a8":{None:u"is-true"},
	u"\u22a9":{None:u"forces"},
	u"\u22aa":{None:u"triple-vertical-bar-right-turnstile"},
	u"\u22ab":{None:u"double-vertical-bar-right-turnstile"},
	u"\u22ac":{None:u"not-proves"},
	u"\u22ad":{None:u"not-true"},
	u"\u22ae":{None:u"not-forces"},
	u"\u22b0":{None:u"precedes-under-relation"},
	u"\u22b1":{None:u"succeeds-under-relation"},
	u"\u22b2":{None:u"normal-subgroup-of"},
	u"\u22b3":{None:u"contains-normal-subgroup"},
	u"\u22b4":{None:u"normal-subgroup-of-or-equals"},
	u"\u22b5":{None:u"contains-normal-subgroup-or-equals"},
	u"\u22b6":{None:u"original-of"},
	u"\u22b7":{None:u"image-of"},
	u"\u22b9":{None:u"hermitian-conjugate-matrix"},
	u"\u22ba":{None:u"intercalate"},
	u"\u22bb":{None:u"logical x-or"},
	u"\u22bc":{None:u"logical nand"},
	u"\u22bd":{None:u"logical nor"},
	u"\u22be":{None:u"right-angle-with-arc"},
	u"\u22bf":{None:u"right-triangle"},
	u"\u22c4":{None:u"diamond"},
	u"\u22c6":{None:u"star"},
	u"\u22c7":{None:u"divide-times"},
	u"\u22c8":{None:u"bow-tie"},
	u"\u22c9":{
		VERB_SUPERBRIEF:u"L norm-factor-semidirect-prod",
		None:           u"left-normal-factor-semidirect-product"},
	u"\u22ca":{
		VERB_SUPERBRIEF:u"R norm-factor-semidirect-prod",
		None:           u"right-normal-factor-semidirect-product"},
	u"\u22cb":{
		VERB_SUPERBRIEF:u"L semidirect-prod",
		None:           u"left-semidirect-product"},
	u"\u22cc":{
		VERB_SUPERBRIEF:u"R semidirect-prod",
		None:           u"right-semidirect-product"},
	u"\u22cd":{None:u"reversed-tilde-equals"},
	u"\u22ce":{None:u"curly-logical-or"},
	u"\u22cf":{None:u"curly-logical-and"},
	u"\u22d0":{None:u"double-subset"},
	u"\u22d1":{None:u"double-superset"},
	u"\u22d2":{None:u"double-intersection"},
	u"\u22d3":{None:u"double-union"},
	u"\u22d4":{None:u"pitch-fork"},
	u"\u22d5":{None:u"equals-and-parallel-to"},
	u"\u22d6":{None:u"dotted-less-than"},
	u"\u22d7":{None:u"dotted-greater-than"},
	u"\u22d8":{None:u"very-much-less-than"},
	u"\u22d9":{None:u"very-much-greater-than"},
	u"\u22da":{None:u"less-than-equals-or-greater-than"},
	u"\u22db":{None:u"greater-than-equals-or-less-than"},
	u"\u22dc":{None:u"equals-or-less-than"},
	u"\u22dd":{None:u"equals-or-greater-than"},
	u"\u22de":{None:u"equals-or-precedes"},
	u"\u22df":{None:u"equals-or-succeeds"},
	u"\u22e0":{None:u"not-precedes-or-equals"},
	u"\u22e1":{None:u"not-succeeds-or-equals"},
	u"\u22e2":{None:u"not-square-image-of-or-equals"},
	u"\u22e3":{None:u"not-square-original-of-or-equals"},
	u"\u22e4":{None:u"square-image-of-or-not-equals"},
	u"\u22e5":{None:u"square-original-of-or-not-equals"},
	u"\u22e6":{None:u"less-than-but-not-equivalent-to"},
	u"\u22e7":{None:u"greater-than-but-not-equivalent-to"},
	u"\u22e8":{None:u"precedes-but-not-equivalent-to"},
	u"\u22e9":{None:u"succeeds-but-not-equivalent-to"},
	u"\u22ea":{None:u"not-normal-subgroup-of"},
	u"\u22eb":{None:u"not-contains-normal-subgroup"},
	u"\u22ec":{None:u"neither-normal-subgroup-of-nor-equals"},
	u"\u22ed":{None:u"neither-contains-normal-subgroup-nor-equals"},
	u"\u22ee":{None:u"vertical-ellipsis"},
	u"\u22ef":{None:u"ellipsis"},
	u"\u22f0":{
		VERB_SUPERBRIEF:u"U diag-ellipsis",
		None:           u"up-diagonal-ellipsis"},
	u"\u22f1":{
		VERB_SUPERBRIEF:u"D diag-ellipsis",
		None:           u"down-diagonal-ellipsis"},
	u"\u22f2":{None:u"element-of-with-long-horizontal-stroke"},
	u"\u22f3":{None:u"element-of-with-vertical-bar-at-end-of-horizontal-stroke"},
	u"\u22f4":{None:u"element-of-with-vertical-bar-at-end-of-horizontal-stroke"},
	u"\u22f5":{None:u"element-of-with-dot-above"},
	u"\u22f6":{None:u"element-of-with-over-bar"},
	u"\u22f7":{None:u"element-of-with-over-bar"},
	u"\u22f8":{None:u"element-of-with-under-bar"},
	u"\u22f9":{None:u"element-of-with-two-horizontal-strokes"},
	u"\u22fa":{None:u"contains-with-long-horizontal-stroke"},
	u"\u22fb":{None:u"contains-with-vertical-bar-at-end-of-horizontal-stroke"},
	u"\u22fc":{None:u"contains-with-vertical-bar-at-end-of-horizontal-stroke"},
	u"\u22fd":{None:u"contains-with-over-bar"},
	u"\u22fe":{None:u"contains-with-over-bar"},
	u"\u22ff":{None:u"bag-member"},
	u"\u2308":{
		VERB_SUPERBRIEF:u"L ceiling",
		None:           u"left-ceiling"},
	u"\u2309":{
		VERB_SUPERBRIEF:u"R ceiling",
		None:           u"right-ceiling"},
	u"\u230a":{
		VERB_SUPERBRIEF:u"L floor",
		None:           u"left-floor"},
	u"\u230b":{
		VERB_SUPERBRIEF:u"R floor",
		None:           u"right-floor"},
	u"\u25a0":{None:u"black-square"},
	u"\u25a1":{None:u"white-square"},
	u"\u25aa":{None:u"small-black-square"},
	u"\u25ab":{None:u"small-white-square"},
	u"\u25ac":{
		VERB_SUPERBRIEF:u"black-rect",
		None:           u"black-rectangle"},
	u"\u25ad":{
		VERB_SUPERBRIEF:u"white-rect",
		None:           u"white-rectangle"},
	u"\u25ae":{
		VERB_SUPERBRIEF:u"black-vert-rect",
		None:           u"black-vertical-rectangle"},
	u"\u25af":{
		VERB_SUPERBRIEF:u"white-vert-rect",
		None:           u"white-vertical-rectangle"},
	u"\u25b0":{None:u"black-parallelogram"},
	u"\u25b1":{None:u"white-parallelogram"},
	u"\u25b2":{None:u"black-point-up-triangle"},
	u"\u25b3":{None:u"white-point-up-triangle"},
	u"\u25b4":{None:u"small-black-point-up-triangle"},
	u"\u25b5":{None:u"small-white-point-up-triangle"},
	u"\u25b6":{None:u"black-point-right-triangle"},
	u"\u25b7":{None:u"white-point-right-triangle"},
	u"\u25b8":{None:u"small-black-point-right-triangle"},
	u"\u25b9":{None:u"small-white-point-right-triangle"},
	u"\u25bc":{None:u"black-point-down-triangle"},
	u"\u25bd":{None:u"white-point-down-triangle"},
	u"\u25be":{None:u"small-black-point-down-triangle"},
	u"\u25bf":{None:u"small-white-point-down-triangle"},
	u"\u25c0":{None:u"black-point-left-triangle"},
	u"\u25c1":{None:u"white-point-left-triangle"},
	u"\u25c2":{None:u"small-black-point-left-triangle"},
	u"\u25c3":{None:u"small-white-point-left-triangle"},
	u"\u25c4":{None:u"black-point-left-triangle"},
	u"\u25c5":{None:u"white-point-left-triangle"},
	u"\u25c6":{None:u"black-diamond"},
	u"\u25c7":{None:u"white-diamond"},
	u"\u25c8":{None:u"white-diamond-containing-black-diamond"},
	u"\u25c9":{None:u"fisheye"},
	u"\u25cc":{None:u"dotted-circle"},
	u"\u25cd":{None:u"circle-with-vertical-fill"},
	u"\u25ce":{None:u"bullseye"},
	u"\u25cf":{None:u"black-circle"},
	u"\u25d6":{None:u"left-half-black-circle"},
	u"\u25d7":{None:u"right-half-black-circle"},
	u"\u25e6":{None:u"white-bullet"},
	u"\u2758":{None:u"vertical-bar"},
	u"\u2772":{
		VERB_SUPERBRIEF:u"L shell-brack",
		None:           u"left-shell-bracket"},
	u"\u2773":{
		VERB_SUPERBRIEF:u"R shell-brack",
		None:           u"right-shell-bracket"},
	u"\u27e6":{
		VERB_SUPERBRIEF:u"L bag-brack",
		VERB_BRIEF:     u"left-bag-brack",
		None:           u"left-bag-bracket"},
	u"\u27e7":{
		VERB_SUPERBRIEF:u"R bag-brack",
		VERB_BRIEF:     u"right-bag-brack",
		None:           u"right-bag-bracket"},
	u"\u27e8":{
		VERB_SUPERBRIEF:u"L angle-brack",
		VERB_BRIEF:     u"left-angle-brack",
		None:           u"left-angle-bracket"},
	u"\u27e9":{
		VERB_SUPERBRIEF:u"R angle-brack",
		VERB_BRIEF:     u"right-angle-brack",
		None:           u"right-angle-bracket"},
	u"\u27ea":{
		VERB_SUPERBRIEF:u"L double-angle-brack",
		VERB_BRIEF:     u"left-double-angle-brack",
		None:           u"left-double-angle-bracket"},
	u"\u27eb":{
		VERB_SUPERBRIEF:u"R double-angle-brack",
		VERB_BRIEF:     u"right-double-angle-brack",
		None:           u"right-double-angle-bracket"},
	u"\u27ec":{
		VERB_SUPERBRIEF:u"L white-shell-brack",
		None:           u"left-white-shell-bracket"},
	u"\u27ed":{
		VERB_SUPERBRIEF:u"R white-shell-brack",
		None:           u"right-white-shell-bracket"},
	u"\u27ee":{
		VERB_SUPERBRIEF:u"L flat-p'ren",
		VERB_BRIEF:     u"left-flat-p'ren",
		None:           u"left-flat-parenthesis"},
	u"\u27ef":{
		VERB_SUPERBRIEF:u"R flat-p'ren",
		VERB_BRIEF:     u"right-flat-p'ren",
		None:           u"right-flat-parenthesis"},
	u"\u2980":{None:u"triple-vertical-lines"},
	u"\u2981":{None:u"spot"},
	u"\u2982":{None:u"type-colon"},
	u"\u2983":{
		VERB_SUPERBRIEF:u"L white-curly-brace",
		None:           u"left-white-curly-brace"},
	u"\u2984":{
		VERB_SUPERBRIEF:u"R white-curly-brace",
		None:           u"right-white-curly-brace"},
	u"\u2985":{
		VERB_SUPERBRIEF:u"L white-p'ren",
		VERB_BRIEF:     u"left-white-p'ren",
		None:           u"left-white-parenthesis"},
	u"\u2986":{
		VERB_SUPERBRIEF:u"R white-p'ren",
		VERB_BRIEF:     u"right-white-p'ren",
		None:           u"right-white-parenthesis"},
	u"\u2987":{
		VERB_SUPERBRIEF:u"L image-brack",
		VERB_BRIEF:     u"left-image-brack",
		None:           u"left-image-bracket"},
	u"\u2988":{
		VERB_SUPERBRIEF:u"R image-brack",
		VERB_BRIEF:     u"right-image-brack",
		None:           u"right-image-bracket"},
	u"\u2989":{
		VERB_SUPERBRIEF:u"L bind-brack",
		VERB_BRIEF:     u"left-bind-brack",
		None:           u"left-binding-bracket"},
	u"\u298a":{
		VERB_SUPERBRIEF:u"R bind-brack",
		VERB_BRIEF:     u"right-bind-brack",
		None:           u"right-binding-bracket"},
	u"\u298b":{
		VERB_SUPERBRIEF:u"L underbar-brack",
		VERB_BRIEF:     u"left-underbar-brack",
		None:           u"left-underbar-bracket"},
	u"\u298c":{
		VERB_SUPERBRIEF:u"R underbar-brack",
		VERB_BRIEF:     u"right-underbar-brack",
		None:           u"right-underbar-bracket"},
	u"\u298d":{
		VERB_SUPERBRIEF:u"L top-tick-brack",
		VERB_BRIEF:     u"left-top-tick-brack",
		None:           u"left-top-tick-bracket"},
	u"\u298e":{
		VERB_SUPERBRIEF:u"R bottom-tick-brack",
		VERB_BRIEF:     u"right-bottom-tick-brack",
		None:           u"right-bottom-tick-bracket"},
	u"\u298f":{
		VERB_SUPERBRIEF:u"L bottom-tick-brack",
		VERB_BRIEF:     u"left-bottom-tick-brack",
		None:           u"left-bottom-tick-bracket"},
	u"\u2990":{
		VERB_SUPERBRIEF:u"R top-tick-brack",
		VERB_BRIEF:     u"right-top-tick-brack",
		None:           u"right-top-tick-bracket"},
	u"\u2991":{
		VERB_SUPERBRIEF:u"L dotted-angle-brack",
		VERB_BRIEF:     u"left-dotted-angle-brack",
		None:           u"left-dotted-angle-bracket"},
	u"\u2992":{
		VERB_SUPERBRIEF:u"R dotted-angle-brack",
		VERB_BRIEF:     u"right-dotted-angle-brack",
		None:           u"right-dotted-angle-bracket"},
	u"\u2993":{
		VERB_SUPERBRIEF:u"L arc-less-than-brack",
		VERB_BRIEF:     u"left-arc-less-than-brack",
		None:           u"left-arc-less-than-bracket"},
	u"\u2994":{
		VERB_SUPERBRIEF:u"R arc-greater-than-brack",
		VERB_BRIEF:     u"right-arc-greater-than-brack",
		None:           u"right-arc-greater-than-bracket"},
	u"\u2995":{
		VERB_SUPERBRIEF:u"L double-arc-greater-than-brack",
		VERB_BRIEF:     u"left-double-arc-greater-than-brack",
		None:           u"left-double-arc-greater-than-bracket"},
	u"\u2996":{
		VERB_SUPERBRIEF:u"R double-arc-less-than-brack",
		VERB_BRIEF:     u"right-double-arc-less-than-brack",
		None:           u"right-double-arc-less-than-bracket"},
	u"\u2997":{
		VERB_SUPERBRIEF:u"L black-shell-brack",
		None:           u"left-black-shell-bracket"},
	u"\u2998":{
		VERB_SUPERBRIEF:u"R black-shell-brack",
		None:           u"right-black-shell-bracket"},
	u"\u29a0":{None:u"spherical-angle-open-left"},
	u"\u29a1":{None:u"spherical-angle-open-up"},
	u"\u29a2":{None:u"turned-angle"},
	u"\u29a3":{None:u"reversed-angle"},
	u"\u29a4":{None:u"angle-with-under-bar"},
	u"\u29a5":{None:u"reversed-angle-with-under-bar"},
	u"\u29a6":{None:u"oblique-angle-open-up"},
	u"\u29a7":{None:u"oblique-angle-open-down"},
	u"\u29a8":{None:u"measured-angle-with-arrow-point-up-right"},
	u"\u29a9":{None:u"measured-angle-with-arrow-point-up-left"},
	u"\u29aa":{None:u"measured-angle-with-arrow-point-down-right"},
	u"\u29ab":{None:u"measured-angle-with-arrow-point-down-left"},
	u"\u29ac":{None:u"measured-angle-with-arrow-point-right-up"},
	u"\u29ad":{None:u"measured-angle-with-arrow-point-left-up"},
	u"\u29ae":{None:u"measured-angle-with-arrow-point-right-down"},
	u"\u29af":{None:u"measured-angle-with-arrow-point-left-down"},
	u"\u29b0":{None:u"reversed-empty-set"},
	u"\u29b1":{None:u"empty-set-with-ovar-bar"},
	u"\u29b2":{None:u"empty-set-with-circle-above"},
	u"\u29b3":{None:u"empty-set-with-right-arrow-above"},
	u"\u29b4":{None:u"empty-set-with-left-arrow-above"},
	u"\u29b5":{None:u"circle-with-horizontal-bar"},
	u"\u29b6":{None:u"circle-with-vertical-bar"},
	u"\u29b7":{None:u"circled-parallel-sign"},
	u"\u29b8":{None:u"circled-reverse-solidus"},
	u"\u29b9":{None:u"circled-perpendicular"},
	u"\u29ba":{None:u"circled-up-tack"},
	u"\u29bb":{None:u"crossed-out-circle"},
	u"\u29bc":{None:u"circled-percentage"},
	u"\u29bd":{None:u"up-arrow-through-circle"},
	u"\u29be":{None:u"circled-white-bullet"},
	u"\u29bf":{None:u"circled-bullet"},
	u"\u29c0":{None:u"circled-less-than"},
	u"\u29c1":{None:u"circled-greater-than"},
	u"\u29c2":{None:u"circle-with-small-cricle-to-the-right"},
	u"\u29c3":{None:u"circle-with-equal-sign-to-the-right"},
	u"\u29c4":{None:u"squared-up-diagonal-slash"},
	u"\u29c5":{None:u"squared-down-diagonal-slash"},
	u"\u29c6":{None:u"squared-asterisk"},
	u"\u29c7":{None:u"squared-small-circle"},
	u"\u29c8":{None:u"squared-square"},
	u"\u29c9":{None:u"two-joined-squares"},
	u"\u29ca":{None:u"triangle-with-dot-above"},
	u"\u29cb":{None:u"triangle-with-under-bar"},
	u"\u29cc":{None:u"s-in-triangle"},
	u"\u29cd":{None:u"triangle-with-serifs-at-bottom"},
	u"\u29ce":{None:u"right-triangle-above-left-triangle"},
	u"\u29cf":{None:u"left-triangle-beside-vertical-bar"},
	u"\u29d0":{None:u"vertical-bar-beside-right-triangle"},
	u"\u29d1":{None:u"bow-tie-with-left-half-black"},
	u"\u29d2":{None:u"bow-tie-with-right-half-black"},
	u"\u29d3":{None:u"black-bow-tie"},
	u"\u29d4":{None:u"times-with-left-half-black"},
	u"\u29d5":{None:u"times-with-right-half-black"},
	u"\u29d6":{None:u"white-hourglass"},
	u"\u29d7":{None:u"black-hourglass"},
	u"\u29d8":{
		VERB_SUPERBRIEF:u"L wiggly-fence",
		None:           u"left-wiggly-fence"},
	u"\u29d9":{
		VERB_SUPERBRIEF:u"R wiggly-fence",
		None:           u"right-wiggly-fence"},
	u"\u29da":{
		VERB_SUPERBRIEF:u"L double-wiggly-fence",
		None:           u"left-double-wiggly-fence"},
	u"\u29db":{
		VERB_SUPERBRIEF:u"R double-wiggly-fence",
		None:           u"right-double-wiggly-fence"},
	u"\u29dc":{None:u"incomplete-infinity"},
	u"\u29dd":{None:u"tie-over-infinity"},
	u"\u29de":{None:u"infinity-negated-with-vertical-bar"},
	u"\u29e0":{None:u"square-with-contoured-outline"},
	u"\u29e1":{None:u"increases-as"},
	u"\u29e2":{None:u"shuffle-product"},
	u"\u29e3":{None:u"equals-and-slanted-parallel"},
	u"\u29e4":{None:u"equals-and-slanted-parallel-over-tilde"},
	u"\u29e5":{None:u"identical-to-and-slanted-parallel"},
	u"\u29e6":{None:u"tautologically-equals"},
	u"\u29e7":{None:u"thermodynamic"},
	u"\u29e8":{None:u"down-triangle-with-left-half-black"},
	u"\u29e9":{None:u"down-triangle-with-right-half-black"},
	u"\u29ea":{None:u"black-diamond-with-down-arrow"},
	u"\u29eb":{None:u"black-lozenge"},
	u"\u29ec":{None:u"white-circle-with-down-arrow"},
	u"\u29ed":{None:u"black-circle-with-down-arrow"},
	u"\u29ee":{None:u"error-barred-white-square"},
	u"\u29ef":{None:u"error-barred-black-square"},
	u"\u29f0":{None:u"error-barred-white-diamond"},
	u"\u29f1":{None:u"error-barred-black-diamond"},
	u"\u29f2":{None:u"error-barred-white-circle"},
	u"\u29f3":{None:u"error-barred-black-circle"},
	u"\u29f5":{None:u"reverse-solidus"},
	u"\u29f6":{None:u"solidus-with-over-bar"},
	u"\u29f7":{None:u"reverse-solidus-with-horizontal-stroke"},
	u"\u29f8":{None:u"big-solidus"},
	u"\u29f9":{None:u"big-reverse-solidus"},
	u"\u29fa":{None:u"double-plus"},
	u"\u29fb":{None:u"triple-plus"},
	u"\u29fc":{
		VERB_SUPERBRIEF:u"L curve-angle-brack",
		VERB_BRIEF:     u"left-curved-angle-brack",
		None:           u"left-curved-angle-bracket"},
	u"\u29fd":{
		VERB_SUPERBRIEF:u"R curve-angle-brack",
		VERB_BRIEF:     u"right-curved-angle-brack",
		None:           u"right-curved-angle-bracket"},
	u"\u29fe":{None:u"tiny"},
	u"\u29ff":{None:u"miny"},
	u"\u2a1d":{None:u"join"},
	u"\u2a1e":{None:u"large-left-triangle"},
	u"\u2a1f":{None:u"schema-composition"},
	u"\u2a20":{None:u"schema-piping"},
	u"\u2a21":{None:u"schema-projection"},
	u"\u2a22":{None:u"plus-with-circle-above"},
	u"\u2a23":{None:u"plus-with-hat-above"},
	u"\u2a24":{None:u"plus-with-tilde-above"},
	u"\u2a25":{None:u"plus-with-dot-below"},
	u"\u2a26":{None:u"plus-with-tilde-below"},
	u"\u2a27":{None:u"plus-with-subscript-two"},
	u"\u2a28":{None:u"plus-with-black-triangle"},
	u"\u2a29":{None:u"minus-with-comma-above"},
	u"\u2a2a":{None:u"minus-with-dot-below"},
	u"\u2a2b":{None:u"minus-with-falling-dots"},
	u"\u2a2c":{None:u"minus-with-rising-dots"},
	u"\u2a2d":{None:u"plus-in-left-half-circle"},
	u"\u2a2e":{None:u"plus-in-right-half-circle"},
	u"\u2a2f":{None:u"cross"},
	u"\u2a30":{None:u"times-with-dot-above"},
	u"\u2a31":{None:u"times-with-under-bar"},
	u"\u2a32":{None:u"semi-direct-product-with-bottom-closed"},
	u"\u2a33":{None:u"smash-product"},
	u"\u2a34":{None:u"times-in-left-half-circle"},
	u"\u2a35":{None:u"times-in-right-half-circle"},
	u"\u2a36":{None:u"circled-times-with-hat-above"},
	u"\u2a37":{None:u"times-in-double-circle"},
	u"\u2a38":{None:u"circled-division"},
	u"\u2a39":{None:u"plus-in-triangle"},
	u"\u2a3a":{None:u"minus-in-triangle"},
	u"\u2a3b":{None:u"times-in-triangle"},
	u"\u2a3c":{None:u"interior-product"},
	u"\u2a3d":{None:u"right-hand-interior-product"},
	u"\u2a3e":{None:u"relationl-composition"},
	u"\u2a40":{None:u"intersection-with-dot"},
	u"\u2a41":{None:u"union-with-minus"},
	u"\u2a42":{None:u"union-with-over-bar"},
	u"\u2a43":{None:u"intersection-with-over-bar"},
	u"\u2a44":{None:u"intersection-with-logical-and"},
	u"\u2a45":{None:u"union-with-logical-or"},
	u"\u2a46":{None:u"union-above-intersection"},
	u"\u2a47":{None:u"intersection-above-union"},
	u"\u2a48":{None:u"union-above-bar-above-intersection"},
	u"\u2a49":{None:u"intersection-above-bar-above-union"},
	u"\u2a4a":{None:u"union-beside-and-joined-with-union"},
	u"\u2a4b":{None:u"intersection-beside-and-joined-with-intersection"},
	u"\u2a4c":{None:u"closed-union-with-serifs"},
	u"\u2a4d":{None:u"closed-intersection-with-serifs"},
	u"\u2a4e":{None:u"double-square-intersection"},
	u"\u2a4f":{None:u"double-square-union"},
	u"\u2a50":{None:u"closed-union-with-serifs-and-smash-product"},
	u"\u2a51":{None:u"logical-and-with-dot-above"},
	u"\u2a52":{None:u"logical-or-with-dot-above"},
	u"\u2a53":{None:u"double-logical-and"},
	u"\u2a54":{None:u"double-logical-or"},
	u"\u2a55":{None:u"two-intersecting-logical-and"},
	u"\u2a56":{None:u"two-intersecting-logical-or"},
	u"\u2a57":{None:u"sloping-logical-or"},
	u"\u2a58":{None:u"sloping-logical-and"},
	u"\u2a59":{None:u"logical-or-overlapping-logical-and"},
	u"\u2a5a":{None:u"logical-and-with-middle-stem"},
	u"\u2a5b":{None:u"logical-or-with-middle-stem"},
	u"\u2a5c":{None:u"logical-and-with-horizontal-dash"},
	u"\u2a5d":{None:u"logical-or-with-horizontal-dash"},
	u"\u2a5e":{None:u"logical-and-with-double-over-bar"},
	u"\u2a5f":{None:u"logical-and-with-under-bar"},
	u"\u2a60":{None:u"logical-and-with-double-under-bar"},
	u"\u2a61":{None:u"small-v-with-under-bar"},
	u"\u2a62":{None:u"logical-or-with-double-over-bar"},
	u"\u2a63":{None:u"logical-or-with-double-under-bar"},
	u"\u2a64":{None:u"domain-antirestriction"},
	u"\u2a65":{None:u"range-antirestriction"},
	u"\u2a87":{None:u"less-than-and-single-line-not-equals"},
	u"\u2a88":{None:u"greater-than-and-single-line-not-equals"},
	u"\u2aaf":{None:u"precedes-above-single-line-equals"},
	u"\u2ab0":{None:u"succeeds-above-single-line-equals"},
	}


# Regular expressions for MathML parser
RE_SINGLE_LETTER=re.compile(u"\D$")
RE_NUMBER=re.compile(u"[\d.,]+$")
RE_SIGNED_NUMBER=re.compile(u"[+-]?[\d.,]+$")
RE_DECIMAL=re.compile(u"[\d]+$")
RE_SINGLE_DIGIT=re.compile(u"[\d]$")
RE_ROMAN_NUMBER=re.compile(u"[IVXLCDM]+$")


# Constants for MathML parser
PRIMED_OPERATORS=(u"\u2032",u"\u2033",u"\u2034")
SIMPLE_DECORATORS=(u"~",u"^",u"\u00af")
STRETCH_SYMBOLS=(u"[",u"]",u"(",u")",u"{",u"}")
LEVEL_CHANGE_TAGS=(u"msup",u"msub",u"msubsup")
STACK_TAGS=(u"munder",u"mover",u"munderover")
CONTAINER_TAGS=(u"mrow",u"mpadded",u"mstyle",u"mtr",u"mlabeledtr",u"mtd")


class MathSpeakNode(list):

	def __init__(self):
		list.__init__([])
		self.ignore=True
		self.isSeparator=False
		self.isMatrix=False
		self.verb=VERB_VERBOSE
		self.tag=u""
		self.attrs={}
		self.cdata=u""
		self.row=0
		self.col=0
		self.simpleTable=True
		self.frac=0
		self.rad=0
		self.modUnder=0
		self.modOver=0
		self.scriptUnder=0
		self.scriptOver=0
		self.stackLevel=u""
		self.normLevel=u""
		self.startLevel=u""
		self.endLevel=u""
		self.tableText=u""
		self.rowLabel=u""
		self.crossOutText=u""
		self.text=u""
		self.excludedStartText=[]

	def __unicode__(self):
		texts=[]
		for x in self:
			texts.append(u"["+x.text+u"]")
		return u"["+u",".join(texts)+u"]"

	def _newChildNode(self,tag,cdata=u""):
		child=self.__class__()
		child.tag=tag
		child.cdata=cdata
		child.verb=self.verb
		child.ignore=self.ignore
		child.normLevel=self.normLevel
		child.startLevel=self.normLevel
		child.endLevel=self.normLevel
		child.stackLevel=self.normLevel
		return child

	def _newOperatorNode(self,cdata):
		child=self._newChildNode(u"mo",cdata)
		child._translate_mo()
		return child

	def _findName(self,dict,value):
		if value in dict:
			entry=dict[value]
			if self.verb in entry:
				return entry[self.verb]
			elif None in entry:
				return entry[None]
		return value

	def _isLetter(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isLetter()
		else:
			return (self.tag==u"mi" and
					RE_SINGLE_LETTER.match(self.cdata)!=None)

	def _isNumber(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isNumber()
		else:
			return (self.tag==u"mn" and
					RE_NUMBER.match(self.cdata)!=None)

	def _table(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._table()
		elif self.tag==u"mtable":
			return self
		else:
			return None

	def _crossOut(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._crossOut()
		elif len(self.crossOutText)>0:
			return self
		else:
			return None

	def _isLevelChanger(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isLevelChanger()
		else:
			return self.tag in LEVEL_CHANGE_TAGS

	def _isOperator(self,value):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isOperator(value)
		elif isinstance(value,tuple):
			return self.tag==u"mo" and self.cdata in value
		else:
			return self.tag==u"mo" and self.cdata==value

	def _isPrimed(self):
		return self._isOperator(PRIMED_OPERATORS)

	def _isMathOperator(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isMathOperator()
		else:
			return (self.tag==u"mo" and
					RE_SINGLE_LETTER.match(self.cdata)!=None)

	def _isModifiedLetter(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isModifiedLetter()
		elif len(self)>1 and self.tag in STACK_TAGS:
			return self[0]._isModifiedLetter()
		else:
			return self._isLetter()

	def _isDottedDigit(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isDottedDigit()
		else:
			return (len(self)==2 and self.tag==u"mover" and
					self[0].tag==u"mn" and
					RE_SINGLE_DIGIT.match(self[0].cdata)!=None and
					self[1].text==self._findName(OPERATOR_DICT,u"\u00b7"))

	def _isBarredDecimal(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._isBarredDecimal()
		else:
			return (len(self)==2 and self.tag==u"mover" and
					self[0]._isNumber() and self[1]._isOperator(u"\u00af"))

	def _tableRow(self,row):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._tableRow(row)
		elif self.tag==u"mtable":
			count=0
			for x in self:
				if not x.tag in(u"mtr",u"mlabeledtr"):  continue
				if count==row:
					return x
				count+=1
			return None

	def _rawNumber(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._rawNumber()
		elif len(self)==2 and self.tag==u"mover":
			return self[0]._rawNumber()
		elif self.tag==u"mn":
			return self.text
		else:
			return u""

	def _rawOperator(self):
		if len(self)==1 and self.tag in CONTAINER_TAGS:
			return self[0]._rawOperator()
		elif self.tag==u"mo" and not self.isSeparator:
			return self.cdata
		else:
			return u""

	def _ordinalAbbrev(self,idx):
		if idx%10==1 and idx!=11:  return str(idx)+u"st"
		if idx%10==2 and idx!=12:  return str(idx)+u"nd"
		if idx%10==3 and idx!=13:  return str(idx)+u"rd"
		else:                      return str(idx)+u"th"

	def _levelLabel(self,oldLevel,newLevel=None):
		if newLevel==None:  newLevel=oldLevel
		if newLevel==u"":
			return u" "+self._findName(LABEL_DICT,u"baseline")+u" "
		else:
			label=u""
			if len(oldLevel)>0 and oldLevel[0]!=newLevel[0]:
				# Report baseline first when script level crosses it
				label=self._findName(LABEL_DICT,u"baseline")+u" "
			for n in range(len(newLevel)):
				if newLevel[n]==u"-":
					label+=self._findName(LABEL_DICT,u"sub")
				else:
					label+=self._findName(LABEL_DICT,u"super")
			label+=self._findName(LABEL_DICT,u"scriptclose")
			return u" "+label+u" "

	def _tableLabels(self,openSym,closeSym):
		# Determine opening, body, and closing labels for <mtable>
		start=self._findName(LABEL_DICT,u"start")
		end=self._findName(LABEL_DICT,u"end")
		by=self._findName(LABEL_DICT,u"by")
		isMatrix=False
		opening=u""
		body=self.tableText
		closing=u""
		used=0
		if self.row==2 and self.col==1 and openSym==u"(" and closeSym==u")":
			# 2x1 <mtable> enclosed by parenthesis is binomial
			bin=self._findName(LABEL_DICT,u"binomial")
			opening=start+bin
			body=u" ".join((
				self._tableRow(0).text,
				self._findName(LABEL_DICT,u"choose"),
				self._tableRow(1).text))
			closing=end+bin
			used=2
		elif ((openSym==u"(" and closeSym==u")") or
				(openSym==u"[" and closeSym==u"]")):
			# <mtable> enclosed by brackets or parenthesis is matrix
			isMatrix=True
			mat=self._findName(LABEL_DICT,u"matrix")
			opening=u" ".join((start,str(self.row),by,str(self.col),mat))
			closing=end+mat
			used=2
		elif openSym==u"|" and closeSym==u"|":
			# <mtable> enclosed by vertical bars is determinant
			det=self._findName(LABEL_DICT,u"determinant")
			opening=u" ".join((start,str(self.row),by,str(self.col),det))
			closing=end+det
			used=2
		else:
			# All other <mtable> are layout elements
			layout=self._findName(LABEL_DICT,u"layout")
			enlarged=self._findName(LABEL_DICT,u"enlarged")
			opening=start+layout
			closing=end+layout
			# Report enlarged opening or closing symbols
			if openSym in STRETCH_SYMBOLS:
				label=self._findName(OPERATOR_DICT,openSym)
				opening=u" ".join((opening,enlarged,label))
				used+=1
			if closeSym in STRETCH_SYMBOLS:
				label=self._findName(OPERATOR_DICT,closeSym)
				closing=u" ".join((enlarged,label,closing))
				used+=1
		return (opening,body,closing,used,isMatrix)

	def _identifyAbsoluteValues(self):
		# Identify <mo> with vertical bars that represent absolute values
		abs=self._findName(LABEL_DICT,u"absolute")
		start=self._findName(LABEL_DICT,u"start")+abs
		end=self._findName(LABEL_DICT,u"end")+abs
		l=len(self)
		n=0
		opened=False
		while n<l:
			if (self[n]._rawOperator()==u"|"):
				if ((n+2)<l and self[n+1]._table() and
						self[n+2]._rawOperator()==u"|"):
					n+=3
					continue
				opened=not opened
				if opened:
					self[n].text=start
				else:
					self[n].text=end
			n+=1

	def _identifyTables(self):
		# Identify <mtable> tags based on context
		start=self._findName(LABEL_DICT,u"start")
		end=self._findName(LABEL_DICT,u"end")
		by=self._findName(LABEL_DICT,u"by")
		l=len(self)
		n=0
		while n<l:
			if (n+1)<l:
				tbl=self[n+1]._table()
			else:
				tbl=None
			o=self[n]._rawOperator()
			if tbl and (n+2)<l:
				c=self[n+2]._rawOperator()
				if tbl and o!=u"" and c!=u"":
					# Handle <...> <mtable> <...>
					(opening,body,closing,used,isMatrix)=tbl._tableLabels(o,c)
					if used==2:
						self[n].text=opening
						self[n+1].text=body
						self[n+2].text=closing
						self[n].isMatrix=isMatrix
						self[n+1].isMatrix=isMatrix
						self[n+2].isMatrix=isMatrix
						n+=3
						continue
			if tbl and (n+1)<l:
				# Handle <...> <mtable>
				(opening,body,closing,used,isMatrix)=tbl._tableLabels(o,u"")
				if used==1:
					self[n].text=opening
					self[n+1].text=u" ".join((body,closing))
					n+=2
					continue
			tbl=self[n]._table()
			if tbl and (n+1)<l:
				# Handle <mtable> <...>
				c=self[n+1]._rawOperator()
				if c!=u"":
					(opening,body,closing,used,isMatrix)=tbl._tableLabels(u"",c)
					if used==1:
						self[n].text=u" ".join((opening,body))
						self[n+1].text=closing
						n+=2
						continue
			if self[n].tag==u"mtable":
				# Handle standalone <mtable> only if it is a direct child
				(opening,body,closing,used,isMatrix)=tbl._tableLabels(u"",u"")
				self[n].text=u" ".join((opening,body,closing))
			n+=1

	def _identifyRepeatingDigits(self):
		# Identify consecutive <mover> tags with repeating digits
		n=0
		while n<(len(self)-1):
			if self[n]._isDottedDigit() and self[n+1]._isDottedDigit():
				# Setup start of group indicator 
				prefix=(self._findName(LABEL_DICT,u"modifying")+
						self._findName(LABEL_DICT,u"each")+
						self._findName(LABEL_DICT,u"above"))
				self[n].text=u" ".join((prefix,self[n]._rawNumber()))
				self[n+1].text=self[n+1]._rawNumber()
				# Change all consecutive dotted digits
				count=2
				for k in range(n+2,len(self)):
					if not self[k]._isDottedDigit():  break
					self[k].text=self[k]._rawNumber()
					count+=1
					n+=1
				# Setup end of group indicator
				self[n+1].text=u" ".join((self[n+1]._rawNumber(),
					self._findName(LABEL_DICT,u"with"),
					self._findName(OPERATOR_DICT,u"\u00b7")))
			elif self[n]._isNumber() and self[n+1]._isBarredDecimal():
				# Force reading of decimal point
				if self[n].text[-1]==u".":
					self[n].text=u" ".join((self[n].text[0:-1],
							self._findName(LABEL_DICT,u"point")))
				# Individually read each digit
				prefix=(self._findName(LABEL_DICT,u"modifying")+
						self._findName(LABEL_DICT,u"above"))
				digits=u" ".join(list(self[n+1]._rawNumber()))
				self[n+1].text=u" ".join((prefix,digits,
					self._findName(LABEL_DICT,u"with"),
					self._findName(OPERATOR_DICT,u"\u00af")))
				n+=1
			n+=1

	def _identifyCrossProducts(self):
		# Identify multiplication signs between matrices as cross operators
		for n in range(1,len(self)-1):
			if not self[n-1].isMatrix:  continue
			if not self[n+1].isMatrix:  continue
			x=self[n]
			if x._rawOperator() in (u"\u00d7",u"\u2062"):
				x.text=self._findName(OPERATOR_DICT,u"\u2a2f")

	def _mergeText(self,prefixLabel=True):
		# Merge text from child nodes 
		self.cdata=u""
		if len(self)==0:  return
		self._identifyAbsoluteValues()
		self._identifyTables()
		self._identifyCrossProducts()
		self._identifyRepeatingDigits()
		l=self.startLevel=self[0].startLevel
		if prefixLabel and self.startLevel!=self.normLevel:
			levelLabel=self._levelLabel(self.normLevel,self.startLevel)
			self.excludedStartText.append(levelLabel)
			self.text=levelLabel
			self.startLevel=self.normLevel
		for n in range(len(self)):
			x=self[n]
			# Determine text separator
			sep=None
			if l!=x.startLevel:
				# Report change in script level
				sep=self._levelLabel(l,x.startLevel)
			elif n>0:
				prev=self[n-1]
				if len(l) and prev._isLevelChanger() and x._isLevelChanger():
					# Re-state script level for different expressions
					sep=self._levelLabel(l,x.startLevel)
				elif prev._isLetter() and x._isNumber():
					# Report baseline if number could be mistaken as subscript
					sep=self._levelLabel(u"")
				elif prev._isNumber() and x.tag==u"mfrac" and x.frac==0:
					# Append "and" if numeric fraction follows a number
					sep=self._findName(LABEL_DICT,u"and")
			# Append child text now
			if sep:
				x.excludedStartText.append(sep)
				self.text+=u" "+sep+u" "
			else:
				self.text+=u" "
			self.text+=x.text
			# Keep track of ending script level in text
			l=x.endLevel
		# Update ending script level
		self.endLevel=l
		self.text=self.text.strip()
		# Determine whether this expression is a matrix
		self.isMatrix=True
		for x in self:
			if not x.isMatrix:
				self.isMatrix=False
				break

	def _mergeNumericFraction(self):
		# Override this method to perform locale-specific translation
		pass

	def _mergeCrossOut(self,crossout,mod=u""):
		cancel=self._findName(LABEL_DICT,u"cancel")
		if len(mod)>0:
			self.text=u" ".join((
				cancel,
				crossout.crossOutText,
				self._findName(LABEL_DICT,u"cancelwith"),
				mod,
				self._findName(LABEL_DICT,u"end")+cancel))
		else:
			self.text=u" ".join((
				cancel,
				crossout.crossOutText,
				self._findName(LABEL_DICT,u"end")+cancel))

	def _defaultTranslation(self):
		self.cdata=u""

	def _translate_math(self):
		self._mergeText()

	def _translate_mtext(self):
		# <mtext> reads out CDATA
		self.text=re.sub(u" +",u" ",self.cdata.strip())

	def _translate_mphantom(self):
		# <mphantom> requires processing but generates no text output
		self._mergeText()
		self.text=u""

	def _translate_mrow(self):
		self._mergeText(prefixLabel=False)

	def _translate_menclose(self):
		self._mergeText()
		# Detect crossed out expressions
		notations=[u"longdiv"]
		if u"notation" in self.attrs:
			notations=self.attrs[u"notation"].split()
		if (u"updiagonalstrike" in notations or
			u"downdiagonalstrike" in notations or
			u"verticalstrike" in notations or
			u"horizontalstrike" in notations):
			self.crossOutText=self.text
			self._mergeCrossOut(self)

	def _translate_maction(self):
		if len(self)==0:  return
		# Use only the first expression in <maction> 
		self.text=self[0].text
		self.startLevel=self[0].startLevel
		self.endLevel=self[0].endLevel

	def _translate_mpadded(self):
		self._mergeText(prefixLabel=False)

	def _translate_ms(self):
		self._translate_mtext()
		label=self._findName(LABEL_DICT,u"string")
		self.text=u" ".join((
			self._findName(LABEL_DICT,u"start")+label,
			self.text,
			self._findName(LABEL_DICT,u"end")+label))

	def _translate_mglyph(self):
		if u"alt" in self.attrs:
			self.text=self.attrs[u"alt"]

	def _translate_maligngroup(self):
		self.cdata=u""

	def _translate_malignmark(self):
		self.cdata=u""

	def _translate_merror(self):
		self._mergeText()
		label=self._findName(LABEL_DICT,u"error")
		self.text=u" ".join((
			self._findName(LABEL_DICT,u"start")+label,
			self.text,
			self._findName(LABEL_DICT,u"end")+label))

	def _translate_mstyle(self):
		self._mergeText()
		if not u"mathvariant" in self.attrs:  return
		single=(len(self)==1 and
			(self[0]._isLetter() or self[0]._isMathOperator()))
		variant=self.attrs[u"mathvariant"]
		prefix=u""
		suffix=u""
		if variant in VARIANT_DICT:
			prefix=self._findName(VARIANT_DICT,variant)
			if not single:
				suffix=self._findName(LABEL_DICT,u"end")+prefix
				prefix=self._findName(LABEL_DICT,u"start")+prefix
		self.text=u" ".join((prefix,self.text,suffix))

	def _mergeSimpleTable(self):
		self.text=u""
		self.row=0
		for x in self:
			if not x.tag in(u"mtr",u"mlabeledtr"):  continue
			# Generate simplified text for row 
			data=[]
			for y in x:
				if y.tag==u"mtd":  data.append(y.text)
			x.text=u" ".join(data)
			# Extend table text now
			self.row+=1
			self.text=u" ".join((self.text,self._ordinalAbbrev(self.row),
					self._findName(LABEL_DICT,u"row"),x.text))

	def _translate_mtable(self):
		# <mtable> resets ending script level
		self.cdata=u""
		self.endLevel=self.startLevel
		for x in self:
			if not x.tag in (u"mtr",u"mlabeledtr"):  continue
			if self.simpleTable:
				self.simpleTable=x.simpleTable
			if (self.col<x.col):  self.col=x.col
			self.row+=1
			self.text=u" ".join((self.text,self._ordinalAbbrev(self.row),
					self._findName(LABEL_DICT,u"row"),x.text))
		if self.simpleTable:
			self._mergeSimpleTable()
		self.tableText=self.text

	def _translate_mtr(self):
		self.cdata=u""
		self.endLevel=self.startLevel
		if self.rowLabel!=u"":
			label=self._findName(LABEL_DICT,u"label")
			self.text=u" ".join((
				self._findName(LABEL_DICT,u"start")+label,
				self.rowLabel,
				self._findName(LABEL_DICT,u"end")+label))
		for x in self:
			if x.tag!=u"mtd":  continue
			if len(self)>1 and self.simpleTable:
				self.simpleTable=x._isLetter() or x._isNumber()
			self.col+=1
			self.text=u" ".join((self.text,self._ordinalAbbrev(self.col),
					self._findName(LABEL_DICT,u"column"),x.text))

	def _translate_mlabeledtr(self):
		# Use first <mtd> as row label and convert into <mtr>
		for n in range(len(self)):
			if self[n].tag!=u"mtd":  continue
			self.rowLabel=self[n].text
			self.pop(n)
			break
		self.tag=u"mtr"
		self._translate_mtr()

	def _translate_mtd(self):
		self._mergeText()
		if self.text==u"":
			self.text=self._findName(LABEL_DICT,u"blank")

	def _translate_mspace(self):
		self.cdata=u""

	def _translate_mn(self):
		value=self.cdata=re.sub(u" +",u" ",self.cdata.strip())
		if RE_SIGNED_NUMBER.match(value):
			# Handle normal number
			if   value[0]==u"-":
				self.text=u" ".join(
					(self._findName(LABEL_DICT,u"negative"),value[1:]))
			elif value[0]==u"+":
				self.text=u" ".join(
					(self._findName(LABEL_DICT,u"positive"),value[1:]))
			else:
				self.text=value
		elif RE_ROMAN_NUMBER.match(value):
			# Handle Roman numeral
			if len(value)>1:
				prefix=self._findName(LABEL_DICT,u"capword")
			else:
				prefix=self._findName(LABEL_DICT,u"capital")
			chars=list(value)
			self.text=u" ".join((prefix,u" ".join(chars)))
		else:
			# Handle number that contains letters
			chars=[self._findName(OPERATOR_DICT,x) for x in list(value)]
			self.text=u" ".join((
				self._findName(LABEL_DICT,u"number"),
				u" ".join(chars)))

	def _translate_mi(self):
		value=self.cdata=self.cdata.strip()
		self.text=self._findName(IDENTIFIER_DICT,value)
		if len(value)==1 and value[0].isupper():
			self.text=u" ".join(
					(self._findName(LABEL_DICT,u"capital"),self.text))

	def _translate_mo(self):
		value=self.cdata=self.cdata.strip()
		self.text=self._findName(OPERATOR_DICT,value)

	def _translate_mfenced(self):
		# Determine opening symbol, closing symbol and separators
		openSym=u"("
		if u"open" in self.attrs:
			openSym=self.attrs[u"open"]
		closeSym=u")"
		if u"close" in self.attrs:
			closeSym=self.attrs[u"close"]
		separators=u","
		if u"separators" in self.attrs:
			separators=re.sub(u" +",u"",self.attrs[u"separators"])
		# Convert <mfenced> into equivalent <mrow> representation
		self.tag=u"mrow"
		if len(separators)>0:
			n=1
			while n<len(self):
				# Insert current separator between child nodes
				child=self._newOperatorNode(separators[0])
				child.isSeparator=True
				self.insert(n,child)
				# Advance to next separator
				if len(separators)>1:
					separators=separators[1:]
				n+=2
		if len(openSym)>0:
			self.insert(0,self._newOperatorNode(openSym))
		if len(closeSym)>0:
			self.append(self._newOperatorNode(closeSym))
		# Detect sets
		if len(self)>1 and openSym==u"{" and closeSym==u"}" and separators==u",":
			set=self._findName(LABEL_DICT,u"set")
			self[0].text=self._findName(LABEL_DICT,u"start")+set
			self[-1].text=self._findName(LABEL_DICT,u"end")+set
		# Process as a <mrow> now
		self._translate_mrow()

	def _mergeSuperscript(self,script):
		if script.text==u"":
			self._translate_mrow()
			return
		sep=self._levelLabel(self[0].endLevel,script.startLevel)
		if self[0].text==u"":
			sep=u""
			self.startLevel=script.startLevel
		elif self[0].startLevel==self[0].endLevel:
			if script.text==u"2" and script.startLevel==(self.startLevel+u"+"):
				label=self._findName(LABEL_DICT,u"squared")
				self.text=u" ".join((self[0].text,label))
				self[1].text=label
				return
			if script.text==u"3" and script.startLevel==(self.startLevel+u"+"):
				label=self._findName(LABEL_DICT,u"cubed")
				self.text=u" ".join((self[0].text,label))
				self[1].text=label
				return
		self.endLevel=script.endLevel
		self[1].excludedStartText.append(sep)
		self.text=self[0].text+sep+script.text

	def _mergeSubscript(self,script):
		if script.text==u"":
			self._translate_mrow()
			return
		sep=self._levelLabel(self[0].endLevel,script.startLevel)
		if self[0]._isLetter() and script._isNumber():
			# Read numeric subscript without level label
			sep=u" "
			self.endLevel=self.startLevel
		else:
			self.endLevel=script.endLevel
			if self[0].text==u"":
				sep=u""
				self.startLevel=script.startLevel
		self.text=self[0].text+sep+script.text

	def _translate_msup(self):
		self.cdata=u""
		if len(self)!=2:  return
		self._mergeSuperscript(self[1])

	def _translate_msub(self):
		self.cdata=u""
		if len(self)!=2:  return
		self._mergeSubscript(self[1])

	def _translate_msubsup(self):
		self.cdata=u""
		if len(self)!=3:  return
		if self[1].text==u"":
			# Treat as <msup> if subscript is empty
			self._mergeSuperscript(self[2])
			return
		elif self[2].text==u"":
			# Treat as <msub> if superscript is empty
			self._mergeSubscript(self[1])
			return
		elif self[2]._isPrimed():
			# Read primed superscript first
			sep=self._levelLabel(self[1].startLevel)
			if self[0]._isLetter() and self[1]._isNumber():
				# Read numeric subscript without level label
				sep=u" "
				self.endLevel=self.startLevel
			else:
				self.endLevel=self[1].endLevel
				if self[0].text==u"":
					self.startLevel=self[1].startLevel
			self.text=self[0].text+u" "+self[2].text+sep+self[1].text
		else:
			# Otherwise read subscript before superscript
			self.endLevel=self[2].endLevel
			sep=self._levelLabel(self[0].endLevel,self[1].startLevel)
			if self[0]._isLetter() and self[1]._isNumber():
				# Read numeric subscript without level label
				sep=u" "
				if self[2].text==u"2" and self[2].startLevel==(self.startLevel+u"+"):
					self.text=u" ".join((self[0].text,self[1].text,
							self._findName(LABEL_DICT,u"squared")))
					return
				if self[2].text==u"3" and self[2].startLevel==(self.startLevel+u"+"):
					self.text=u" ".join((self[0].text,self[1].text,
							self._findName(LABEL_DICT,u"cubed")))
					return
			elif self[0].text==u"":
				sep=u" "
				self.startLevel=self[1].startLevel
			self.text=self[0].text+sep+self[1].text
			self.text+=self._levelLabel(self[2].startLevel)
			self.text+=self[2].text

	def _translate_mmultiscripts(self):
		self.cdata=u""
		if len(self)==0:  return
		# Convert <mmultiscripts> into equivalent <mrow> representation
		self.tag=u"mrow"
		children=[self.pop(0)]
		insertPos=-1
		while len(self)>0:
			x=self.pop(0)
			if x.tag==u"mprescripts":
				insertPos=0
				continue
			if len(self)==0:
				# Subscript and superscript must come in pairs
				break
			y=self.pop(0)
			# Fix <none> nodes
			if x.tag==u"none" and y.tag==u"none":
				continue
			if x.tag==u"none":
				x.tag=u"mi"
				x.text=u""
			if y.tag==u"none":
				y.tag=u"mi"
				y.text=u""
			# Construct <msubsup> node
			child=self._newChildNode(u"msubsup")
			child.append(self._newChildNode(u"mi"))
			child.append(x)
			child.append(y)
			child._translate_msubsup()
			# Insert <msubsup> node at the appropriate location
			if insertPos>=0:
				children.insert(insertPos,child)
				insertPos+=1
			else:
				children.append(child)
		# Process as a <mrow> now
		while len(children)>0:
			self.append(children.pop(0))
		self._translate_mrow()

	def _radicalLabels(self,level):
		# Determine index, opening and closing labels
		nest=self._findName(LABEL_DICT,u"rootnest")
		index=self._findName(LABEL_DICT,u"rootindex")
		opening=self._findName(LABEL_DICT,u"rootstart")
		closing=self._findName(LABEL_DICT,u"rootend")
		if   level==1:  prefix=u""
		elif level==2:  prefix=nest
		elif level==3:  prefix=nest+self._findName(LABEL_DICT,u"twice")
		else:           prefix=nest+str(level-1)
		return (prefix+index,prefix+opening,prefix+closing)

	def _translate_mroot(self):
		self.cdata=u""
		if len(self)!=2:  return
		self.rad+=1
		self.endLevel=self.startLevel
		(index,opening,closing)=self._radicalLabels(self.rad)
		self.text=u" ".join((index,self[1].text,opening,self[0].text,closing))

	def _translate_msqrt(self):
		self.cdata=u""
		if len(self)==0:  return
		self._mergeText()
		self.rad+=1
		(index,opening,closing)=self._radicalLabels(self.rad)
		self.text=u" ".join((opening,self.text,closing))

	def _translate_mfrac(self):
		self.cdata=u""
		if len(self)!=2:  return
		# Handle numeric fractions
		self._mergeNumericFraction()
		if self.text!=u"":  return
		# TODO: Identify continued fraction 
		# Determine opening, middle and closing text
		label=self._findName(LABEL_DICT,u"frac")
		start=self._findName(LABEL_DICT,u"start")
		end=self._findName(LABEL_DICT,u"end")
		over=self._findName(LABEL_DICT,u"fracover")
		nest=self._findName(LABEL_DICT,u"fracnest")
		self.frac+=1
		if self.verb==VERB_SUPERBRIEF:
			if   self.frac==1:  prefix=u""
			elif self.frac==2:  prefix=nest
			elif self.frac==3:  prefix=nest+self._findName(LABEL_DICT,u"twice")
			else:               prefix=nest+str(self.frac-1)
			opening=prefix+label
			middle=prefix+over
			closing=prefix+end+label
		else:
			opening=label
			middle=u""
			closing=label
			for n in range(self.frac):
				opening=start+opening
				middle=over+middle
				closing=end+closing
		# Combine into text
		self[1].excludedStartText.append(middle)
		self.text=u" ".join((opening,self[0].text,middle,self[1].text,closing))

	def _stackText(self,location,modifier):
		if modifier.text==u"":  return
		# Check for crossed out item
		if len(self.stackLevel)==1:
			crossout=self[0]._crossOut()
			if crossout:
				self._mergeCrossOut(crossout,modifier.text)
				return
		# Adjust modifier text
		dot=self._findName(OPERATOR_DICT,u"\u00b7")
		twoDots=self._findName(LABEL_DICT,u"..")
		if modifier.text==self._findName(OPERATOR_DICT,u"."):
			modifier.text=dot
		elif modifier.text==dot+u" "+dot:
			modifier.text=twoDots
		mod=modifier.text
		# Perform special proessing when symbol is single letter variable
		if (self[0]._isModifiedLetter() and
				modifier._isOperator(SIMPLE_DECORATORS)):
			self.text+=(u" "+self._findName(LABEL_DICT,location)+u"-"+
					self._findName(OPERATOR_DICT,modifier._rawOperator()))
			return
		# Check for need to open stack
		open=True
		modCount=self.modUnder+self.modOver
		if (self.scriptUnder+self.scriptOver)>0:
			pass
		elif location==u"over" and self.modUnder>0 and modCount>1:
			pass
		elif location==u"under" and self.modOver>0 and modCount>1:
			pass
		elif mod in (dot,twoDots) or modifier._isMathOperator():
			open=False
		# Perform translation now
		if open:
			label=self._findName(LABEL_DICT,u"script")
			if location==u"over":
				self.scriptOver+=1
				prefix=self._findName(LABEL_DICT,u"over")
				for n in range(self.scriptOver):  label=prefix+label
			else:
				self.scriptUnder+=1
				prefix=self._findName(LABEL_DICT,u"under")
				for n in range(self.scriptUnder):  label=prefix+label
			self.text=u" ".join((self.text,label,mod))
		else:
			label=self._findName(LABEL_DICT,u"modifying")
			if location==u"over":
				self.modOver+=1
				suffix=self._findName(LABEL_DICT,u"above")
				for n in range(self.modOver):  label=label+suffix
			else:
				self.modUnder+=1
				suffix=self._findName(LABEL_DICT,u"below")
				for n in range(self.modUnder):  label=label+suffix
			self.text=u" ".join((label,self.text,
				self._findName(LABEL_DICT,u"with"),mod))

	def _endScripts(self):
		if len(self.stackLevel)>1:  return
		if (self.scriptOver+self.scriptUnder)==0:  return
		self.text+=u" "+self._findName(LABEL_DICT,u"scriptend")

	def _translate_mover(self):
		self.cdata=u""
		if len(self)!=2:  return
		self.text=self[0].text
		self._stackText(u"over",self[1])
		self._endScripts()

	def _translate_munder(self):
		self.cdata=u""
		if len(self)!=2:  return
		self.text=self[0].text
		self._stackText(u"under",self[1])
		self._endScripts()

	def _translate_munderover(self):
		self.cdata=u""
		if len(self)!=3:  return
		self.text=self[0].text
		self._stackText(u"under",self[1])
		self._stackText(u"over",self[2])
		self._endScripts()


class MathSpeak(object):

	def translate(self,math,verbosity=u"verbose",interactive=False):
		# Determine verbosity
		verb=VERB_VERBOSE
		if   verbosity==u"superbrief":  verb=VERB_SUPERBRIEF
		elif verbosity==u"brief":       verb=VERB_BRIEF
		self.interactive=interactive
		# Perform actual translation
		node=self._createNode()
		node.verb=verb
		self._stack=[node]
		self._text=[]
		try:
			parser=expat.ParserCreate(u"utf-8")
			parser.StartElementHandler=self._startElementHandler
			parser.EndElementHandler=self._endElementHandler
			parser.CharacterDataHandler=self._characterDataHandler
			parser.Parse(math)
		except expat.ExpatError:
			return u""
		# Return collected text
		return u"\n".join(self._text)

	def _createNode(self):
		return MathSpeakNode()

	def _startElementHandler(self,tag,attrs):
		# Strip namespace.
		tag=tag.split(":",1)[-1]
		parent=self._stack[-1]
		node=self._createNode()
		node.tag=tag.lower()
		node.attrs=attrs
		node.verb=parent.verb
		if node.tag==u"math":
			node.ignore=False
		else:
			node.ignore=parent.ignore
		# Perform special processing for MathML tags
		if not node.ignore:
			# Determine script level of new node
			node.normLevel=parent.normLevel
			adj=u""
			if   parent.tag==u"msup" and len(parent)==1:  adj=u"+"
			elif parent.tag==u"msub" and len(parent)==1:  adj=u"-"
			elif parent.tag==u"msubsup":
				if   len(parent)==1:  adj=u"-"
				elif len(parent)==2:  adj=u"+"
			elif parent.tag==u"mmultiscripts" and len(parent)>0:
				isSubscript=True
				for n in range(1,len(parent)):
					if parent[n].tag!=u"mprescripts":
						isSubscript=not isSubscript
				if isSubscript:  adj=u"-"
				else:            adj=u"+"
			node.normLevel+=adj
			node.startLevel=node.endLevel=node.normLevel
			# Determine stack level of new node
			node.stackLevel=parent.stackLevel
			if node.tag in STACK_TAGS:
				node.stackLevel+=u"."
		# Append node to parent
		parent.append(node)
		# Push new node on stack
		self._stack.append(node)

	def _endElementHandler(self,tag):
		# Pop completed node from stack
		node=self._stack.pop()
		parent=self._stack[-1]
		# Ignore nodes outside <math> tag
		if node.ignore:
			del parent[-1]
			return
		# Look for specialized translation method
		try:
			func=getattr(node,u"_translate_"+node.tag)
		except AttributeError:
			func=node._defaultTranslation
		# Generate translated text now
		func.__call__()
		# Keep track of nested elements
		parent.frac=max(parent.frac,node.frac)
		parent.rad=max(parent.rad,node.rad)
		parent.scriptUnder=max(parent.scriptUnder,node.scriptUnder)
		parent.scriptOver=max(parent.scriptOver,node.scriptOver)
		parent.modUnder=max(parent.modUnder,node.modUnder)
		parent.modOver=max(parent.modOver,node.modOver)
		# Collect text from <math> nodes
		if node.tag==u"math":
			self._text.append(re.sub(u" +",u" ",node.text))
			if not self.interactive:
				# This won't be used for interaction, so delete the tree.
				del parent[-1]

	def _characterDataHandler(self,data):
		node=self._stack[-1]
		node.cdata+=data


# vim: set tabstop=4 shiftwidth=4:
