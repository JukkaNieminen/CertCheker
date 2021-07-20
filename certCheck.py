from urllib.request import ssl, socket
import json
from win10toast import ToastNotifier

i = "i"

# List of URLs
urls = []
print("Press <ENTER> when you have entered the last URL")
while i != "":
    i = input("Insert URL you want to check: ")
    if i != "":
        urls.append(i)
    else:
        i =""

def getExpiry(addresses):
    expiryList = []
    for url in addresses:
        base_url = url
        port = '443'

        hostname = base_url
        context = ssl.create_default_context()
        # Create a connection to the hostname using SSL and save socket information to variable
        try:
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    data = json.dumps(ssock.getpeercert())
        except: 
            expiryList.append("Could not get certificate information of " + url + ", did you type the URL correctly and is the site running on port 443?")
            continue
        # Load data to dictionary
        d = json.loads(data)
        # Append hostname and expiry time to list
        a = "SSL-Certificate of " + url + " will expire @ " + str((d["notAfter"]))
        expiryList.append(a)
  
    # Return the list (duh)
    return expiryList

toaster = ToastNotifier()

# Print out the results
expiries = getExpiry(urls)
for e in expiries:
    toaster.show_toast("CertCheker notification", e)