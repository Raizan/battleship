__author__ = "Reisuke"

from PodSixNet.Connection import connection, ConnectionListener
from ConfigParser import SafeConfigParser


class Client(ConnectionListener):

    def __init__(self):
        # Reading configuration file for server settings
        parser = SafeConfigParser()
        parser.read('network.conf')

        # Define port and server address
        server_address = parser.get('game_server', 'server_address')
        port = parser.get('game_server', 'port')
        port = int(port)

        self.Connect((server_address, port))
        self.temp_data = None
        # self.running = 1

    def Loop(self):
        connection.Pump()
        self.Pump()

    def PassData(self):
        return self.temp_data

    # Network get data only on Network
    def Network(self, data):
        self.temp_data = data

