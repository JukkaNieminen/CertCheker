from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import json


def getExpiry(URL):
    base_url = URL
    port = '443'

    hostname = base_url
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())
            data = json.dumps(ssock.getpeercert())
            # print(ssock.getpeercert())

    d = json.loads(data)

    return d["notAfter"]

print(getExpiry("www.tavastiasoft.fi"))