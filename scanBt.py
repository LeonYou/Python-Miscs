# coding = utf-8

from bs4 import BeautifulSoup
import urllib.request
import socket
import os


PAGE_COUNT = 1
HOST = 'http://www.lwgod.cc'
MAIN_PAGE = 'forum-292-%d.html'
LOCAL_PATH = 'BT'
DOWNLOAD_FILE_TYPE = '.torrent'
DOWNLOAD_FILE_FILTER = ['720p', '1080p']

def getWebPageContent(url):
    f = urllib.request.urlopen(url)
    data = f.read()
    f.close()
    return data

def getWebPageContentForTag(url, tag, classVal):
	data = getWebPageContent(url)
	soup = BeautifulSoup(data, 'html.parser')
	return soup.findAll(tag, classVal)

def createLocalStoragePath(path):
	if not os.path.exists(path):
		os.makedirs(path)

def filterFile(fileName):
	if os.path.splitext(fileName)[-1].lower() != DOWNLOAD_FILE_TYPE:
		return False
	else:
		for key in DOWNLOAD_FILE_FILTER:
			if key in fileName.lower():
				return True
	return False

def downloadFile(url, localFile):
	socket.setdefaulttimeout(30)

	try:
		urllib.request.urlretrieve(url,localFile)
		print(localFile)
	except socket.timeout:
		count = 1
		while count <= 3:
			try:
				urllib.request.urlretrieve(url,localFile)                                                
				break
			except socket.timeout:
				print('Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count)
				++count
		if count > 3:
			print("downloading fialed!")


if __name__ == '__main__':
	createLocalStoragePath(LOCAL_PATH)

	for i in range(PAGE_COUNT):
		pageList = getWebPageContentForTag(HOST + '/' + MAIN_PAGE%(i+1), 'a', 's xst')
		for page in pageList:
			try:
				content = getWebPageContentForTag(HOST + '/' + page['href'], 'ignore_js_op', None)
				btSession = getWebPageContentForTag(HOST + '/' + content[0].a['href'], 'div', 'dxksst')

				btPath = btSession[0].a['href']
				btFileName = btSession[0].font.string
				if not filterFile(btFileName):
					continue

				downloadFile(HOST + '/' + btPath, os.path.join(LOCAL_PATH, btFileName))
			except:
				continue
		
	print('Done')
