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
        if data["action"] == "broadcast_request":
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
                    if j == 2:
                        temp_index = 3
                    elif j == 3:
                        temp_index = 2

                    # Replace client channel which already quited with this string
                    # Why we should do this? To prevent other client which maybe still on matchmaking
                    # and trying to enter this room because we are going to delete this room.
                    self.client_pairs[i][j] = "no_client"

                    # Replace board status
                    self.client_pairs[i][1] = "opponent_disconnected"

                    # Broadcast to other player
                    self.BroadcastGameStatus(self.client_pairs[i][temp_index])

                    # If that was the only client in room, delete this room
                    no_client_counter = 0
                    for iterator in self.client_pairs[i]:
                        if iterator == "no_client":
                            no_client_counter += 1

                    if no_client_counter == 2:
                        del self.client_pairs[i]    # delete room

                    # game_data = self.client_pairs[i]
                    still_checking = 0
                    break

            if still_checking == 0:
                break

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
            # If there are two users in room
            if len(pair) == 4:
                if pair[2] == channel:
                    sender = pair[2]
                    receiver = pair[3]
                    break
                elif pair[3] == channel:
                    sender = pair[3]
                    receiver = pair[2]
                    break

        # Send to other player in room
        if flag == 1:
            receiver.Send(data)
        # Send to both player in room
        elif flag == 2:
            receiver.Send(data)
            sender.Send(data)
        # Send to who made request
        elif flag == 3:
            channel.Send(data)

    def BroadcastGameStatus(self, channel):
        for i in self.client_pairs:
            temp_data = {"action": "broadcast", "status": i[1]}
            # If only one player exists, broadcast to itself alone
            if len(i) == 3:
                # Room: One player, probably still matchmaking
                self.SendToOther(channel, temp_data, flag=3)
            # If other player exists, broadcast to both players in room
            elif len(i) == 4:
                # Room: Two players, probably in a game session
                # or maybe it's actually a "no_client" string?!
                # Well, it will be checked in SendToOther method
                # So let's be positive and use flag = 2
                self.SendToOther(channel, temp_data, flag=2)

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