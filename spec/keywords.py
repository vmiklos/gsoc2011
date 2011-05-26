from xml.sax.handler import ContentHandler
from xml.sax import make_parser

import sys
sys = reload(sys)
sys.setdefaultencoding("utf-8")

class Handler(ContentHandler):
	def __init__(self):
		self.seenfirsttable = False
		self.intable = False
		self.intext = False
		self.inpara = False
		self.ignorenexttext = False
		self.inppr = False
		self.texts = []
		self.result = []

	def startElement(self, name, attributes):
		if name == "w:tbl":
			if not self.seenfirsttable:
				self.seenfirsttable = True
			else:
				self.intable = True
		elif name == "w:t" and self.intable:
			if self.ignorenexttext:
				self.ignorenexttext = False
			else:
				self.intext = True
		elif (not self.inppr) and ((name == "w:vertAlign" and attributes['w:val'] == 'superscript') or (name == "w:i")):
			self.ignorenexttext = True
		elif name == "w:p":
			self.inpara = True
		elif name == "w:pPr":
			self.inppr = True

	def endElement(self, name):
		if name == "w:tbl":
			self.intable = False
		elif name == "w:t":
			self.intext = False
		elif name == "w:pPr":
			self.inppr = False
		elif name == "w:p":
			text = "".join(self.texts).strip()
			if len(text):
				self.result.append(text)
			self.texts = []

	def characters(self, data):
		if self.intext:
			self.texts.append(data)

parser = make_parser()
handler = Handler()
parser.setContentHandler(handler)
parser.feed(open("keywords.xml").read())
parser.close()

c = 3 # ignore first line
while c < len(handler.result):
	name = handler.result[c]
	c += 1
	where = handler.result[c]
	c += 1
	t = handler.result[c].replace(' (obsolete)', '')
	if t == "Destination and Value":
		print >>sys.stderr, "Warning, changing 'Destination and Value' to 'Destination' for '%s'" % name
		t = "Destination"
	if not name.startswith("\\"):
		raise Exception("invalid name '%s'" % name)
	# drop leading \, replace \ with \\
	name = name[1:].replace("\x5c", "\x5c\x5c")
	if (t not in ("Flag", "Destination", "Symbol", "Toggle", "Value")):
		raise Exception("invalid type '%s' for '%s'" % (t, name))
	t = {
		'Flag': 'CONTROL_FLAG',
		'Destination': 'CONTROL_DESTINATION',
		'Symbol': 'CONTROL_SYMBOL',
		'Toggle': 'CONTROL_TOGGLE',
		'Value': 'CONTROL_VALUE'
		}[t]
	c += 1
	print '{"%s", %s},' % (name, t)
