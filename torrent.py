import requests
import hashlib
import random
import string
import socket

from bencode import bencode, bdecode


class Torrent(object):
    """
    Given a filename decodeds & parses tracker info

    - build torrent class
    - open torrent file
    - decode torrent file
    - get response from tracker
    - get peer list
    """

    def __init__(self, torrent_filename):
        self.filename = torrent_filename
        self.decoded_data = self.decode_file()
        self.announce_url = self.decoded_data['announce']
        self.info = self.decoded_data['info']
        self.info_hash = hashlib.sha1(bencode(self.info)).digest()
        self.peer_id = ''.join(random.choice(string.ascii_lowercase +
                                             string.digits) for x in range(20))
        self.overall_file_length = self.info['length']
        self.download_left = self.overall_file_length
        self.uploaded = 0
        self.downloaded = 0
        self.compact = 1
        self.no_peer_id = 0
        self.port = 8123
        self.tracker_params = {
            'info_hash': self.info_hash,
            'peer_id': self.peer_id,
            'port': self.port,
            'uploaded': self.uploaded,
            'downloaded': self.downloaded,
            'left': self.download_left,
            'compact': self.compact,
            'no_peer_id': self.no_peer_id,
        }
        self.tracker_response = self.get_tracker_response()
        self.peers_list = self.get_peer_list()

    def decode_file(self):
        """
        Returned bencode decoded torrent file
        """
        with open(self.filename) as f:
            decoded_data = bdecode(f.read())

        return decoded_data

    def get_tracker_response(self):
        """
        Get request is sent to the tracker along with parsed torrentfile data
        """
        response = requests.get(
            self.announce_url,
            params=self.tracker_params
        )
        response_decoded = bdecode(response.content)

        return response_decoded

    def get_peer_list(self):
        """
        Decodeds peers value may be a string consisting of multiples of 6 bytes
        First 4 bytes are the IP address and last 2 bytes are the port number
        """
        peers = self.tracker_response['peers']
        peer_address = ''
        peer_list = []

        for i, peer in enumerate(peers):
            if i % 6 == 4:
                port_large = ord(peer) * 256
            elif i % 6 == 5:
                port = port_large + ord(peer)
                peer_address += ':' + str(port)
                peer_list.append(peer_address)
                peer_address = ''
            elif i % 6 == 3:
                peer_address += str(ord(peer))
            else:
                peer_address += str(ord(peer)) + '.'

        return peer_list

    def connect_to_peer(self, peer):
        """
        Given a peer id address initiate a handshake
        """
        sock = socket.socket()
        ip, port = peer.split(':')
        port = int(port)
        sock.connect((ip, port))

        pstrlen = chr(19)
        pstr = "BitTorrent protocol"
        reserved = 8 * chr(0)
        response_size = 68
        handshake = pstrlen + pstr + reserved + self.info_hash + self.peer_id
        sock.send(handshake)
        peer_response = sock.recv(response_size)

        return peer_response

if __name__ == "__main__":
    tor = Torrent('ub.torrent')
    peer_response = tor.connect_to_peer(tor.peers_list[0])
    print peer_response
    import ipdb
    ipdb.set_trace()
