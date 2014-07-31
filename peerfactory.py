from twisted.internet import protocol


class PeerProtocol(protocol.Protocol):

    def __init__(self, factory, handshake):
        self.factory = factory
        self.handshake = handshake

    def connectionMade(self):
        self.factory.numConnections += 1
        self.transport.write(self.handshake)

    def dataReceived(self, data):
        print "Received data:", data
        self.transport.loseConnection()


class PeerFactory(protocol.ClientFactory):
    numConnections = 0

    def __init__(self, handshake):
        self.handshake = handshake

    def buildProtocol(self, addr):
        return PeerProtocol(self, self.handshake)

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
