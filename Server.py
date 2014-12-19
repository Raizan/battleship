__author__ = "Reisuke"

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep
from weakref import WeakKeyDictionary
from ConfigParser import SafeConfigParser


class ServerChannel(Channel):

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        print "close"
        self._server.DeleteClient(self)

    def PassOn(self, data):
        print "PassOn", data
        if data["action": "broadcast_request"]:
            self._server.BroadcastGameStatus(self)

        elif data["action"] == "quit":
            self._server.DeleteClient(self)
            self.Close()

        elif data["action"] == "attack":
            self._server.SendToOther(self, data)

    # Get data here
    def Network(self, data):
        self.PassOn(data)


class GameServer(Server):

    channelClass = ServerChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.clients = WeakKeyDictionary()
        self.client_pairs = []  # [board, status, player1, player2]
        print 'Server launched'

    def Connected(self, channel, addr):
        print "new connection: ", channel
        print "New Player" + str(channel.addr)
        self.clients[channel] = True
        self.Matchmaking(channel)
        temp_data = {"action": "matchmaking"}
        channel.Send(temp_data)
        print self.client_pairs

    def GetRoomData(self, channel):
        game_data = None
        still_checking = 1
        for i in self.client_pairs:
            for j in range(len(self.client_pairs)):
                if i[j] is channel:
                    game_data = i
                    still_checking = 0
                    break
            if still_checking == 0:
                break

        return game_data

    def DeleteClient(self, channel):
        print "Deleting", channel
        still_checking = 1

        for i in range(len(self.client_pairs)):
            for j in range(len(self.client_pairs[i])):
                if self.client_pairs[i][j] is channel:
                    self.client_pairs[i][j] = "no_client"
                    self.client_pairs[i][1] = "opponent_disconnected"
                    game_data = self.client_pairs[i]
                    still_checking = 0
                    break
            if still_checking == 0:
                break

        # temp = {"action": "receive", "game_data": game_data}
        # self.SendToOther(self, temp)
        del self.clients[channel]

    def Matchmaking(self, channel):
        board = [[0 for x in range(20)] for y in range(10)]
        status = "find_match"
        if len(self.client_pairs) == 0:
            self.client_pairs.append([board, status, channel])
        else:
            no_pair = 1
            for pair in self.client_pairs:
                if len(pair) == 3:
                    pair.append(channel)
                    pair[1] = "deploy_phase"
                    no_pair = 0

            if no_pair == 1:
                self.client_pairs.append([board, status, channel])

    def SendToOther(self, channel, data, flag=1):
        print "SendToOther", data
        for pair in self.client_pairs:
            if pair[2] == channel:
                sender = pair[2]
                receiver = pair[3]
                break
            elif pair[3] == channel:
                sender = pair[3]
                receiver = pair[2]
                break
        if flag == 1:
            receiver.Send(data)
        elif flag == 2:
            receiver.Send(data)
            sender.Send(data)

    def BroadcastGameStatus(self, channel):
        for i in self.client_pairs:
            temp_data = {"action": "broadcast", "status": i[1]}
            # If only one player exists
            if len(i) == 3:
                print "One player"
                self.SendToOther(channel, temp_data)
            # If other player exists
            elif len(i) == 4:
                print "Two players"
                self.SendToOther(channel, temp_data, flag=2)

    # find socket location on client_pairs
    def FindClientPair(self):
        pass

    def Loop(self):
        while True:
            self.Pump()
            sleep(0.0001)

if __name__ == "__main__":
    # Reading configuration file for server settings
    parser = SafeConfigParser()
    parser.read('network.conf')

    # Define port and server address
    server_address = parser.get('game_server', 'server_address')
    port = parser.get('game_server', 'port')
    port = int(port)

    battleship_server = GameServer(localaddr=(server_address, port))
    battleship_server.Loop()