from twisted.internet import protocol
from message import Message


class Peer(protocol.Protocol):

    def __init__(self, factory, handshake, torrent):
        self.factory = factory
        self.handshake = handshake
        self.torrent = torrent

        self.message_list = []
        self.interested_msg = 3 * chr(0) + chr(1) + chr(2)
        
        self.peer_state = "HANDSHAKE"
        self.total_pieces = 0
        self.peer_pieces = []

    def connectionMade(self):
        self.factory.numConnections += 1

        # print "Send Handshake: %r" % self.handshake
        self.transport.write(self.handshake)

    def dataReceived(self, data):
        # Take data and push it to message list
        print "Data Received: %r" % data
        self.populateMessageList(data)
        
        while(self.message_list and self.message_list[0].checkLength()):  
            temp = self.returnNextMessage()
            print "Type: %r" % temp.msg_type
            print "Full Message: %r" % temp.msg

            if temp.msg_type == "BITFIELD":
                self.total_pieces = ord(data[3])-1
                print "Peer total pieces: %r" % self.total_pieces

                # Converts each byte to a string of bits (temp_binary_piece)
                for i in range(5,5+self.total_pieces):
                    temp_binary_piece = bin(ord(data[i]))[2:].rjust(8,'0')

                    # Stores each bit so we know which piece peer has
                    for j in range(0,8):
                        self.peer_pieces.append(temp_binary_piece[j])

                # Send Unchoke Message
                print "Send unchoke msg after bitfield msg"
                self.transport.write(self.interested_msg)

            elif temp.msg_type == "HAVE":
                pass

            elif temp.msg_type == "KEE_ALIVE":
                pass

            elif temp.msg_type == "CHOKE":
                pass

            elif temp.msg_type == "UNCHOKE":
                pass

            elif temp.msg_type == "INTERESTED":
                pass

            elif temp.msg_type == "NOT_INTERESTED":
                pass

            import ipdb
            ipdb.set_trace()


    def populateMessageList(self,data):
        # Function to push either partial or full msg to list

        if(self.peer_state == "HANDSHAKE"):
            self.addHandshake(data)

        elif(self.peer_state == "MESSAGE"):

            if(self.message_list):

                if(self.message_list[-1].checkLength()):
                    # Last message is complete, add new message
                    self.addNewMessage(data)
                else:
                    # Last message is not complete, insert rest of message
                    self.addIncompleteMessage(data)
            else:
                # No messages, add new message
                self.addNewMessage(data)

    def addIncompleteMessage(self,data):
        msg_full_len = self.message_list[-1].length
        msg_1_len = len(self.message_list[-1].msg)
        msg_2_len = msg_full_len - msg_1_len

        total_size = len(data)

        if(total_size == msg_2_len):
            self.message_list[-1].msg += data
        elif(total_size > msg_2_len):
            self.message_list[-1].msg += data[0:msg_2_len]
            self.populateMessageList(data[msg_2_len:total_size])
        else:
            self.message_list[-1].msg += data

    def addNewMessage(self, data):
        if(data[3] == chr(0)):
            msg_type = "KEEP_ALIVE"
            msg_size = 4

        elif(data[4] == chr(0)):
            msg_type = "CHOKE"
            msg_size = 5

        elif(data[4] == chr(1)):
            msg_type = "UNCHOKE"
            msg_size = 5

        elif(data[4] == chr(2)):
            msg_type = "INTERESTED"
            msg_size = 5

        elif(data[4] == chr(3)):
            msg_type = "NOT_INTERESTED"
            msg_size = 5

        elif(data[4] == chr(4)):
            msg_type = "HAVE"
            msg_size = 5

        elif(data[4] == chr(5)):
            msg_type = "BITFIELD"
            msg_size = (ord(data[3])-1)+5

        total_size = len(data)

        if(total_size == msg_size):
            temp = Message(msg_size, data, msg_type)
            self.message_list.append(temp)
        elif(total_size > msg_size):
            temp = Message(msg_size, data[0:msg_size],msg_type)
            self.message_list.append(temp)
            self.populateMessageList(data[msg_size:total_size])
        else:
            temp = Message(msg_size, data[0:total_size], msg_type)
            self.message_list.append(temp)

    def addHandshake(self,data):
        total_size = len(data)
        hndshk_size = ord(data[0])+49

        if(len(data) == hndshk_size):
            temp = Message(hndshk_size,data,"HANDSHAKE")
            self.message_list.append(temp)
            self.peer_state = "MESSAGE"

        elif(len(data) > hndshk_size):
            temp = Message(hndshk_size,data[0:hndshk_size],"HANDSHAKE")
            self.message_list.append(temp)
            self.peer_state = "MESSAGE"
            self.populateMessageList(data[hndshk_size:total_size])

        else:
            temp = Message(hndshk_size,data[0:total_size],"HANDSHAKE")
            self.messsage_list.append(temp)
        

    def returnNextMessage(self):
        if(self.message_list[0].checkLength()):
            return self.message_list.pop(0)
        else:
            return 0


class PeerFactory(protocol.ClientFactory):
    numConnections = 0

    def __init__(self, handshake, torrent):
        self.handshake = handshake
        self.torrent = torrent

    def buildProtocol(self, addr):
        return Peer(self, self.handshake, self.torrent)

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
