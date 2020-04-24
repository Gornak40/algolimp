from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def userInfo(handle):
	req = get('https://codeforces.com/api/user.info?handles={}'.format(handle))
	if req:
		return req.json()['result'][0]


def getTitle(link):
	req = get(link, headers={'user-agent': UserAgent().random})
	bs = BeautifulSoup(req.content)
	if not bs.title:
		return 'Статья'
	return bs.title.string


def getColor(user):
	r = user.get('rating')
	if r is None:
		return 'white'
	if r < 1200:
		return 'gray'
	if r < 1400:
		return 'green'
	if r < 1600:
		return '#03A89E'
	if r < 1900:
		return 'blue'
	if r < 2100:
		return '#a0a'
	if r < 2400:
		return '#FF8C00'
	return 'red'


def searchFunc(algo, flt):
	flt = flt.lower().strip().split()
	if not flt:
		return True
	text = (algo.name + ' ' + algo.other).lower()
	return any([x in text for x in flt])