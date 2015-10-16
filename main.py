import requests
#from bs4 import BeautifulSoup

  #cookie UA
  #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"

  #f = open('oreo.html', 'w')
  #f.write(r.text.encode('utf-8'))
  #f.close()

class DKApi:
  def __init__(self):
    self.login()

  def login(self):
    print "Logging in"

    login_url = "https://www.draftkings.com/account/login"
    values = {
      'login' : "itemgrab@gmail.com",
      'password' : "fossil1",
    }

    r = requests.post(login_url, data=values)
    self.cookies = r.cookies

  def fetch_contest_page(self, id):
    print "Fetching contest page for game id: %s" % id
    url = "https://www.draftkings.com/contest/gamecenter/%s" % id
    r = requests.get(url, cookies=self.cookies)

    #print "Status: %s" % r.status_code
    #print "Headers: %s" % r.headers
    #print "Cookies: %s" % r.cookies
    #print "History: %s" % r.history
    #print "Text: %s" % r.text

    return r

  ########### Contest Range Code ###########
  def find_contest_range(self, lower=1, upper=999999999):
    print "Finding contest range with lower bound: %s and upper bound %s" % (lower, upper)

    #First we need to find the first occurance of any hit
    arbitrary_contest_id = self.find_arbitrary_valid_contest(lower, upper)
    print "Arbitrary contest id: %s" % arbitrary_contest_id

    #Now that we know a valid contest ID, we can use that as our upper bound for finding the first valid contest
    first = self.find_first_contest(lower, arbitrary_contest_id)
    print "First contest_id: %s" % first

    #Find last
    last = self.find_last_contest(arbitrary_contest_id, upper)
    print "Last contest_id: %s" % last

    return (first, last)

  #Binary search thru ranges until it finds a single page which returns 200 OK, and doesn't redirect beforehand. 
  def find_arbitrary_valid_contest(self, lower, upper):

    ranges = [ (lower, upper) ]

    while True:
      ranges, contest_id = self.find_contest_in_range(ranges)

      if(ranges == None or len(ranges) == 0):
        print "Ranges have been exhuasted. Contest ID: %s" % contest_id
        break

    return contest_id


  #TODO: Worry about edge cases
  def find_first_contest(self, lower, upper):
    print "Finding first contest with lower bound: %s and upper bound: %s" % (lower, upper)

    while True:
      if(upper - lower < 2):
        if self.contest_has_data(lower):
          return lower
        else:
          return upper

      contest_id = (lower + upper) / 2
      has_data = self.contest_has_data(contest_id)
      if has_data:
        upper = contest_id
      else:
        lower = contest_id


  #TODO: Can most likely combine this with the find_first using logic
  def find_last_contest(self, lower, upper):
    print "Finding first contest with lower bound: %s and upper bound: %s" % (lower, upper)

    while True:
      if(upper - lower < 2):
        if self.contest_has_data(upper):
          return upper
        else:
          return lower

      contest_id = (lower + upper) / 2
      has_data = self.contest_has_data(contest_id)

      if has_data:
        lower = contest_id
      else:
        upper = contest_id

  #Takes a queue of ranges. Tests the first range, and returns a tuple of (Updated queue of ranges, found costest ID). When the function finds its first contest ID, it will set the ranges to "None". 
  def find_contest_in_range(self, ranges):
    range_to_test = ranges.pop(0)
    id_to_test = (range_to_test[0] + range_to_test[1]) / 2

    has_data = self.contest_has_data(id_to_test)

    if has_data:
      return (None, id_to_test)
    else:
      #Split range into 2 sub ranges not including point we just tested
      ranges.append( (range_to_test[0], id_to_test - 1) )
      ranges.append( (id_to_test + 1, range_to_test[1]) )
      return (ranges, None)

  #A bit of a weak test, but sees if the contest page returns 200OK and doesn't redirect. 
  def contest_has_data(self, id):
    had_data = False

    r = self.fetch_contest_page(id)

    if(r.status_code == 200 and len(r.history) == 0):
      print "Contest %s had data" % id
      had_data = True
    
    return had_data

if __name__ == "__main__":
  print "Starting dkBot"
  api = DKApi()
  first, last = api.find_contest_range(1, 29999999)

  print "Finished. First: %s Last: %s" % (first, last)
