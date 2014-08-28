from twisted.internet import protocol


class PeerProtocol(protocol.Protocol):

    def __init__(self, factory, handshake, torrent):
        self.factory = factory
        self.handshake = handshake
        self.torrent = torrent
        self.interested_msg = 3 * chr(0) + chr(1) + chr(2)
        self.peer_state = "HANDSHAKE"
        self.total_pieces = 0
        self.peer_pieces = []

    def connectionMade(self):
        self.factory.numConnections += 1

        print "Send Handshake: %r" % self.handshake
        self.transport.write(self.handshake)

    def dataReceived(self, data):
       # Check to find type of message

        if data[4] == chr(0):
            print "Choke Message: %r" % data

        elif data[4] == chr(1):
            print "Unchoke Message: %r" % data
            self.peer_state = "UNCHOKE"

            # send request message here

            import ipdb
            ipdb.set_trace()

        elif data[4] == chr(2):
            print "Interested Message: %r" % data

        elif data[4] == chr(3):
            print "Non-Interested Message: %r" % data

        elif data[4] == chr(4):
            print "Have Message: %r" % data

        elif data[4] == chr(5):
            print "Bitfield Message: %r" % data
            
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

        else:
            print "Handshake Message: %r" % data
            if self.checkHandshake(data):
                self.peer_state = "CHOKE"
                print "Send Interested Message: %r" % self.interested_msg
                self.transport.write(self.interested_msg)
        
    def checkHandshake(self, data):
        # handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
        pstrlen = ord(data[0])
        pstr = data[1:pstrlen + 1]
        reserved = data[pstrlen + 1:pstrlen + 1 + 8]
        info_hash = data[pstrlen + 1 + 8:pstrlen + 1 + 8 + 20]
        peer_id = data[pstrlen + 1 + 8 + 20:pstrlen + 1 + 8 + 20 + 20]

        # Put code here to check if we want to connect to peer

        return True


class PeerFactory(protocol.ClientFactory):
    numConnections = 0

    def __init__(self, handshake, torrent):
        self.handshake = handshake
        self.torrent = torrent

    def buildProtocol(self, addr):
        return PeerProtocol(self, self.handshake, self.torrent)

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
