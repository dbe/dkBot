import urllib2
from bs4 import BeautifulSoup


if __name__ == "__main__":
  print "Starting dkBot"

  url = "http://www.draftkings.com/contest/gamecenter/9568996"
  opener = urllib2.build_opener()
  opener.addheaders.append( ('Cookie', 'hey=there') )

  print "Fetching: %s" % url
  response = opener.open(url)
  print "Finished fetching resource"

  print "Info %s" % response.info()
  print "Url %s" % response.geturl()
  print "Code %s" % response.getcode()


  print "Building soup"
  soup = BeautifulSoup(response.read(), "html.parser")

  print "All links at url:"
  print soup.find_all('a')



