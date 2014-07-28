from torrent import Torrent
from client import EchoFactory
from twisted.internet import reactor

tor = Torrent('ub.torrent')

reactor.run()

for peer in tor.peers_list[0:3]:
    handshake = tor.get_handshake(peer)
    ip_add, port = peer.split(":")
    print 'connection to ', ip_add, port
    reactor.connectTCP(ip_add, int(port), EchoFactory(handshake))




# peer_response = tor.connect_to_peer(tor.peers_list[0])
# print peer_response
# import ipdb
# ipdb.set_trace()
