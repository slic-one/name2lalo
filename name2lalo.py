import sys
import httplib
import HTMLParser

is_coordinates = False
res_data = []


class LaLoHTMLParser(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attr):
        global is_coordinates
        if attr == [('class', 'latitude')] or attr == [('class', 'longitude')]:
            is_coordinates = True

    def handle_endtag(self, tag):
        global is_coordinates
        if tag.lower() == "span":
            is_coordinates = False

    def handle_data(self, data):
        global is_coordinates
        if is_coordinates:
            res_data.append(data)


# Try getting command line argument, ask for input if none
try:
    name = sys.argv[1]
except IndexError:
    name = raw_input('Please input city name: ')

connection = httplib.HTTPSConnection('en.wikipedia.org')
connection.request("GET", "/wiki/" + name)

response = connection.getresponse()

if response.status != 200:
    print 'Page not found.'
    quit(1)

# Some encodings trigger UnicodeDecodeError on feed()
page = response.read().decode('utf-8')

parser = LaLoHTMLParser()
data = parser.feed(page)

if len(res_data) >= 2:
    la = res_data[0]
    lo = res_data[1]
    print "%s: %s, %s" % (name, la, lo)
else:
    print 'No data found for this query.'

parser.close()
connection.close()
