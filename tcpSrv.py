# -*- coding: utf-8 -*-
"""
Created on 20.08.2024
@author: Hinterleitner
"""
import socket, errno
from PyQt5.QtGui import QTextCursor

# for testing: nc 192.168.1.1 10000

class tcpsrv:
	clientPre = "[CLIENT] "
	infoPre = "[INFO] "
	logFn = "tcpSrv.log"
	echo = True
	cons = []
	s = []
	feil = []
	# TCP_IP = ""
	# TCP_IP = "192.168.1.1"
	# TCP_PORT = 10000
	# TCP_PORT = 80


	def __init__(self):
		pass
		self.feil = open(self.logFn, "a")
		# self.TCP_IP = ""
		# self.TCP_PORT = 10000

	def _prepend(self, text, console):
		# set the cursor position to 0
		if(console):
			cursor = QTextCursor(console.document())
			# set the cursor position (defaults to 0 so this is redundant)
			cursor.setPosition(0)
			console.setTextCursor(cursor)
			# insert text at the cursor
			console.insertPlainText(text + '\n')


	def _printSrv(self, msg):
		self._prepend(msg, self.cons)
		with open(self.logFn, "a") as feil:
			feil.write(msg + '\n')
		print(msg, flush = True)

	def _processRxData(self, client, data):
			rxMsg = str(data.decode("utf-8")).strip()
			ip = client[0]
			port = str(client[1])
			reportMsg = self.clientPre + ip + "/" + port + ": " + rxMsg
			self._printSrv(reportMsg)

	def setupListener(self, IP, port, console, echo):
			self.cons = console
			self.echo = echo
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.bind((IP, port))
			# return s

	def _startListener(self, sock):
			sock.listen(1)

	def runListener(self):
		try:

				BUFFER_SIZE = 1024*2
				self._startListener(self.s)
				infinity = True
				while(infinity):
						conn, addr = self.s.accept()
						self._printSrv(self.infoPre + "client address: " + str(addr))
						clientConn = True
						try:
								while(clientConn):
										data = conn.recv(BUFFER_SIZE)
										if not data:
												clientConn = False
												self._printSrv(self.infoPre + "client gone gracefully")
										else:
												self._processRxData(addr, data)
												if(self.echo):
													conn.sendall(data)	  # echo data
								conn.close()

						except socket.error as e:
								if e.errno != errno.ECONNRESET:
										raise # Not error we are looking for
								self._printSrv(self.infoPre + "client gone wild")
								pass # Handle error here.
						finally:
								conn.close()

		except KeyboardInterrupt:
				self._printSrv("\nCtrl+C irq")
				pass

		self._printSrv( self.infoPre + "server out")

	# useage
	# s = setupListener(TCP_IP, TCP_PORT, cons, echo)
	# runListener() ... blocking
