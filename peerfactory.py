from twisted.internet import protocol
from bencode import bencode, bdecode


class PeerProtocol(protocol.Protocol):

    def __init__(self, factory, handshake, torrent):
        self.factory = factory
        self.handshake = handshake
        self.torrent = torrent

    def connectionMade(self):
        self.factory.numConnections += 1
        self.transport.write(self.handshake)

    def dataReceived(self, data):
        print "Received data:", data
        self.torrent.check_handshake(data)
        import ipdb
        ipdb.set_trace()
        self.transport.loseConnection()


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
