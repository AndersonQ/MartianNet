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
import sys # to use argv 
import urllib2 # to use urlopen
from bs4 import BeautifulSoup # parses html

## FUNCTIONS ##
# file writing function
def writeFile(filename, data):
	f = open(filename, 'w')
	f.write(data)
	f.close

## INPUTS ##
target = sys.argv[1] # the target url taken as an argument when running script
#nlinks = 10 # the number of links to crawl and pre-load (still to be implemented)

## LOOP ##
# opens the url
mypage = urllib2.urlopen(target)

# creates parse tree from url
soup = BeautifulSoup(mypage)

# turns parse tree into formatted Unicode string
prettysoup = (soup.prettify())

#removes non ascii characters (beautiful soup doesn't like them)
asciisoup = filter(lambda x: x in string.printable, prettysoup)

# writes the target page to file
writeFile('basefile.html', asciisoup)

urls = [] # list to store urls found on target page

# searches tree for all links and appends links to urls list
for link in soup.find_all("a"):
	urls.append(link.get('href'))

# extracts the root url from target url
pieces = string.split(target, '/')
rootsite = pieces[0] + '//' + pieces[2]

#creates a script to use 'sed' to replace the links with
#the address of the file where it was stored
sedScript = open('sedScript.sh', "w")

for url in range(0,len(urls)):
	newpage = urls[url]
	newpageOLD = newpage
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
			prettynewsoup = (newsoup.prettify())
			newasciisoup = filter(lambda x: x in string.printable, prettynewsoup)
			writeFile('remotefile'+str(url)+'.html', newasciisoup)
			#write to sedScript
			sedLine = "sed -i -e \'s@" + newpageOLD + "@" + \
						'remotefile'+str(url)+'.html@g\' ' + \
						"basefile.html\n"
			sedScript.write(sedLine) # writes to script
		except urllib2.URLError:
			print 'Skipping'

sedScript.close()