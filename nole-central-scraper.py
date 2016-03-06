#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nole-central-scraper.py
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

from lxml import html
import requests

event_date_list = []
event_home = requests.get('https://nolecentral.dsa.fsu.edu/events')
event_list_titles_tree = html.fromstring(event_home.content)
event_title_list = event_list_titles_tree.xpath('//h4/text()')
for i in range(len(event_title_list)):
	event_title_list[i] = event_title_list[i].replace("\n", "")
	event_title_list[i] = event_title_list[i].replace("\r", "")
	event_title_list[i] = event_title_list[i].replace("\t", "")

for i in range(len(event_title_list)):
	if event_title_list[i] == 'Search':
		event_title_list[i] = ""
	if event_title_list[i] == 'Filters':
		event_title_list[i] = ""
	if event_title_list[i] == 'Categories':
		event_title_list[i] = ""
	if event_title_list[i] == 'Themes':
		event_title_list[i] = ""
	if event_title_list[i] == 'Recommendations':
		event_title_list[i] = ""
	if event_title_list[i] == 'Perks':
		event_title_list[i] = ""
	if "Monday," in event_title_list[i]:
		event_title_list[i] = ""
	if "Tuesday," in event_title_list[i]:
		event_title_list[i] = ""
	if "Wednesday," in event_title_list[i]:
		event_title_list[i] = ""
	if "Thursday," in event_title_list[i]:
		event_title_list[i] = ""
	if "Friday," in event_title_list[i]:
		event_title_list[i] = ""
	if "Saturday," in event_title_list[i]:
		event_title_list[i] = ""
	if "Sunday," in event_title_list[i]:
		event_title_list[i] = ""
		
event_title_list.remove("")
event_title_list = filter(None, event_title_list)
print(event_title_list)

events = open('event_titles.txt', 'wb')
for i in range(len(event_title_list)):
	events.write(event_title_list[i])
	events.write('\n')
events.close		

event_specific = requests.get('https://nolecentral.dsa.fsu.edu/organization/ChristiansonCampusFSU/calendar/details/832765')
tree = html.fromstring(event_specific.content)
event_title = tree.xpath('//title[1]/text()')
