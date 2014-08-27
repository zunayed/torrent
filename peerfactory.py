from twisted.internet import protocol


class PeerProtocol(protocol.Protocol):

    def __init__(self, factory, handshake, torrent):
        self.factory = factory
        self.handshake = handshake
        self.torrent = torrent
        self.interested_msg = 3 * chr(0) + chr(1) + chr(2)
        self.peer_state = "HANDSHAKE"

    def connectionMade(self):
        self.factory.numConnections += 1

        print "Send Handshake: %r" % self.handshake
        self.transport.write(self.handshake)

    def dataReceived(self, data):
        print "Length: %d" % len(data)

        if self.peer_state == "HANDSHAKE":
            print "Received Handshake Data: %r" % data

            if self.checkHandshake(data):
                self.peer_state = "CHOKE"
                print "Send Interested Message: %r" % self.interested_msg
                self.transport.write(self.interested_msg)
                # import ipdb
                # ipdb.set_trace()

        if self.peer_state == "CHOKE":

            # Check to find type of message
            if data[4] == chr(0):
                print "Choke Message: %r" % data
            elif data[4] == chr(1):
                print "Unchoke Message: %r" % data
            elif data[4] == chr(2):
                print "Interested Message: %r" % data
            elif data[4] == chr(3):
                print "Non-Interested Message: %r" % data
            elif data[4] == chr(4):
                print "Have Message: %r" % data
            elif data[4] == chr(5):
                print "Bitfield Message: %r" % data
            else:
                print "Unknown Message: %r" % data
            
            import ipdb
            ipdb.set_trace()

        # self.transport.loseConnection()

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
