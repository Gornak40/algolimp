from requests import get


def userInfo(handle):
	req = get('https://codeforces.com/api/user.info?handles={}'.format(handle))
	if req:
		return req.json()['result'][0]