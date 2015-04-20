import xml.etree.ElementTree as ET

class XMLParser(object):

	@staticmethod
	def retrieveBodyElement(data):
		try:
			root = ET.fromstring(data)
			bodyElement = root.find(".//body")

			return bodyElement

		except:
			return None

	@staticmethod
	def retrieveAction(data):
		bodyElement = XMLParser.retrieveBodyElement(data)

		if bodyElement == None:
			return None

		actionAttribute = bodyElement.attrib["action"]

		return actionAttribute

	@staticmethod
	def retrieveApiVersion(versionCheck):
		bodyElement = XMLParser.retrieveBodyElement(versionCheck)

		try:
			apiVersion = bodyElement.find("ver").attrib["v"]

			return int(apiVersion)
			
		except:
			return None