#!/usr/bin/env python
# Script will load rfd output in json format from pulled.list file. Then will parse for new items and place into knownitems.list.
# If there are any new items NOT in knownitems.list, it will push to pushover service
# Ensure to provide environment API_TOKEN and USER_TOKEN. ie 'export API_TOKEN="xxxxxxxxxxxxxxx"'
# If using docker ensure to add environment variable, ie '-e API_TOKEN='xxxxxxxxxxxxx''

import os
import json

#Discord Setup
import discord_notify as dn
discord_url = os.environ.get('DISCORD_URL')
if discord_url:
  notifier = dn.Notifier(discord_url)

#Pushover setup
from pushover import Client
api_token = os.environ.get('API_TOKEN')
user_token = os.environ.get('USER_TOKEN')
print("api token: ",api_token)
print("user token: ",user_token)
if api_token:
  if user_token:
    client = Client(user_token, api_token=api_token)

#Load list of pulled items
source_json = []
try:
  with open('pulled.list','r') as rp_pulledlist: #Pull the latest list of results from rfd, load into a python list.
    source_json = json.load(rp_pulledlist)
except IOError:
  f = open('pulled.list','w+')
  print("Pull file created")
  f.close

# Load list of known items
known_list = []
try:
  with open('knownitems.list','r') as rp_knownlist:
    known_list = json.load(rp_knownlist)
except IOError:
  f = open('knownitems.list', 'w+')
  print("Known items list File created")
  f.close()

final_list = []
final_known_list = []
element = {}
newitems_list = []

#Start to build list of known items, include the ones we already know
for element3 in known_list:
  final_list.append(element3)

#Scan the new items

for element in source_json:

  #URL Matcher:
  urlmatch = False
  for key,value in element.items():
    if "url" in key:
      #print("scanning url:", value)
      # check if url matches what we already have
      for element2 in known_list:
        for key2,value2 in element2.items():
          if "url" in key2:
            #print("Does it match:", value2)
            if (value in value2):
              #print("match")
              urlmatch = True

  if not urlmatch:
    #print("appending to new item list")
    final_list.append(element)
    newitems_list.append(element)

#New item list, notify based on these:
print ("New items:", newitems_list)

#Outputting the new list nicely and push
push_list = ""
for element3 in newitems_list:
  for key,value in element3.items():
    push_list = push_list + key + " : " + str(value) + "\n"

if not push_list:
  print("New deal list is empty, not notifying.")

else:  
  print ("New Deals: ", push_list)

  if api_token:
    if user_token:
      print("Sending pushover message.")
      client.send_message(push_list, title="New deal mentioned on RFD")

  if discord_url:
    print("Sending discord webhook message.")  
    notifier.send(push_list, print_message=True)

#write full list including new items into the list file
with open('knownitems.list', 'w+') as fp:
  json.dump(final_list, fp)
