from urllib.request import ssl, socket
import json
from win10toast import ToastNotifier

msg ="I fetched this information about the domains listed in C:\\Temp\\CertCheker\\url.txt"
contentList = []
toaster = ToastNotifier()


# Read list of urls from file in ProgramFiles, separated by commas (,)
urlFile = open("C:\\Temp\\CertCheker\\url.txt","r")
content = urlFile.readlines()
urlFile.close()

for item in content:
    item = item.strip('\n')
    contentList.append(item)

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

# Print out the results
expiries = getExpiry(contentList)
for e in expiries:
    msg = msg + e + "\n"

try:
    reportFile = open("C:\\Temp\\CertCheker\\CertReport.txt","w")
    reportFile.write(msg)
    reportFile.close()
    toaster.show_toast("CertCheker notification", "New certificate report is ready for reading @\nC:\Temp\CertReport.txt")
except:
    toaster.show_toast("CertCheker notification", "There was a problem in creating the certtificate report.")