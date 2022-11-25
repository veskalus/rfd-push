#!/usr/bin/env python

import os
import json

#Pushover setup
api_token = os.environ['API_TOKEN']
user_token = os.environ['USER_TOKEN']

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
      print("scanning url:", value)
      # check if url matches what we already have

      for element2 in known_list:
        for key2,value2 in element2.items():
          if "url" in key2:
            print("Does it match:", value2)

            if (value in value2):
              print("match")
              urlmatch = True

  if not urlmatch:
    print("appending to new item list")
    final_list.append(element)
    newitems_list.append(element)

#New item list, notify based on these:
print ("New items:", newitems_list)

#priont("Known list:", )

print ("Final known list:", final_list)

#write full list including new items into the list file
with open('knownitems.list', 'w+') as fp:
  json.dump(final_list, fp)
