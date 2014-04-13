 # This file is part of MartianNet.
 #
 # MartianNet is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 # MartianNet is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with MartianNet.  If not, see <http://www.gnu.org/licenses/>.


# coding: UTF-8

## IMPORTS  ##
import string
#from sys import argv
import sys
#from urllib2 import urlopen # opens urlb2ul
import urllib2
from bs4 import BeautifulSoup # parses html

## FUNCTIONS ##
# file writing function
def writeFile(filename, data):
	f = open(filename, 'w')
	f.write(data)
	f.close

## INPUTS ##
#target = 'http://en.wikipedia.org/wiki/Glasgow' # target url
target = sys.argv[1]
nlinks = 10 # number of links to pre-load

## LOOP ##
# opens the url
mypage = urllib2.urlopen(target)

soup = BeautifulSoup(mypage)

# formats html and turns it into a string
prettysoup = (soup.prettify())

#removing non ascii characters
asciisoup = filter(lambda x: x in string.printable, prettysoup)

# writes the target page to file
writeFile('basefile.html', asciisoup)

urls = [] # list to store urls from target url page

for link in soup.find_all("a"): #{"class": "mw-redirect"}):
	urls.append(link.get('href'))

#print urls

pieces = string.split(target, '/')
rootsite = pieces[0] + '//' + pieces[2]

#create a script to use 'sed' to replace the links with
#the adree of the file where it was stored
sedScript = open('sedScript.sh', "w")

for url in range(0,len(urls)):#nlinks):
	#newpage = 'http://en.wikipedia.org' + urls[url]
	newpage = urls[url]
	newpageOLD = newpage
	#print newpage
	if newpage != None:
		https = string.find(newpage, 'https://')
		http = string.find(newpage, 'http://')
		if (https == -1) and (http == -1):
			print newpage
			newpage = rootsite + newpage
			print newpage
		try:
			openpage = urllib2.urlopen(newpage)
			newsoup = BeautifulSoup(openpage)
			lamesoup = (newsoup.prettify())
			newascii = filter(lambda x: x in string.printable, lamesoup)
			writeFile('remotefile'+str(url)+'.html', newascii)
			#write to sedScript
			sedLine = "sed -i -e \'s@" + newpageOLD + "@" + \
						'remotefile'+str(url)+'.html@g\' ' + \
						"basefile.html\n"
			sedScript.write(sedLine) # writes to script
		except urllib2.URLError:
			print 'Skipping'

sedScript.close()
