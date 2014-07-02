import requests
import hashlib
import random
import string

from bencode import bencode, bdecode

with open("ub.torrent") as f:
    decoded_data = bdecode(f.read())

announce_url = decoded_data['announce']
info = decoded_data['info']
info_hash = hashlib.sha1(bencode(info)).digest()

peer_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))

uploaded = 0
downloaded = 0

overall_file_length = info['length']
left = overall_file_length

compact = 1
no_peer_id = 0

port = 8000

tracker_params = {
    'info_hash': info_hash,
    'peer_id': peer_id,
    'port': port,
    'uploaded': uploaded,
    'downloaded': downloaded,
    'left': left,
    'compact': compact,
    'no_peer_id': no_peer_id,
}

response = requests.get(announce_url, params=tracker_params)
import ipdb
ipdb.set_trace()
