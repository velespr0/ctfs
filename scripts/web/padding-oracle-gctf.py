# google-ctf-2016 wolf spider
from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import socket
import time

PROXIES = {}#'http': 'http://127.0.0.1:8082', 'https': 'http://127.0.0.1:8082'}

class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.Session()
        self.session.proxies = PROXIES
        self.session.verify = False
        self.wait = kwargs.get('wait', 2.0)

    def oracle(self, data, **kwargs):
        ct = str(data).encode('hex')
        print 'Testing %s' % ct
        url = 'https://wolf-spider.ctfcompetition.com/qwerty'
        cookies = {'UID': 'b6fa37b734fe0fe603ea8f6c326bf4d92abda1c1.' + ct}

        r = self.session.get(url, cookies=cookies)
        print '%s %d %d %s' % (ct.encode('hex'), r.status_code, len(str(r.headers)), len(r.text))
        
        if r.status_code == 500:
            raise BadPaddingException
        else:
            return

if __name__ == '__main__':
  import logging
  import sys
  import re
  
  logging.basicConfig(level=logging.DEBUG)
  logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)
  
  padbuster = PadBuster()

  if sys.argv[1] == 'encrypt':

    payload = '757365726e616d653d70696d707380000000000000000000000000000000017026757365726e616d653d61646d696e'.decode('hex')

    iv = '3a57f1a4662f38f0d64552571bdd6850'.decode('hex')
    encrypted = padbuster.encrypt(payload, block_size=16)
    print 'encrypted: %r' % encrypted

  else:
    #original_cipher = b64decode(b64decode(sys.argv[1]).split('=', 1)[1])
    ct = '3a57f1a4662f38f0d64552571bdd68506dd90a8056a979b1278eae82a8ad42f1'
    print('Original cipher: %r' % ct)
  
    pt = padbuster.decrypt(ct[32:].decode('hex'), block_size=16, iv=ct[:32].decode('hex'))
    print('Decrypted cipher: %r' % pt)

# vim: ts=2 sw=2 sts=2 et fdm=marker
