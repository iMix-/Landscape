import asyncio
import logging
import json
import io

from .Parsers import XMLParser

class BaseHandler(asyncio.Protocol, object):

	def __init__(self):
		self.logger = logging.getLogger("Landscape")
		
		self.xmlListeners = {
			"verChk": self.handleVersionCheck,
			"rndK": self.handleRandomKey,
			"login": self.handleLogin
		}

	def handleVersionCheck(self, data):
		self.logger.info("Received API version check")

		apiVersion = XMLParser.retrieveApiVersion(data)

		if apiVersion != 153:
			self.send("<msg t='sys'><body action='apiKO' r='0'></body></msg>")
			self.transport.close()
		else:
			self.send("<msg t='sys'><body action='apiOK' r='0'></body></msg>")

	def handleRandomKey(self, data):
		self.logger.info("Received random key request")

	def handleLogin(self, data):
		pass

	def connection_made(self, transport):
		peername = transport.get_extra_info("peername")
		self.logger.info("Connection received from %s", peername)

		self.transport = transport

		self.send("<cross-domain-policy>"
			"<allow-access-from domain='*' to-ports='*' />"
			"</cross-domain-policy>")

	def connection_lost(self, exception):
		if exception != None:
			self.logger.error("Client connection lost: %s", exception.message)
		else:
			self.logger.info("Client disconnected")

	def data_received(self, data):
		message = data.decode().strip("\x00")

		self.logger.debug("Received %s", message)

		if message.startswith("<"):
			if message == "<policy-file-request/>":
				pass # Already sent
			else:
				action = XMLParser.retrieveAction(message)

				if action == None or action not in self.xmlListeners:
					self.transport.close()
				else:
					self.xmlListeners[action](message)

	def send(self, data):
		# Parameter needs to be in byte format
		outgoing = (data + "\x00").encode()

		self.transport.write(outgoing)