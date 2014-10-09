#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright 2014 NV Access Limited

class InteractiveMathSpeak(object):

	def __init__(self, mathSpeak, mathMl):
		self.mathSpeak = mathSpeak
		mathSpeak.translate(mathMl, interactive=True)
		node = self.node = mathSpeak._stack[0][0]
		# If descending would land on a node which has no siblings,
		# make that node the root.
		if len(node) == 1:
			node[0].parent = node
			node = node[0]
			while self._isUselessNode(node):
				try:
					node[0].parent = node
					node = node[0]
				except IndexError:
					node = None
					break
			if node is not None and len(node.parent) == 1:
				self.node = node
		self.node.parent = None
		self.node.indexInParent = 0

	def _getChild(self, parent, index):
		if parent is None or index < 0:
			raise LookupError
		try:
			node = parent[index]
		except IndexError:
			raise LookupError
		node.parent = parent
		node.indexInParent = index
		return node

	def _nodeMovementText(self):
		text = []
		text.extend(self.node.excludedStartText)
		text.append(self.node.text)
		return " ".join(text)

	def _isUselessNode(self, node):
		return node.tag == "mrow" and len(node.parent) == 1

	def nextNode(self):
		self.node = self._getChild(self.node.parent, self.node.indexInParent + 1)
		return self._nodeMovementText()

	def previousNode(self):
		self.node = self._getChild(self.node.parent, self.node.indexInParent - 1)
		return self._nodeMovementText()

	def childNode(self):
		node = self._getChild(self.node, 0)
		while self._isUselessNode(node):
			node = self._getChild(node, 0)
		self.node = node
		return self._nodeMovementText()

	def parentNode(self):
		node = self.node.parent
		if node is None:
			raise LookupError
		while self._isUselessNode(node):
			node = node.parent
		self.node = node
		return self._nodeMovementText()

	def _findTableCell(self):
		node = self.node
		while node is not None and node.tag != "mtd":
			node = node.parent
		if node is not None:
			return node
		raise LookupError

	def nextColumn(self):
		if self.node.tag == "mtable":
			# Move to the first cell in the table.
			self.node = self._getChild(self._getChild(self.node, 0), 0)
			return self._nodeMovementText()
		elif self.node.tag == "mtr":
			# Move to the first cell in the row.
			self.node = self._getChild(self.node, 0)
			return self._nodeMovementText()
		node = self._findTableCell()
		self.node = self._getChild(node.parent, node.indexInParent + 1)
		return self._nodeMovementText()

	def previousColumn(self):
		node = self._findTableCell()
		self.node = self._getChild(node.parent, node.indexInParent - 1)
		return self._nodeMovementText()

	def nextRow(self):
		if self.node.tag == "mtable":
			# Move to the first cell in the table.
			self.node = self._getChild(self._getChild(self.node, 0), 0)
			return self._nodeMovementText()
		elif self.node.tag == "mtr":
			# Move to the first cell in the next row.
			oldRow = self.node
			colIndex = 0
		elif self.node.tag == "mtd":
			oldRow = self.node.parent
			colIndex = self.node.indexInParent
		else:
			raise LookupError
		table = oldRow.parent
		newRow = self._getChild(table, oldRow.indexInParent + 1)
		self.node = self._getChild(newRow, self.node.indexInParent)
		return self._nodeMovementText()

	def previousRow(self):
		if self.node.tag == "mtr":
			# Move to the first cell in the previous row.
			oldRow = self.node
			colIndex = 0
		elif self.node.tag == "mtd":
			oldRow = self.node.parent
			colIndex = self.node.indexInParent
		else:
			raise LookupError
		table = oldRow.parent
		newRow = self._getChild(table, oldRow.indexInParent - 1)
		self.node = self._getChild(newRow, self.node.indexInParent)
		return self._nodeMovementText()
