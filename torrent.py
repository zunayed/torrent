import requests
import hashlib
import random
import string

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
        self.overall_file_length = self.info['length']
        self.download_left = self.overall_file_length
        self.uploaded = 0
        self.downloaded = 0
        self.compact = 1
        self.no_peer_id = 0
        self.port = 8123
        self.peer_id = self.generate_peer_id()
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

    def generate_peer_id(self):
        peer_id = ''.join(random.choice(string.ascii_lowercase +
                                        string.digits) for x in range(20))

        return peer_id

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

    def get_peer_address(self, peer):
        f = lambda x: str(ord(x))
        ip_address = '.'.join(map(f, peer[0:4]))
        port = str((ord(peer[4])*256)+ord(peer[5]))
        return ip_address + ':' + port

    def get_peer_list(self):
        """
        Decodeds peers value may be a string consisting of multiples of 6 bytes
        First 4 bytes are the IP address and last 2 bytes are the port number
        """
        peer_string = self.tracker_response['peers']
        peers = [peer_string[i:i+6] for i in range(0, len(peer_string), 6)]

        return map(self.get_peer_address, peers)

    def get_handshake(self, peer):
        """
        Given a peer id address return a handshake
        """
        pstrlen = chr(19)
        pstr = "BitTorrent protocol"
        reserved = 8 * chr(0)
        handshake = pstrlen + pstr + reserved + self.info_hash + self.peer_id
        return handshake
