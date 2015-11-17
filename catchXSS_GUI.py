from PyQt4 import QtGui, QtCore, QtWebKit
import urllib2, sys, random, time
from threading import Thread
from bs4 import BeautifulSoup

# to the next version, first make a craw of the website, store all urls and inject it the javascript xD
class Crawler():
	
	def __init__(self, url):
	
		self.url= url
		self.urlFirst= url
		self.urlsFound=[url]
		self.checked=[url]
		
	def running(self):
		while self.urlsFound != []:
			self.crawling()
		
	def catchCode(self, url):

		try:
			self.url= url
			req=urllib2.Request(url)
			self.htmlcode=urllib2.urlopen(req)
			self.htmlCode=self.htmlcode.read()
		except Exception, e:
			if "HTTP Error" in str(e):
				pass
			else:
				pass
#			print e
			#print "Self urls: "+str(self.urlsFound)
			
			
	def crawling(self):
		
		for web in self.urlsFound:
			self.urlsFound.remove(web)
			if not "http://" in web:
				web= self.urlFirst+"/"+web
			print "[*] Crawling url: "+str(web)
			self.catchCode(web)
		sopa=BeautifulSoup(self.htmlCode)
		for tag in sopa.findAll("a", href=True):
				if tag["href"] in self.urlsFound:
					pass
				elif tag["href"] == "#":
					pass
				elif tag["href"] not in self.urlsFound:
					self.urlsFound.append(tag["href"])
		self.showCrawling()
	def showCrawling(self):
	
	#	print "[SELF URLS] "+str(self.tocheck)	
		for foundUrl in self.urlsFound:
			self.urlsFound.remove(foundUrl)
			if not "http://" in foundUrl:
				foundUrl = self.urlFirst+"/"+foundUrl
			if foundUrl not in self.checked:
				self.checked.append(foundUrl)
			else:
				#print "[!!] Not copied to self.checked"
				pass
				
			print " [-] Url: "+foundUrl
			

class Quest(QtGui.QWidget):

	def __init__(self):
		
		QtGui.QWidget.__init__(self)
		self.web= ""
		self.payload= ""
		self.setWindowTitle("Enter a website and a payload to inject it")
		self.setGeometry(200, 400, 500, 200)
		self.setWindowIcon(QtGui.QIcon("inj.png"))
		labelWeb= QtGui.QLabel("Enter a web: ", self)
		self.lineWeb= QtGui.QLineEdit(self)
		labelPayload= QtGui.QLabel("Enter a payload: ", self)
		self.linePayload= QtGui.QLineEdit(self)
		buttonOk= QtGui.QPushButton("Inject", self)
		buttonOk.setStyleSheet("border: 1px solid white;")
		buttonOk.clicked.connect(self.catchData)
		self.connect(self.linePayload, QtCore.SIGNAL("returnPressed()"), self.catchData)
		buttonOk.resize(200, 30)
		grid= QtGui.QGridLayout()
		grid.addWidget(labelWeb, 0, 0)
		grid.addWidget(self.lineWeb, 0, 1)
		grid.addWidget(labelPayload, 1, 0)
		grid.addWidget(self.linePayload, 1, 1)
		grid.addWidget(buttonOk, 2, 1)
		self.setLayout(grid)
		self.setStyleSheet("background-color: black; color: white; ")
		
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.close()
			
			
	def catchData(self):
		
		web= str(self.lineWeb.text())
		payload= str(self.linePayload.text())
		self.hide()
		if web == "" and payload == "":
			window.lineStatus.setText(" You must input a web and a payload to use")
		else:
			browser.show()
			browser.loadPage(web, payload)
			self.close()
		
		
class Browser(QtGui.QMainWindow):

		def __init__(self):
			
			QtGui.QMainWindow.__init__(self)
			self.setWindowTitle("Browser injector")
			self.setWindowIcon(QtGui.QIcon("inj.png"))
			self.resize(900, 600)
			#self.mainLayout= QtGui.QHBoxLayout(self.centralWidget)
		#	self.mainLayout.setSpacing(0)
			#self.mainLayout.setMargin(1)
			#self.frame= QtGui.QFrame(self.centralWidget)
			#self.gridLayout= QtGui.QVBoxLayout(self.frame)
			#self.gridLayout.setMargin(0)
			#self.gridLayout.setSpacing(0)
			self.html= QtWebKit.QWebView()
			self.setCentralWidget(self.html)
			#self.gridLayout.addWidget(self.html)
			
		def loadPage(self, web, payload):
		
			self.web= web
			self.payload= payload
			self.html.load(QtCore.QUrl(web+payload))
			self.html.show()
			
		def keyPressEvent(self, e):
		
			if e.key() == QtCore.Qt.Key_Escape:
				self.close()
				
				
class About(QtGui.QWidget):

	def __init__(self):
	
		QtGui.QWidget.__init__(self)
		labelAbout= QtGui.QLabel("[!] coder: mentefria", self)
		labelName= QtGui.QLabel("[!] XSS Finder GUI v 0.1", self)
		labelDesc= QtGui.QLabel("[!] A simple finder XSS GUI", self)
		labelLicense= QtGui.QLabel("Copyright @ Created at 06-03-2015", self)
		buttonOK= QtGui.QPushButton("Aceptar", self)
		buttonOK.clicked.connect(self.cerrar)
		buttonOK.setStyleSheet("border: 1 px solid white;")
		grid= QtGui.QGridLayout()
		grid.addWidget(labelName, 1, 0)
		grid.addWidget(labelDesc, 2, 0)
		grid.addWidget(labelLicense, 4, 0)
		grid.addWidget(labelAbout, 3, 0)
		grid.addWidget(buttonOK, 5, 0)
		self.setLayout(grid)
		self.setWindowTitle("About... ")
		self.setGeometry(400, 300, 200, 200)
		self.setFixedSize(200, 200)
		self.setWindowIcon(QtGui.QIcon("info.png"))
		self.setStyleSheet("background-color:black; color: white;")
		
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.close()
			
	def cerrar(self):
		
		self.close()
		
		
class Ventana(QtGui.QMainWindow):

	def __init__(self):
	
		# Window
		QtGui.QMainWindow.__init__(self)
		self.setGeometry(200, 200, 600, 460)
		self.setFixedSize(590,460)
		iconGUI= QtGui.QIcon("scan.png")
		self.setWindowIcon(iconGUI)
		self.setWindowTitle("simple XSS Finder v0.1 ")
		self.URLS= []	
		# Content
		labelIntro= QtGui.QLabel("[!] XSS Finder ", self)
		labelDork= QtGui.QLabel("Dork: http://example.org/task/Rule?query=", self)
		labelUrl= QtGui.QLabel("Enter url: ", self)
		#labelListaUrls= QtGui.QLabel("Lista Urls: ", self)
		self.lineaUrl= QtGui.QLineEdit(self)
		#buttonListaUrls= QtGui.QPushButton("Buscar lista", self)
		#buttonListaUrls.clicked.connect()
		self.listProofs= QtGui.QListWidget(self)
		#self.listProofs.addItem("will be the payloads... ")
		self.listUrl= QtGui.QListWidget(self)
		self.listUrl.addItem("Will be the urls...")
		labelStatus= QtGui.QLabel("[+] Status: ", self)
		self.lineStatus= QtGui.QLabel("", self)
		# setting up CSS
		self.setStyleSheet(" background-color: black;")
		labelIntro.setStyleSheet("color: white;")
		labelDork.setStyleSheet("color: red;")
		labelUrl.setStyleSheet("color: white;")
		self.lineaUrl.setStyleSheet("color: white; border: 1px solid white;")
		self.listProofs.setStyleSheet("background-color: grey; color: black;")
		self.listUrl.setStyleSheet("background-color: grey; color: black;")
		labelStatus.setStyleSheet("color: white;")
		self.lineStatus.setStyleSheet("color: red;")
		# Positioning and resize
		labelIntro.resize(200, 20)
		labelIntro.move(240, 80)
		labelDork.resize(350, 20)
		labelDork.move(150, 110)
		labelUrl.resize(450, 20)
		labelUrl.move(40, 130)
		self.lineaUrl.resize(400, 25)
		self.lineaUrl.move(110, 130)
		self.listProofs.move(40, 160)
		self.listProofs.resize(520, 50)
		self.listUrl.move(40, 220)
		self.listUrl.resize(520, 200)
		labelStatus.resize(200, 20)
		labelStatus.move(40, 430)
		self.lineStatus.resize(500, 20)
		self.lineStatus.move(100, 430)
		
		# Adding a toolbar
		toolbar= QtGui.QToolBar(self)
		toolbar.setIconSize(QtCore.QSize(140, 50))
		toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		toolbar.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)
		
		function= QtGui.QAction(QtGui.QIcon("scan.png"), "Search vulnerable pages", self)
		function1= QtGui.QAction(QtGui.QIcon("browser.png"), "Exploit with browser", self)
		function2= QtGui.QAction(QtGui.QIcon("url.ico"), "Add a URL list (.txt)", self)
		function3= QtGui.QAction(QtGui.QIcon("info.png"), "About", self)
		
		function.triggered.connect(self.inject)
		function1.triggered.connect(self.browExploit)
		function2.triggered.connect(self.catchList)
		function3.triggered.connect(self.aboutUs)
			
		toolbar.addAction(function)
		toolbar.addAction(function1)
		toolbar.addAction(function2)
		toolbar.addAction(function3)
		
		toolbar.setFixedSize(600, 75)
		toolbar.setFloatable(False)
		toolbar.setMovable(False)
		toolbar.setStyleSheet("color: white; border: 0.5px solid grey;")
		self.catchingPayloads()
		
	def keyPressEvent(self, e):
	
		if e.key() == QtCore.Qt.Key_Escape:
			self.close()
					
	
	def catchingPayloads(self):
		
		try:
			listaFilenames=  ["pt.txt","pnt.txt","po.txt"] # "pneg.txt", , "pmail.txt"
			self.payload_list=[]
			trash= ""
			for fail in listaFilenames:
				randomize= random.choice(range(len(listaFilenames)))
				fail= listaFilenames[randomize]
				trash += listaFilenames.pop(randomize)
				f=open(fail, "r")
				payloads = f.read()
				f.close()
				payloadss= payloads.split("\n")
				for payload in payloadss:
					if payload == "":
						pass
					else:
						self.payload_list.append(payload)
			self.listProofs.addItem(self.payload_list[0])
			self.lineStatus.setText(" Payloads loaded succesfully")
		except Exception, e:
			self.lineStatus.setText(" Error catching Payloads; Description: "+str(e))
	
	def showPayload(self):
		
		self.catchingPayloads()
		self.listProofs.clear()
		try:
			for payload in self.payload_list:
				if payload == "":
					pass
				else:
					self.listProofs.addItem(payload)
		except Exception, e:
			self.lineStatus.setText(" Error showing payloads; Description: "+str(e))
		
	
	def inject(self):
		
		try:
			self.catchUrl()
		except Exception, e:
			self.lineStatus.setText(" Error catching URL; Description: "+str(e))
		try:
			self.lineStatus.setText(" Crawling url...")
			#	url="http://restaurantbalear.260mb.net"	
			##	threadCraw= Thread(target=crawling.running)
			#	threadCraw.start()
			for url in self.URLS:
				crawling= Crawler(url)
				#threadCraw= Thread(target=crawling.running)
				#threadCraw.start()
				crawling.running()
				for url in crawling.checked:
					self.URLS.append(url)
				self.lineStatus.setText(" First testing against HTML Injection")
				time.sleep(1)
				t= testingHTMLInject(url)
				if t == True:
					self.lineStatus.setText(" Vulnerable to HTML Injection")
				elif t == False:
					self.lineStatus.setText(" Not Vulnerable to HTML Injection")
				found = False
				self.listProofs.clear()
				self.listProofs.addItem(" Payloads using: ")
				for payload in self.payload_list:
					if found == True:
						break
					if not found:
						website= (url+payload)
						self.listProofs.addItem(website)
						time.sleep(1)
						found= testSearchXSS(url, payload)
						#self.tinject= threadInject(web, payload)
						#self.tinject.start()
						if found == True:
							self.listUrl.clear()
							item= QtGui.QListWidgetItem((url+payload), self.listUrl)
							#colorFound= QtCore.Qt.green
							colorfound= QtGui.QColor(0,  160,0)
							item.setBackground(colorfound)
							self.URLS.remove(url)						
						elif found == "error":
							self.lineStatus.setText(" Enter a valid URL") #Error connecting with: "+url)
							found = True
						else:
							item= QtGui.QListWidgetItem((url+payload), self.listUrl)
							colorfound= QtGui.QColor(0, 0, 0)
							item.setBackground(colorfound)
				#t= Thread(target=testSearchXSS, args=(url, payload))
				#t.start()
				#self.testSearchXSS()
				#t= Thread(target=self.testSearchXSS)
				#t.setDaemon(True)
				#t.start()
		except Exception, e:
			self.lineStatus.setText(" Error threading; Description: "+str(e))
			
			
	def browExploit(self):
		
		quest.show()
		
		
	def catchUrl(self):
		
		url= str(self.lineaUrl.text())
		if not url:
			self.lineStatus.setText(" You must input a website ")
		else:
			self.URLS.append(url)
			self.lineStatus.setText(" URL cached succesfully")
			self.lineaUrl.setText("")
	
	def savingUrls(self):
	
		try:
			for url in self.urls:
				self.URLS.append(url)
			self.lineStatus.setText(" URLS to be injected saved succesfully")
		except:
			self.lineStatus.setText(" URLS to be injected NOT founded")
			
			
	def catchList(self):
		
		fi = QtGui.QFileDialog.getOpenFileName(self, 'Buscar Archivo', '')
		try:
			f=open(fi, "r")
			todo=f.readlines()
			f.close()
			self.lineStatus.setText(" URLS text file catched succesfully")
		except:
			pass
		try:
			self.urls= todo.split("\n")
		except Exception, e:
			pass
			
	def aboutUs(self):
		
		about.show()

	
def testingHTMLInject(web):
		
	try:
		payload= "<h1>hello Im There</h1>"
		url= web+'">'+payload
		req= urllib2.Request(url)
		page= urllib2.urlopen(req)
		code= page.read()
		if payload in code:
			return True
		else:
			return False
	except Exception, e:
		print " Error Html Injection; Description: "+str(e)
		
		
def testSearchXSS( web, payload):
	try:
		
		url= web+payload
		req= urllib2.Request(url)
		page= urllib2.urlopen(req)
		code= page.read()
		if payload in code:
			return True
		else:
			pass
	except Exception, e:
			if "400" in str(e):
				pass
			elif "nonnumeric port" in str(e) or "urlopen error" in str(e):
				return "error"
				exit(0)
			else:
				print "[-] Error\n testSearchXSS[!] Description: "+str(e)

	
app= QtGui.QApplication(sys.argv)
window= Ventana()
about= About()
browser= Browser()
quest= Quest()
window.show()
sys.exit(app.exec_())
