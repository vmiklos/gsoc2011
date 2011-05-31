import urllib
import time
from email.Utils import formatdate
from mod_python import apache
from xml.sax import saxutils
import StringIO
import asciidocapi
import random
import pickle

class Parser:
	def __init__(self, rss):
		self.rss = rss
		self.asciidoc = asciidocapi.AsciiDocAPI()
		self.asciidoc.options('--no-header-footer')
		self.rndcache = {}
		try:
			sock = open("rndcache")
			self.rndcache = pickle.load(sock)
			sock.close()
		except IOError:
			pass
		except EOFError:
			pass
	def close(self):
		sock = open("rndcache", "w")
		pickle.dump(self.rndcache, sock)
		sock.close()
	def getline(self, timestamp):
		l = 1
		for i in self.buf.split('\n'):
			if i.startswith("== %s" % timestamp):
				return l
			else:
				l += 1
	def feed(self, buf):
		self.buf = buf
		l = buf.split('\n\n==')
		l.reverse()
		for i in l[:10]:
			timestamp = i.split('\n')[0].strip()
			if timestamp in self.rndcache.keys():
				h, m = self.rndcache[timestamp]
			else:
				h = random.choice(range(17, 19))
				m = random.choice(range(00, 60))
				self.rndcache[timestamp] = (h, m)
			try:
				date = formatdate(time.mktime(time.strptime(timestamp + " %s:%s" % (h, m), "%Y-%m-%d %H:%M")), True)
			except ValueError:
				continue
			entry = "\n".join(i.split('\n')[1:])
			infile = StringIO.StringIO(entry)
			outfile = StringIO.StringIO()
			self.asciidoc.execute(infile, outfile)
			markup = saxutils.escape(outfile.getvalue())
			title = timestamp
			self.rss.additem(title, markup, "http://cgit.freedesktop.org/~vmiklos/lo-gsoc/tree/README?h=refs/heads/diary#n%s" % self.getline(timestamp), date)

class Rss:
	def __init__(self, req, title, link, desc):
		self.req = req
		self.title = title
		self.desc = desc
		self.link = link
		self.items = []
	def additem(self, title, desc, link, pubDate):
		self.items.append([title, desc, link, pubDate])
	def output(self):
		self.req.content_type = 'application/xml'
		self.req.write("""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
<title>%s</title>
<description>%s</description>
<link>%s</link>\n""" % (self.title, self.desc, self.link))
		for title, desc, link, pubDate in self.items:
			self.req.write("""<item>
			<title>%s</title>
			<description>%s</description>
			<link>%s</link>
			<pubDate>%s</pubDate>
			</item>\n""" % (title, desc, link, pubDate))
		self.req.write("</channel>\n</rss>")
		return apache.OK

def handler(req):
	sock = urllib.urlopen("http://cgit.freedesktop.org/~vmiklos/lo-gsoc/plain/README")
	parser = Parser(Rss(req, "GSoC 2011 Diary of Miklos Vajna", "http://cgit.freedesktop.org/~vmiklos/lo-gsoc/tree/README?h=diary", "About improving RTF import."))
	parser.feed(sock.read())
	parser.close()
	sock.close()
	return parser.rss.output()
