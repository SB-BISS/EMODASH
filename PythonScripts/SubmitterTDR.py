
import threading
import time
import json
import urllib3
import certifi

'''
URL IS HARD CODED, to be improved.
'''


# use with or without proxy
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)
# http = urllib3.proxy_from_url('http://proxy_host:proxy_port')

# interaction for a specific Device instance - replace 'd000-e000-v000-i000-c000-e001' with your specific Device ID
url = 'https://iotmmsp1941838965trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/7d9da3fb-ffcd-46cb-bb2f-cdb1c8c78c9f'

headers = urllib3.util.make_headers()

# use with authentication
# please insert correct OAuth token
headers['Authorization'] = 'Bearer bf7d76bf122dfa78f2b1e5b1899746e'
headers['Content-Type'] = 'application/json;charset=utf-8'

class SubmitterTDR (threading.Thread):
   def __init__(self, threadID, body):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.body = body
 
   def run(self):
      self.send_body(self.name, self.body)
      
   def send_body(self,threadName, body):
    try:
        r = http.urlopen('POST', url, body=str(body), headers=headers)
        print(r.status)
        print(r.data)
        
    except urllib3.exceptions.SSLError as e:
        print (e)
        
    #threadName.exit()
      
      
