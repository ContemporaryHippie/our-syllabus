#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  beautiful-soup-navigator.py
#  
#  Copyright 2016 James Matherly <james@ElNovoBuntu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from bs4 import BeautifulSoup
import urllib
import json
import xlsxwriter
import csv

pre_ahref_tags = []
ahref_tags = []
date_and_time = []
soup = []
title = []
description = []
location = []
row = 0
col = 0
event_dict ={
	'Title': [],
	'Location': [],
	'Date and Time': [],
	#'Description': [],
}

with open('event_titles.txt') as f:
    content = f.readlines() #stores each line from f(events.txt) in content

for i in range(len(content)): #removes special characters
	content[i] = content[i].replace("\n", "")
	content[i] = content[i].replace("\r", "")
	content[i] = content[i].replace("\t", "")

nole_central_page = urllib.urlopen('https://nolecentral.dsa.fsu.edu/events').read() #reads from Nole Central
page_code = BeautifulSoup(nole_central_page) #stores Nole central's source

for i in content: 
	pre_ahref_tags.append(page_code.find_all(title=i)) #stores anchor tags into pre_ahref_tags

for i in range(len(pre_ahref_tags)):
	ahref_tags.append(pre_ahref_tags[i][0]['href'])

for i in range(len(ahref_tags)):
	title.append(content[i])
	event_page = urllib.urlopen('https://nolecentral.dsa.fsu.edu/%s' % (ahref_tags[i])).read()
	event_code = BeautifulSoup(event_page)
	location.append(event_code.find_all('h3', class_ = '__sectionmargintophalf')[0].text)
	location[i] = location[i].replace("\n", "")
	location[i] = location[i].replace("\r", "")
	location[i] = location[i].replace("\t", "")
	location[i] = str(location[i])
	date_and_time.append(event_code.find_all("div", class_ = "event-info-h3indent")[0].text)
	date_and_time[i] = date_and_time[i].replace("\n", "")
	date_and_time[i] = date_and_time[i].replace("\r", "")
	date_and_time[i] = date_and_time[i].replace("\t", "")
	date_and_time[i] = str(date_and_time[i])
	"""description.append(event_code.find_all("div", class_ = "event-info-description __sectionmargintophalf")[0].text)
	description[i] = description[i].replace("\n", "")
	description[i] = description[i].replace("\r", "")
	description[i] = description[i].replace("\t", "")
	description[i] = str(description[i])"""

event_dict['Title'].append(title)
event_dict['Location'].append(location)
event_dict['Date and Time'].append(date_and_time)
for i in range(len(location)):
	if 'Huge' in location[i]:
		location[i] = 'HCB Classroom Building)'
	if 'Thagard' in location[i]:
		location[i] = '960 Learning Way, Tallahassee, FL 32306'
	if ('Florida State University' not in location[i]):
		location[i] += ', Florida State University'


with open('event_data.json', 'w') as f:
     json.dump(event_dict, f)


f = open('dict.csv','wb')

writer = csv.writer(open('dict.csv', 'wb'))
writer.writerow(['Date and Time', 'Location', 'Title'])
for i in range(len(title)):
	writer.writerow([date_and_time[i], location[i], title[i]])
f.close()

