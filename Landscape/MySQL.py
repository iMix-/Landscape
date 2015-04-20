import mysql.connector
import Output

class MySQL:
	con = None
	mysql = None	
	host = None
	username = None
	password = None
	database = None
	
	def __init__(self, host, username, password, database):
		self.host = host
		self.username = username
		self.password = password
		self.database = database
		self.CreateConnection()
		
		
	def CreateConnection(self):
		try:
			self.con = mysql.connector.Connect(host = self.host, user = self.username, password = self.password, database = self.database)
			self.mysql = self.con.cursor(dictionary=True)
			Output.Write("Connected to MySQL server", "success")
		except mysql.connector.Error:
			Output.Write("Connection to MySQL server has failed", "error")
		
	def Insert(self, table, columns, values):
		Query = "INSERT INTO " + table
		Query += ' (' + ', '.join(columns) + ')'
		Query += " VALUES("
		c = 0
		for value in values:
			if c != len(values) -1: 
				Query += "'" + value + "', "
			else:
				Query += "'" + value + "'"
			c += 1
		Query += ")"
		self.Execute(Query)
	
	def Select(self, table, columns, where = None):
		Query = "SELECT "
		Query += ', '.join(columns)
		Query += ' FROM ' + table
		Query += ' WHERE ' + where
		self.Execute(Query)
		s = self.mysql.fetchall()
		return s
		
	def GetUserDataByUsername(self, columns, username):
		Query = "SELECT "
		Query += ', '.join(columns)
		Query += ' FROM users'
		Query += ' WHERE username = \'' + username + '\''
		self.Execute(Query)
		s = self.mysql.fetchone()
		return s

	def GetUserDataByID(self, columns, ID):
		Query = "SELECT "
		Query += ', '.join(columns)
		Query += ' FROM users'
		Query += ' WHERE ID = \'' + str(ID) + '\''
		self.Execute(Query)
		s = self.mysql.fetchone()
		return s
		
	def UpdateColumnByID(self, column, newVal, ID):
		Query = "UPDATE `users` SET `" + column + "` = '" + newVal + "' WHERE `ID` = '" + str(ID) + "'"
		self.Execute(Query)
		self.con.commit()
	
	def UpdateColumnByUsername(self, column, newVal, Username):
		Query = "UPDATE `users` SET `" + column + "` = '" + newVal + "' WHERE `Username` = '" + Username + "'"
		self.Execute(Query)
		self.con.commit()
	
	def Execute(self, query):
		self.mysql.execute(query)
