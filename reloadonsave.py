import gedit
import telnetlib

class ReloadOnSave(gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
		self.connect()
	
	def activate(self, window):
		window.connect("tab-added", self.tab_added)

	def connect(self):
		try:
			self.conn = telnetlib.Telnet('localhost', 4242, 10)
			self.connected = True
			print 'Reloadonsave.py: Connected to telnet host localhost:4242'
		except:
			# Either no telnet client, or firefox plugin not running
			print "Open firefox	and go to Tools -> MozRepl -> Start"
			self.connected = False
		
	def tab_added(self, window, tab):
		doc = tab.get_document()
		doc.connect("saved", self.send_command)

	def send_command(self, document, dk):
		if not self.connected:
			self.connect()
		repl = '''
		y = content.window.pageYOffset;
		x = content.window.pageXOffset;
		content.window.location.reload();
		content.scrollTo(x,y);
		''' 
		self.conn.write(repl)

