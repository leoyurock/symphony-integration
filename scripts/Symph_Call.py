#!/usr/bin/python
import urllib2
import requests
import json
import sys
import os
import time

#Loads the environment variable as JSON structure
#We will use this later
JSON_Data = json.dumps(dict(**os.environ), sort_keys=True, indent=4)
EnvData_dict = json.loads(JSON_Data)

#Building a Slack Pre-Reqs and the message
Open_Msg = ( "<messageML>" )

#Build for WARNING
WARNING_Msg = ( "<b>Severity at " + EnvData_dict["_SEVERITY"] + " | Date : " + time.strftime("%Y-%m-%d") +  " | Time : " + time.strftime("%H:%M:%S") +  "</b> <br/><br>" + \
"<ul>"+ \
"<li>" + "Value : " + EnvData_dict["_VALUE"] + "</li><li>" + "Row.Colum : " + EnvData_dict["_VARIABLE"] + "</li><li>" + "Gateway : " + EnvData_dict["_GATEWAY"] + "</li>" + \
"<li>" + "Probe : " + EnvData_dict["_PROBE"] + "</li><li>" + "Sampler : " + EnvData_dict["_SAMPLER"] + "</li><li>" + "Managed Entity : " + EnvData_dict["_MANAGED_ENTITY"] +"</li>"+ \
"</ul>" + \
"")

#Build for OK
OK_Msg = ( "<b>Severity at " + EnvData_dict["_SEVERITY"] + " | Date : " + time.strftime("%Y-%m-%d") +  " | Time : " + time.strftime("%H:%M:%S") +  "</b> <br/><br>" + \
"<ul>"+ \
"<li>" + "Value : " + EnvData_dict["_VALUE"] + "</li><li>" + "Row.Colum : " + EnvData_dict["_VARIABLE"] + "</li><li>" + "Gateway : " + EnvData_dict["_GATEWAY"] + "</li>" + \
"<li>" + "Probe : " + EnvData_dict["_PROBE"] + "</li><li>" + "Sampler : " + EnvData_dict["_SAMPLER"] + "</li><li>" + "Managed Entity : " + EnvData_dict["_MANAGED_ENTITY"] +"</li>"+ \
"</ul>" + \
"")

#Build for CRITICAL
CRITICAL_Msg = ( "<b>Severity at " + EnvData_dict["_SEVERITY"] + " | Date : " + time.strftime("%Y-%m-%d") +  " | Time : " + time.strftime("%H:%M:%S") +  "</b> <br/><br>" + \
"<ul>"+ \
"<li>" + "Value : " + EnvData_dict["_VALUE"] + "</li><li>" + "Row.Colum : " + EnvData_dict["_VARIABLE"] + "</li><li>" + "Gateway : " + EnvData_dict["_GATEWAY"] + "</li>" + \
"<li>" + "Probe : " + EnvData_dict["_PROBE"] + "</li><li>" + "Sampler : " + EnvData_dict["_SAMPLER"] + "</li><li>" + "Managed Entity : " + EnvData_dict["_MANAGED_ENTITY"] +"</li>"+ \
"</ul>" + \
"")

Close_Msg = ( "</messageML>" )

#After grabbing the environment variables
#Check on the severity environment variable and
#form the message.
if (EnvData_dict["_SEVERITY"] == "WARNING"):
    Send_Msg = Open_Msg + WARNING_Msg + Close_Msg
if (EnvData_dict["_SEVERITY"] == "OK"):
    Send_Msg = Open_Msg + OK_Msg + Close_Msg
if (EnvData_dict["_SEVERITY"] == "CRITICAL"):
    Send_Msg = Open_Msg + CRITICAL_Msg + Close_Msg

#We're using Slack JSON API
#Doing our POST to the URL
webhook_url = 'http://httpbin.org/post'
#webhook_url = 'https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/xxxxxxxxxxxxxxxxx'

#Here we will build the response
response = requests.post( webhook_url, data=Send_Msg, headers={'Content-Type': 'application/text'} )
if response.status_code != 200:
    raise ValueError(
        'Request to Symphony returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

#Writing the whole Env Vars to file for sanity checks
#with open('/export/home/epayano/geneos/scripts/environ.json', 'w') as f:
#    json.dump(dict(**os.environ), f, sort_keys=True, indent=4)
#f.close()

# We're grabbing attributes at a granular level
f = open('/export/home/epayano/geneos/scripts/environ.json', 'w')
#Write out the metadata
f.write(JSON_Data)
#JSON Array Size
f.write('\n')
f.write('JSON array length is : ')
#size of the array convert to string
f.write(str(len(EnvData_dict)))
f.write('\n')
#Server Response
f.write('server status_code : ')
f.write(str(response.status_code))
f.write('\n')
f.write('server reason : ')
f.write(str(response.reason))
f.write('\n')
f.write('server response text : ')
f.write(str(response.text))
f.write('\n')
#Wriet our Message onto file
f.write(str(Send_Msg))
f.write('\n')
#Close the file up
f.close()
