from PyQt5.QtWidgets import QPushButton, QLabel, QApplication, QWidget, QGridLayout, QTextEdit, QDesktopWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer, QCoreApplication
from time import sleep
import os, sys
import signal

app = QApplication([])
stdFont = QFont('Arial', 24)
consFont = QFont("Helvetica [Cronyx]", 16) #, QFont.Bold)
buttStyleSheet = "border-radius : 8; border : 3px solid darkgrey"
app.setStyleSheet("QPushButton { background-color: grey } ")
app.setStyleSheet("QPushButton:pressed { background-color: lightgrey } ")

class sockRx(QObject):	# Step 1: Create a worker class
	finished = pyqtSignal()
	progress = pyqtSignal(int)
	infinity = True
	def tcpRxFn(self):
		from tcpSrv import tcpsrv
		srv = tcpsrv()
		# srv.setupListener("192.168.1.1", 10000, consTcp, True)
		srv.setupListener("", 10000, consTcp, True)
		stateTcpIsOff()
		stateTcpIsOn()
		srv.runListener()

		self.progress.emit(n + 1)
		self.finished.emit()

	def wifiRxFn(self):
		n = 0
		sleep(0.5)
		DEBUG("wifi thread started")
		while( self.infinity ):
			sleep(0.5)
			wifiStatus = readWifiStatus()
			if(False == wifiStatus):
				stateWifiIsOff()
			if(True == wifiStatus):
				stateWifiIsOn()
			DEBUG("wifi thread active")
			# self.progress.emit(n + 1)
		DEBUG("wifi thread ending ")
		self.finished.emit()
		DEBUG("wifi thread endedet ")

	def exitAll(self):
		DEBUG("exiting threads, ")
		self.infinity = False

tcpThread = QThread()							# Step 3: Create a QThread
tcpRx = sockRx()								# Step 3: Create a tcpRx object
tcpRx.moveToThread(tcpThread)					# Step 4: Move tcpRx to the tcpThread
tcpThread.started.connect(tcpRx.tcpRxFn)		# Step 5: Connect signals and slots
tcpThread.finished.connect(tcpThread.deleteLater)
tcpRx.finished.connect(tcpRx.deleteLater)
tcpRx.finished.connect(tcpThread.quit)
# tcpRx.progress.connect(reportProgress)
tcpThread.start()								# Step 6: Start the tcpThread

wifiThread = QThread()
wifiRx = sockRx()								# Step 3: Create a wifiRx object
wifiRx.moveToThread(wifiThread)					# Step 4: Move wifiRx to the wifiThread
wifiThread.started.connect(wifiRx.wifiRxFn)		# Step 5: Connect signals and slots
wifiThread.finished.connect(wifiThread.deleteLater)
wifiRx.finished.connect(wifiRx.deleteLater)
wifiRx.finished.connect(wifiThread.quit)
# wifiRx.progress.connect(reportProgress)
wifiThread.start()								# Step 6: Start the wifiThread
# wifiRx.exitAll()

def buttStartWifiFn():
	resp = os.popen("sudo systemctl start hostapd").read()
	print("start WiFi: ", resp)

def buttStopWifiFn():
	resp = os.popen("sudo systemctl stop hostapd").read()
	print("stop WiFi: ", resp)

def readWifiStatus():
	resp = os.popen("sudo systemctl status hostapd").read().split('\n')[2]
	if "Active: active (running)" in resp:
		return True
	if "Active: inactive (dead)" in resp:
		return False
	else:
		return None

def buttStartTcpFn(): pass
def buttStopTcpFn(): pass

def buttExitFn():
	# QCoreApplication.instance().quit()
	DEBUG("stopping threads")
	wifiRx.exitAll()
	sleep(0.1)
	DEBUG("wating thraeds")
	# wifiThread.wait()
	print("over and out")
	# sys.exit()
	# app.exit()
	exit()



def DEBUG(text):
	# print(text, flush = True)
	pass

def stateWifiIsOn():
	stateWifi.setStyleSheet("color: green;")
	stateWifi.setText("Wifi is on")

def stateWifiIsOff():
	stateWifi.setStyleSheet("color: darkred;")
	stateWifi.setText("Wifi is off")

def stateTcpIsOn():
	stateTcp.setStyleSheet("color: green;")
	stateTcp.setText("Tcp is on")

def stateTcpIsOff():
	stateTcp.setStyleSheet("color: darkred;")
	stateTcp.setText("Tcp is off")


# buttons
buttStartWifi = QPushButton( '\nstart Wifi\n'  , font = stdFont, styleSheet = buttStyleSheet)
buttStopWifi = QPushButton('\nstop WiFi\n', font = stdFont, styleSheet = buttStyleSheet)
buttStartTcp = QPushButton('\nstart Tcp\n', font = stdFont, styleSheet = buttStyleSheet)
buttStopTcp = QPushButton('\nstop Tcp\n', font = stdFont, styleSheet = buttStyleSheet)

buttExit = QPushButton('\nEXIT\n', font = stdFont, styleSheet = buttStyleSheet)

# buttExit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
buttStartWifi.clicked.connect(buttStartWifiFn)
buttStopWifi.clicked.connect(buttStopWifiFn)
buttStartTcp.clicked.connect(buttStartTcpFn)
buttStopTcp.clicked.connect(buttStopTcpFn)
buttExit.clicked.connect(buttExitFn)

labelWifi = QLabel('Start / Stop SOCKBase0', font = stdFont, alignment = Qt.AlignmentFlag.AlignCenter)
labelTcp =  QLabel('TCP RX on port ... ', font = stdFont, alignment = Qt.AlignmentFlag.AlignCenter)

stateWifi = QLabel("", font = stdFont, alignment = Qt.AlignmentFlag.AlignCenter)
stateWifiIsOff()
stateTcp = QLabel("", font = stdFont, alignment = Qt.AlignmentFlag.AlignCenter)
stateTcpIsOff()

consTcp = QTextEdit(readOnly=True, styleSheet = "border : 3px solid darkgrey", font = consFont)


win = QWidget()

layout = QGridLayout()

layout.addWidget(labelWifi, 0, 0)
layout.addWidget(labelTcp, 0, 1)


layout.addWidget(buttStartWifi, 1, 0)
layout.addWidget(buttStartTcp, 1, 1)


layout.addWidget(buttStopWifi, 2, 0)
layout.addWidget(buttStopTcp, 2, 1)


layout.addWidget(stateWifi, 3, 0)
layout.addWidget(stateTcp, 3, 1)

layout.addWidget(consTcp, 4, 1)

layout.addWidget(buttExit, 5, 0)

# buttStopWifi.resize(  100, -1)

monitor = QDesktopWidget().screenGeometry(1)
win.move(monitor.left(), monitor.top())
win.setLayout(layout)

signal.signal(signal.SIGINT, signal.SIG_DFL)	# makes program closeable via Ctrl+C

# win.showFullScreen()
win.showMaximized()
# win.show()

'''
DEBUG(buttExit.height())
DEBUG(buttStopWifi.height())
buttExit.resize( buttExit.width(), int(1.5*buttExit.height()) )
DEBUG(buttExit.height())
'''

# app.exec(  )
import sys
sys.exit(app.exec())
