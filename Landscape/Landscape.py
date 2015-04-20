import json, io, asyncio, logging
from .LoginHandler import LoginHandler
# from .GameHandler import GameHandler

class Landscape(object):

	def __init__(self, server):
		config = self.getServerDetails(server)

		for attribute in config:
			setattr(self, attribute.lower(), config[attribute])

		self.logger = logging.getLogger("Landscape")

		self.logger.info("Starting server on %s:%d", self.address, self.port)

	def start(self):
		loop = asyncio.get_event_loop()
		
		if self.type == "login":
			protocol = LoginHandler
		else:
			protocol = GameHandler
			
		coro = loop.create_server(protocol, self.address, self.port)
		server = loop.run_until_complete(coro)

		try:
			loop.run_forever()
		except KeyboardInterrupt:
			self.logger.info("Stopping server")
		finally:
			server.close()
			loop.run_until_complete(server.wait_closed())
			loop.close()

	def getServerDetails(self, server):
		data = None

		with open("Config.json", "r") as configuration:
			data = configuration.read().replace("\n", "")
			config = json.loads(data)

			return config[server]