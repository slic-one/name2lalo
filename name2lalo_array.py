import sys
import httplib
import HTMLParser
import json

is_latitude = False
is_longitude = False

is_coordinates = False
res_data = []

la = ""
lo = ""


class LaLoHTMLParser(HTMLParser.HTMLParser):
    """ Custom HTMLParser class to handle only specific data """

    def handle_starttag(self, tag, attr):
        global is_latitude
        global is_longitude
        if attr == [('class', 'latitude')]:
            is_latitude = True
        elif attr == [('class', 'longitude')]:
            is_longitude = True

    def handle_endtag(self, tag):
        global is_latitude
        global is_longitude
        if tag.lower() == "span":
            is_latitude = False
            is_longitude = False

    def handle_data(self, data):
        global is_latitude
        global is_longitude

        global la
        global lo

        if is_latitude:
            la = data
        elif is_longitude:
            lo = data


def parse_wiki(city):
    global la
    global lo

    connection = httplib.HTTPSConnection('en.wikipedia.org')
    connection.request("GET", "/wiki/" + city)

    # Clear values:
    la = ""
    lo = ""

    try:
        response = connection.getresponse()
    except httplib.ResponseNotReady:
        return -1

    if response.status != 200:
        print city + ': Page not found.'
        return -1

    # Some encodings trigger UnicodeDecodeError on feed()
    page = response.read().decode('utf-8')

    parser.feed(page)

    connection.close()

    if la == "" or lo == "":
        print city + ": No coordinates found on this page"
        return -1

    return {
        'name': city,
        'la': la,
        'lo': lo,
    }


parser = LaLoHTMLParser()

# Try getting command line argument, if none - ask for input:
file_name = ""
try:
    file_name = sys.argv[1]
except IndexError:
    file_name = raw_input('Please input city name: ')

# Read input .json file:
try:
    with open(file_name) as data_file:
        city_names = json.load(data_file)
except IOError:
    print "Couldn't parse the file"
    quit(1)

output_file = open('out.json', 'w')
output_data = []
# Write output:
for index in range(len(city_names)):
    result = parse_wiki(city_names[index]["name"])
    if result != -1:
        output_data.append(result)
        print result['name'] + ": " + result['la'] + ", " + result['lo']

json.dump(output_data, output_file, indent=4, sort_keys=True, ensure_ascii=True)

output_file.close()
parser.close()
