import http.client
import json

conn = http.client.HTTPSConnection("sanggar.cloudciti.io")

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/json" 
}

payload = json.dumps({
    "status": "dari python", 
    "path": "s3://test-terminated-staging-4bxka/",
    "message" : "pythone",
    "size" : "999mb"
})

conn.request("GET", "/v9/dbaas/backup/MWZhM2M5YzktMjc0Ni00MGE3LWIxZmEtNDdiOWE1NGQwNzUy/validateBackup", payload, headersList)
response = conn.getresponse()
result = response.read()

print(result.decode("utf-8"))