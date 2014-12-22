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
        # print "PassOn", data
        if data["action"] == "broadcast_request":
            self._server.BroadcastGameStatus(self)

        elif data["action"] == "quit":
            self.Close()

        elif data["action"] == "attack":
            self._server.SendToOther(self, data)

        elif data["action"] == "ready":
            self._server.InitBoard(self, data)

    # Get data here
    def Network(self, data):
        self.PassOn(data)


class GameServer(Server):

    channelClass = ServerChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.clients = WeakKeyDictionary()
        # [[room_full_flag, ready_state], [board, board], status, player1, player2] room_full_flag=1 means room is full
        self.client_pairs = []
        print 'Server launched'

    def Connected(self, channel, addr):
        print "new connection: ", channel
        print "New Player" + str(channel.addr)
        self.clients[channel] = True
        self.Matchmaking(channel)
        temp_data = {"action": "matchmaking"}
        channel.Send(temp_data)
        # print self.client_pairs

    # Client and room deletion management
    def DeleteClient(self, channel):
        print "Deleting", channel
        still_checking = 1

        for i in range(len(self.client_pairs)):
            for j in range(len(self.client_pairs[i])):
                if self.client_pairs[i][j] == channel:
                    # Replace board status
                    self.client_pairs[i][2] = "opponent_disconnected"
                    # If room is on full state, make sure there's another client there
                    # Broadcast to other player
                    if self.client_pairs[i][0][0] == 1 and len(self.client_pairs[i]) == 5:
                        # If index = 2, then index = 3 is the other client
                        if j == 3:
                            self.BroadcastGameStatus(self.client_pairs[i][4])
                        # If index = 3, then index = 2 is the other client
                        elif j == 4:
                            self.BroadcastGameStatus(self.client_pairs[i][3])
                        # Delete client from room
                        del self.client_pairs[i][j]
                        # If room is on full state and one client is already out
                    elif self.client_pairs[i][0][0] == 1 and len(self.client_pairs[i]) == 4:
                        # Delete this room
                        del self.client_pairs[i]
                    # If room is not full and this client wants to exit
                    elif self.client_pairs[i][0][0] == 0:
                        # Delete this room
                        del self.client_pairs[i]

                    still_checking = 0
                    break

            if still_checking == 0:
                break
        # Delete this client from client channel dictionary
        del self.clients[channel]

    # Anonymous game session creator
    def Matchmaking(self, channel):
        board = [[0 for x in range(10)] for y in range(10)]
        status = "find_match"
        room_full_flag = 0
        ready_state = 0
        # If no room exists
        if len(self.client_pairs) == 0:
            self.client_pairs.append([[room_full_flag, ready_state], [board, board], status, channel])

        # if at least a room exists
        else:
            # Assume this client has no room.
            got_no_room = 1
            # Check every pair in client_pairs
            for pair in self.client_pairs:
                # If room full flag is 0 means it's not full, join client to this room
                if pair[0][0] == 0:
                    pair.append(channel)
                    # This room is full now
                    pair[0][0] = 1
                    # Because it's full, both players are entering the deploy_phase
                    pair[2] = "deploy_phase"
                    # Congratulations! This client gets a room
                    got_no_room = 0
                    break

            # If all rooms already full, make a new one
            if got_no_room == 1:
                self.client_pairs.append([[room_full_flag, ready_state], [board, board], status, channel])

        # print self.client_pairs

    # Send message to itself, other client, or both clients based on flag
    def SendToOther(self, channel, data, flag=1):
        # print "SendToOther", data
        sender = None
        receiver = None
        for pair in self.client_pairs:
            # If there are two users in room
            if pair[0][0] == 1 and len(pair) == 5:
                if pair[3] == channel:
                    sender = pair[3]
                    receiver = pair[4]
                    break
                elif pair[4] == channel:
                    sender = pair[4]
                    receiver = pair[3]
                    break
            # If room is already on full state but the other party quit
            elif pair[0][0] == 1 and len(pair) == 4:
                receiver = pair[3]
                flag = 1

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

    # Broadcast game status
    def BroadcastGameStatus(self, channel):
        for pair in self.client_pairs:
            for index in range(len(pair)):
                if pair[index] == channel:
                    temp_data = {"action": "broadcast", "status": pair[2]}
                    # If only one player exists, broadcast to itself alone
                    if pair[0][0] == 0:
                        # Room: One player, probably still matchmaking
                        self.SendToOther(channel, temp_data, flag=3)
                    # If other player exists, broadcast to both players in room
                    elif pair[0][0] == 1:
                        # Room: Two players, probably in a game session
                        # Let's test it by using flag = 2
                        self.SendToOther(channel, temp_data, flag=2)

    def InitBoard(self, channel, data):
        still_checking = 1
        board_number = None
        for i in range(len(self.client_pairs)):
            for j in range(len(self.client_pairs[i])):
                if self.client_pairs[i][j] == channel:
                    # Update player ready_state
                    self.client_pairs[i][0][1] += 1
                    if j == 3:
                        board_number = 0
                    elif j == 4:
                        board_number = 1

                    # Update board state to deploy_phase result
                    self.client_pairs[i][1][board_number] = data["my_board"]

                    # Send ready_state to players if both are ready
                    if self.client_pairs[i][0][1] == 2:
                        temp_data = {"action": "ready_response", "ready_counter": self.client_pairs[i][0][1]}
                        self.SendToOther(channel, temp_data, flag=2)
                    still_checking = 0
                    break

            if still_checking == 0:
                break

    def print_client_pairs(self):
        for i in range(len(self.client_pairs)):
            print "--------------"
            print i
            for j in range(len(self.client_pairs[i])):
                if j != 1:
                    print self.client_pairs[i][j]
            print "--------------"

    # Main loop
    def Loop(self):
        while True:
            self.Pump()
            # self.print_client_pairs()
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