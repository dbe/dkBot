import urllib
import urllib2

import requests

from bs4 import BeautifulSoup

  #cookie UA
  # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  
def login():
  print "Logging in"

  login_url = "https://www.draftkings.com/account/login"
  values = {
    'login' : "itemgrab@gmail.com",
    'password' : "fossil1",
  }

  r = requests.post(login_url, data=values)
  cookies = r.cookies
  print "Cookies: %s" % cookies

  return cookies

def fetch_contest_page(id, cookies):
  print "Fetching contest page for game id: %s" % id
  url = "https://www.draftkings.com/contest/gamecenter/%s" % id
  r = requests.get(url, cookies=cookies)

  print "Status: %s" % r.status_code
  print "Headers: %s" % r.headers
  print "Cookies: %s" % r.cookies
  print "History: %s" % r.history
  #print "Text: %s" % r.text


  #f = open('oreo.html', 'w')
  #f.write(r.text.encode('utf-8'))
  #f.close()

if __name__ == "__main__":
  print "Starting dkBot"

  cookies = login()
  #fetch_contest_page(10512345, cookies)
  fetch_contest_page(9512345, cookies)

